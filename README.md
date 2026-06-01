# AML Daily Task

基于 **Dify AI 工作流**的反洗钱（AML）案件自动分析系统。从银行核心系统定时拉取案件数据，经过结构化预处理后批量调用 AI 工作流进行风险研判，结果入库并提供 REST API 查询。

---

## 目录

- [项目背景](#项目背景)
- [系统架构](#系统架构)
- [核心流程](#核心流程)
- [目录结构](#目录结构)
- [快速启动](#快速启动)
- [环境变量](#环境变量)
- [API 接口](#api-接口)
- [数据说明](#数据说明)

---

## 项目背景

银行反洗钱合规部门每日需要对可疑交易案件进行人工研判，工作量大且重复性高。本项目将案件数据自动化接入 Dify AI 工作流，实现：

- 自动从 T3B 核心系统下载案件数据（`.unl.gz` 格式）
- 对原始数据进行结构化聚合（区分对公/对私客户，汇总交易特征）
- 并发调用 Dify 工作流完成 AI 风险研判
- 结果持久化，支持按案件流水号查询

---

## 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                      APScheduler                        │
│              （定时触发，支持 cron 表达式）                │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│               DownloadUnlService                        │
│         POST 接口拉取 t3b_case_aml_llmp.unl.gz           │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  unl_gz_to_csv                          │
│     解压 gzip，以 \x07 (^G) 为分隔符转换为 CSV            │
│              （Informix UNL 格式）                       │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│              CSVProcessingService                       │
│  • 列名映射（中文 → 英文字段）                             │
│  • 按 case_id 聚合多条交易记录                            │
│  • 区分对公（C）/ 对私（I）客户，输出不同字段集              │
│  • 计算交易统计（总额、笔数、夜间交易、借贷分类等）           │
│  • 块内去重，支持大文件分块处理                            │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│               BatchApiService                           │
│  ThreadPoolExecutor 并发处理每行数据                      │
│  ① POST /files/upload  上传单行 CSV 到 Dify              │
│  ② POST /workflows/run 触发工作流（input: AML_message）  │
│  ③ 解析 outputs.RES，写入 dify_call_results 表           │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│            PostgreSQL / SQLite                          │
│         dify_call_results（按 case_id 存储）             │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│              Flask REST API（:5000）                     │
│         GET /dify_result/<case_id> 查询结果              │
└─────────────────────────────────────────────────────────┘
```

---

## 核心流程

### 1. 数据采集
系统在每次任务执行前，通过 POST 接口从文件服务器下载 `.unl.gz` 格式的案件数据文件（T3B 系统 Informix 数据库导出格式，字段以 `^G` 分隔）。

### 2. 格式转换
将 `.unl.gz` 解压并转换为标准 CSV，字段按预定义映射表从中文列名转换为英文字段名。

### 3. 数据预处理
`CSVProcessingService` 对原始明细数据进行聚合：

| 聚合维度 | 说明 |
|---------|------|
| 客户基本信息 | 对公客户额外输出法人信息、注册资本、经营范围；对私客户输出性别、证件信息 |
| 交易统计 | 总金额、笔数、均值、最大值、首末交易日期 |
| 风险特征 | 夜间交易笔数、风险关键词、主要交易渠道、对手方样本 |
| 网络特征 | IP、IPv6、MAC 地址，整数金额交易信息 |

### 4. AI 研判
每条聚合后的案件数据作为独立 CSV 文件上传至 Dify，触发工作流后提取 `outputs.RES` 字段作为研判结果存库。并发数可通过 `TASK_CONCURRENCY` 配置。

---

## 目录结构

```
AML-daily-task/
├── main.py                        # 入口：初始化 DB、调度器、Flask
├── config/
│   └── settings.py                # 统一配置（读取环境变量）
├── models/
│   ├── task_config.py             # 任务配置表（含 cron 表达式）
│   └── dify_result.py             # Dify 调用结果表
├── scheduler/
│   └── task_scheduler.py          # APScheduler 封装
├── services/
│   ├── batch_api_service.py       # 核心：批量调用 Dify 工作流
│   ├── csv_processing_service.py  # CSV 聚合预处理
│   ├── download_unl_service.py    # UNL 文件下载
│   ├── task_service.py            # 任务 CRUD
│   └── unl_gz_to_csv.py           # UNL 格式转换工具
├── api/
│   └── task_api.py                # Flask REST API
├── utils/
│   └── csv_field_limit_handler.py # CSV 大字段自动扩容工具
├── scripts/                       # 测试数据生成脚本
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## 快速启动

### 方式一：Docker Compose（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/martin44779-minima/AML-daily-task.git
cd AML-daily-task

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env，填写 Dify API 地址和 KEY

# 3. 启动（含 PostgreSQL）
docker-compose up -d

# 4. 验证
curl http://localhost:5000/health
```

### 方式二：本地运行

```bash
# 1. 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/macOS

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env

# 4. 启动
python main.py
```

---

## 环境变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `DATABASE_URL` | 否 | `sqlite:///task_container.db` | 数据库连接串，支持 PostgreSQL / SQLite |
| `TASK_CONCURRENCY` | 否 | `3` | Dify 工作流并发调用数 |
| `CSV_PROCESSING_CHUNK_SIZE` | 否 | `50000` | CSV 分块处理行数 |
| `UNL_DOWNLOAD_URL` | 是 | - | UNL 文件下载接口地址 |
| `UNL_FILE_NAME_LIST` | 是 | - | 要下载的文件名，逗号分隔 |
| `UNL_FILE_SVR_ID` | 是 | - | 文件服务器 ID |
| `UNL_RMT_PUB_PATH` | 否 | - | 远程发布路径 |

任务配置通过数据库管理，`task_data` 字段（JSON）中需包含：

| 字段 | 说明 |
|------|------|
| `api_endpoint` | Dify API 地址，如 `http://dify-host/v1` |
| `API-KEY` | Dify 应用 API Key |
| `csv_file_path` | 数据文件路径或目录 |
| `max_workers` | 并发数（覆盖全局配置） |

---

## API 接口

服务启动后监听 `0.0.0.0:5000`。

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/health` | 健康检查 |
| `GET` | `/tasks/list` | 列出所有启用的任务 |
| `POST` | `/tasks/trigger/<task_id>` | 按 ID 手动触发任务 |
| `POST` | `/tasks/trigger_by_name/<task_name>` | 按名称手动触发任务 |
| `GET` | `/dify_result/<case_id>` | 按案件流水号查询 AI 研判结果 |
| `POST` | `/csv/preprocess` | 手动触发 CSV 预处理 |

**查询研判结果示例：**

```bash
curl http://localhost:5000/dify_result/20240101001
```

```json
{
  "case_id": "20240101001",
  "parsed_result": "经分析，该客户交易存在以下风险特征：...",
  "execution_time": "2024-01-01T02:15:30",
  "status": "completed"
}
```

**手动触发任务示例：**

```bash
curl -X POST http://localhost:5000/tasks/trigger_by_name/dify_tasks
```

---

## 数据说明

### 输入格式
原始数据为 Informix 数据库导出的 `.unl.gz` 文件，字段以 `\x07`（`^G`）分隔，包含案件编号、客户信息、交易明细等 40+ 个字段。

### 输出字段（聚合后）

**通用字段：** `case_id`、`main_cust_name`、`main_cust_id`、`total_trans_amt`、`trans_count`、`avg_trans_amt`、`night_trans_count`、`risk_keywords`、`model_name` 等

**对公客户额外字段：** `legal_name`（法定代表人）、`reg_fund_amount`（注册资本）、`biz_scope`（经营范围）、`faren_id_type/number`（法人证件）

**对私客户额外字段：** `main_cust_gender`（性别）、`id_type/number`（证件信息）

---

## 技术栈

- **Python 3.11+**
- **Flask** — REST API
- **APScheduler** — 定时任务调度
- **SQLAlchemy** — ORM，支持 PostgreSQL / SQLite
- **pandas** — 大文件分块聚合处理
- **Dify** — AI 工作流平台
- **Docker / Docker Compose** — 容器化部署
