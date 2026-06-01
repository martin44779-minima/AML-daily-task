# CSV数据预处理服务

## 概述

CSV数据预处理服务是一个专门用于在获取原始CSV文件和上传CSV文件之间进行数据处理的服务。该服务主要负责将原始交易级CSV按案例编号聚合为案例级CSV，用于反洗钱（AML）系统的数据处理流程。

## 功能特性

- **数据聚合**: 将原始交易数据按案例编号进行聚合
- **风险识别**: 自动识别小额、高频、夜间、匿名等风险交易特征
- **数据清洗**: 过滤低价值交易（如手续费、系统费等）
- **样本提取**: 提取关键交易样本（前3笔+后3笔）
- **API接口**: 提供RESTful API接口供外部系统调用

## 文件结构

```
services/
├── csv_processing_service.py    # 主要的CSV处理服务
api/
└── task_api.py                 # 包含CSV预处理API接口
docs/
└── CSV_PREPROCESSING_SERVICE.md # 本文档
```

## 核心功能

### 1. 数据聚合逻辑

- 按案例编号([case_id](file:///D:/AML_daily_task/services/batch_api_service.py#L218-L218))分组
- 计算总交易金额、交易次数、平均交易金额等统计指标
- 识别夜间交易（23点-6点）
- 生成风险关键词标签

### 2. 风险检测规则

- **小额交易**: 平均交易金额 ≤ 10元
- **高频交易**: 交易次数 ≥ 50次
- **夜间交易**: 夜间交易占比 > 80%
- **匿名交易**: 对方名称缺失率 > 50%
- **可疑用途**: 包含"充值"、"返现"、"游戏"、"彩票"等关键词

### 3. 输出字段

处理后的CSV文件包含以下29个字段：

| 字段名 | 描述 |
|--------|------|
| case_id | 案例编号 |
| main_cust_name | 主客户名称 |
| main_cust_id | 主客户编号 |
| main_cust_industry | 主客户职业行业 |
| main_cust_gender | 主客户性别 |
| main_cust_open_date | 主客户开户日期 |
| id_type | 证件类型 |
| id_number | 证件号 |
| total_trans_amt | 总交易金额 |
| trans_count | 交易次数 |
| avg_trans_amt | 平均交易金额 |
| max_trans_amt | 最大交易金额 |
| first_trans_date | 首次交易日期 |
| last_trans_date | 最后交易日期 |
| report_start_date | 报告起始日期 |
| report_end_date | 报告结束日期 |
| night_trans_count | 夜间交易次数 |
| risk_keywords | 风险关键词 |
| counterparty_sample | 交易对手样本 |
| top_opposing_areas | 主要交易地区 |
| main_tnx_channels | 主要交易渠道 |
| sample_trx_list | 交易样本列表 |
| debit_count | 借方交易次数 |
| debit_amt | 借方交易金额 |
| credit_count | 贷方交易次数 |
| credit_amt | 贷方交易金额 |
| model_name | 模型名称 |
| is_network_gambling_suspected | 是否疑似网络赌博 |
| tr_org | 交易机构 |

## API接口

### CSV预处理接口

**端点**: `POST /csv/preprocess`

#### 请求参数

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| input_file_path | String | 否 | 输入CSV文件路径（与csv_content二选一） |
| csv_content | String | 否 | CSV内容字符串（与input_file_path二选一） |
| output_file_path | String | 否 | 输出CSV文件路径（不提供则生成临时文件） |

#### 请求示例

```json
{
    "input_file_path": "/path/to/input.csv",
    "output_file_path": "/path/to/output.csv"
}
```

或

```json
{
    "csv_content": "案例编号,数据日期,主客户编号,...\nCASE001,2023-01-01,CUST001,...",
    "output_file_path": "/path/to/output.csv"
}
```

#### 响应参数

| 参数 | 类型 | 描述 |
|------|------|------|
| success | Boolean | 处理是否成功 |
| message | String | 处理结果消息 |
| processed_count | Integer | 处理的案例数量 |
| output_file | String | 输出文件路径 |

#### 响应示例

```json
{
    "success": true,
    "message": "预处理完成，共处理 1 个案例",
    "processed_count": 1,
    "output_file": "/path/to/output.csv"
}
```

## 使用方法

### 1. 直接调用服务

```python
from services.csv_processing_service import CSVProcessingService

service = CSVProcessingService()
result = service.preprocess_csv("input.csv", "output.csv")
print(result)
```

### 2. 调用Dify兼容函数

```python
from services.csv_processing_service import process_csv_for_dify

result = process_csv_for_dify(
    csv_file_path="input.csv",
    output_path="output.csv"
)
print(result)
```

### 3. 通过API调用

```bash
curl -X POST http://localhost:5000/csv/preprocess \
  -H "Content-Type: application/json" \
  -d '{
    "input_file_path": "/path/to/input.csv",
    "output_file_path": "/path/to/output.csv"
  }'
```

## 集成到Dify

该服务特别适合集成到Dify等低代码平台中，通过`process_csv_for_dify`函数可以方便地在Dify工作流中调用CSV预处理功能。

## 注意事项

1. 输入CSV文件应按照预定的列顺序排列（无需列名）
2. 必须包含以下关键字段：案例编号、主客户名称、交易金额、交易时间
3. 服务会自动处理中文编码问题
4. 大文件处理时请注意内存使用情况