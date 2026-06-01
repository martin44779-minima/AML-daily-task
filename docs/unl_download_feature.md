# UNL文件下载功能说明

## 功能概述
本功能允许在定时任务开始执行之前，自动调用一个POST接口下载`.unl.gz`文件。该功能通过环境变量配置接口参数，确保灵活性和安全性。

## 环境变量配置

在 `.env` 文件中添加以下配置项：

```bash
# UNL文件下载配置
UNL_DOWNLOAD_URL=http://your-api-endpoint.com/api/download  # 下载接口的URL
UNL_FILE_NAME_LIST=file1.unl.gz,file2.unl.gz              # 要下载的文件名列表，逗号分隔
UNL_FILE_SVR_ID=server123                                  # 文件服务器ID
UNL_RMT_PUB_PATH=/public/path                             # 远程发布路径
```

## 配置项说明

- `UNL_DOWNLOAD_URL`: 目标API接口的完整URL
- `UNL_FILE_NAME_LIST`: 需要下载的文件名列表，多个文件名用逗号分隔
- `UNL_FILE_SVR_ID`: 文件服务器标识符
- `UNL_RMT_PUB_PATH`: 远程发布路径

## 请求格式

服务会向配置的URL发送POST请求，请求体格式如下：

```json
{
  "fileNameList": ["file1.unl.gz", "file2.unl.gz"],
  "fileSvrId": "server123",
  "rmtPubPath": "/public/path"
}
```

## 实现细节

1. 在每次定时任务执行前，系统会自动调用下载服务
2. 下载的文件会被保存到临时目录中
3. 如果下载失败，任务将继续执行（非阻塞模式）
4. 服务遵循定时任务数据库操作安全模式，使用独立的数据库连接

## 服务位置

- 服务类: `services/download_unl_service.py`
- 主要方法: `DownloadUnlService.download_unl_files()`
- 集成位置: `scheduler/task_scheduler.py` 中的 `execute_task_function`

## 注意事项

1. 确保网络连通性，能够访问配置的下载URL
2. 验证接口参数格式是否符合目标API要求
3. 监控磁盘空间，因为下载的文件会占用临时存储空间
4. 如果下载失败，任务仍会继续执行，需关注日志中的警告信息
5. 系统会优先处理名为 t3b_case_aml_llmp.unl.gz 或 T3B_CASE_AML_LLMP.unl.gz 的特定UNL文件
6. 只有匹配特定名称的UNL文件才会被执行后续处理逻辑
7. 系统会自动跳过所有CSV文件，仅处理目标UNL文件