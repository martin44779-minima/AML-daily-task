import pandas as pd
import tempfile
import os
from services.csv_processing_service import CSVProcessingService

# 创建完整的测试数据，包含所有必需的列
test_data = """案例编号,数据日期,主客户编号,主客户名称,主客户职业行业,主客户性别,主客户开户日期,对公对私标志,可疑模型编号,可疑模型名称,可疑特征规则编号,可疑特征规则特征名称,模型平台最高分数,机器学习匹配规则前10特征序号,机器学习匹配规则前10特征说明,机器学习匹配规则前10特征风险值,可疑案例下所有客户号,可疑案例下所有客户名称,可疑案例下所有账号,交易主键,交易日期,交易日期和时间,交易机构,客户类型,卡号折号,卡片类型,am1交易渠道,源系统交易渠道,am1交易代码,源系统交易代码,现转标志,借贷标志,收付标志,币种,原币种交易金额,折人民币交易金额,折美元交易金额,交易余额,交易发生国家,交易发生地区,资金用途和来源,对方名称,对方账号,对手PBC账户类型,对方是否我行客户,对方客户编号,对方客户类型,对方卡号折号,对方金融机构编号,对方金融机构名称,对方金融机构网点国家,对方金融机构网点地区,交易IPV6地址,IP地址,交易MAC地址,摘要码,交易备注
CASE001,2024-01-01,CUST001,测试客户1,IT行业,男,2020-01-01,I,MOD001,测试模型1,RULE001,测试规则1,95.5,1,特征1,85.2,CUST001,测试客户1,ACC001,TRX001,2024-01-01,2024-01-01 10:00:00,机构1,个人,CARD001,借记卡,ATM,ATM,1001,1001,现,借,付,CNY,1000.0,1000.0,140.0,5000.0,中国,北京,普通转账,收款方1,ACC002,储蓄账户,是,CUST002,个人,CARD002,FIN001,银行1,中国,北京,::1,192.168.1.1,AA:BB:CC:DD:EE:FF,001,测试备注
CASE001,2024-01-01,CUST001,测试客户1,IT行业,男,2020-01-01,I,MOD001,测试模型1,RULE001,测试规则1,95.5,2,特征2,78.9,CUST001,测试客户1,ACC001,TRX002,2024-01-01,2024-01-01 11:00:00,机构1,个人,CARD001,借记卡,ATM,ATM,1001,1001,现,借,付,CNY,500.0,500.0,70.0,4500.0,中国,北京,普通转账,收款方2,ACC003,储蓄账户,是,CUST003,个人,CARD003,FIN001,银行1,中国,北京,::1,192.168.1.1,AA:BB:CC:DD:EE:FF,001,测试备注
CASE002,2024-01-02,CUST002,测试客户2,金融行业,女,2019-06-01,I,MOD002,测试模型2,RULE002,测试规则2,88.3,1,特征3,92.1,CUST002,测试客户2,ACC002,TRX003,2024-01-02,2024-01-02 15:30:00,机构2,企业,CARD002,贷记卡,网银,网银,2001,2001,转,贷,收,USD,200.0,1400.0,200.0,10000.0,美国,纽约,跨境汇款,境外公司,ACC004,对公账户,否,,企业,,FIN002,外资银行,美国,纽约,,10.0.0.1,BB:CC:DD:EE:FF:00,002,国际汇款"""

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
    
    if result['success']:
        print("✓ 处理成功!")
        # 显示输出文件内容
        if os.path.exists(output_file):
            df = pd.read_csv(output_file, header=None)
            print(f"输出数据形状: {df.shape}")
            print("前几行数据:")
            print(df.head())
    else:
        print("✗ 处理失败")
        
except Exception as e:
    print(f"错误: {str(e)}")
    import traceback
    traceback.print_exc()

# 清理
if os.path.exists(input_file):
    os.unlink(input_file)
if os.path.exists(output_file):
    os.unlink(output_file)