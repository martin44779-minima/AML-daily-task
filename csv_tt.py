from services.csv_processing_service import CSVProcessingService

# 创建服务实例
service = CSVProcessingService()

# 测试健壮性 - 使用包含各种边界情况的测试文件
result = service.preprocess_csv('test_robustness.csv', 'output_robustness_test.csv')
print("健壮性测试结果:", result)


# 使用较小的chunk size来更好测试分块处理功能
service = CSVProcessingService(chunk_size=10000)  # 1万行一个块

# 测试大文件处理 - 使用生成的5万行数据文件
# result = service.preprocess_csv('large_test_data_250w.csv', 'output_large_file_test.csv')
# print("大文件处理测试结果:", result)

expected_columns = [
    'case_id', 'main_cust_name', 'main_cust_id', 'main_cust_industry',
    'main_cust_gender', 'main_cust_open_date', 'main_cust_addr', 'main_cust_phone_number', 'id_type', 'id_number',
    'total_trans_amt', 'trans_count', 'avg_trans_amt',
    'max_trans_amt', 'first_trans_date', 'last_trans_date',
    'report_start_date', 'report_end_date', 'night_trans_count',
    'risk_keywords', 'counterparty_sample', 'top_opposing_areas',
    'main_tnx_channels', 'sample_trx_list', 'debit_count',
    'debit_amt', 'credit_count', 'credit_amt',
    'model_name', 'is_network_gambling_suspected', 'tr_org', 'features', 'highest_score'
]

import time
c = time.now()
print(len(expected_columns))