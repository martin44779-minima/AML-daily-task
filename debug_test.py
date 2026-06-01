import pandas as pd
import tempfile
import os
from services.csv_processing_service import CSVProcessingService

# 创建测试数据
test_data = """案例编号,主客户名称,原币种交易金额,交易日期和时间
CASE001,测试客户1,1000.0,2024-01-01 10:00:00
CASE001,测试客户1,500.0,2024-01-01 11:00:00
CASE002,测试客户2,200.0,2024-01-02 15:30:00"""

# 创建临时文件
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8') as f:
    f.write(test_data)
    input_file = f.name

output_file = tempfile.mktemp(suffix='.csv')

try:
    service = CSVProcessingService()
    print("服务创建成功")
    
    result = service.preprocess_csv(input_file, output_file)
    print(f"处理结果: {result}")
    
except Exception as e:
    print(f"错误: {str(e)}")
    import traceback
    traceback.print_exc()

# 清理
if os.path.exists(input_file):
    os.unlink(input_file)
if os.path.exists(output_file):
    os.unlink(output_file)