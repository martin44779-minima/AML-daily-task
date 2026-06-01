# CSV to UNL.GZ 转换工具使用说明

## 功能描述
此工具将CSV文件转换为UNL格式，并使用gzip压缩为.UNL.GZ文件。字段之间使用`\x07`（ASCII字符7，即Bell字符）作为分隔符。

## 脚本位置
`D:\AML_daily_task\scripts\csv_to_unl_gz.py`

## 使用方法

### 1. 命令行使用

#### 基本用法：
```bash
python scripts/csv_to_unl_gz.py /path/to/input.csv
```
这将在相同目录下生成名为 `input.unl.gz` 的文件。

#### 指定输出路径：
```bash
python scripts/csv_to_unl_gz.py /path/to/input.csv -o /path/to/output/custom_name.unl.gz
```

#### 仅生成UNL文件（不压缩）：
```bash
python scripts/csv_to_unl_gz.py /path/to/input.csv --unl-only
```

#### 指定输出路径且仅生成UNL文件：
```bash
python scripts/csv_to_unl_gz.py /path/to/input.csv --unl-only -o /path/to/output/custom_name.unl
```

### 2. 作为模块导入使用

```python
from scripts.csv_to_unl_gz import csv_to_unl_gz, csv_to_unl

# 转换为压缩的UNL.GZ文件
result_path = csv_to_unl_gz('/path/to/input.csv')
print(f'Generated: {result_path}')

# 或者指定输出路径
result_path = csv_to_unl_gz('/path/to/input.csv', '/custom/output/path/file.unl.gz')

# 仅生成UNL文件（不压缩）
result_path = csv_to_unl('/path/to/input.csv')
```

## 技术细节

- **分隔符**: 使用 `\x07` (ASCII 7, Bell字符) 作为字段分隔符
- **编码**: 输入和输出均使用 UTF-8 编码
- **行结束符**: 每行末尾使用 `\n` (LF)
- **压缩格式**: 使用 gzip 格式压缩

## 示例

假设有一个CSV文件 `data.csv` 内容如下：
```
Name,Age,City
John,25,New York
Jane,30,San Francisco
```

转换后的UNL格式内容将是：
```
Name\x07Age\x07City
John\x0725\x07New York
Jane\x0730\x07San Francisco
```

然后被压缩为 `.unl.gz` 文件。

## 注意事项

1. 脚本会自动创建输出目录（如果不存在）
2. 如果输出路径未指定，将使用输入文件路径并替换扩展名为 `.unl.gz`
3. 支持各种编码格式的CSV文件（优先使用UTF-8）
4. 大文件处理时会占用相应内存，注意系统资源