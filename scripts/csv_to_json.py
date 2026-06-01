import csv
import json
import logging
from typing import List, Dict, Generator

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def csv_to_json_string(csv_file_path: str) -> str:
    """
    将CSV文件转换为JSON字符串，其中key是列名，value是CSV中的数值
    
    Args:
        csv_file_path: CSV文件路径
        
    Returns:
        JSON格式的字符串
    """
    # 定义列名
    column_names = [
        'case_id', 'stat_dt', 'main_cust_id', 'main_cust_name', 'main_CERT_TYPE',
        'main_CERT_No', 'main_PBC_OCP/INDUS', 'main_GENDER', 'main_CREATE_DT',
        'MODEL_ID', 'MODEL_NAME', 'fetr_id', 'FETR_NAME', 'CUST_ID', 'CUST_NAME',
        'ACCT_ID', 'TR_ID', 'TR_DT', 'TR_TM', 'TR_ORG_ID', 'CUST_TYPE',
        'CARD_NO', 'CARD_STYLE', 'TR_CHNL', 'S_TR_CHNL', 'TR_CD', 'S_TR_CD',
        'IS_CASH', 'DEBIT_CREDIT', 'RCV_PAY', 'CURR_CD', 'TR_AMT', 'TR_CNY_AMT',
        'TR_USD_AMT', 'TR_BAL_AMT', 'TR_COUNTRY', 'TR_AREA', 'FUND_USE',
        'OPP_NAME', 'OPP_ACCT_ID', 'OPP_ACCT_TYPE', 'OPP_IS_CUST', 'OPP_CUST_ID',
        'OPP_CUST_TYPE', 'OPP_CARD_NO', 'OPP_ORG_ID', 'OPP_ORG_NAME',
        'OPP_ORG_COUNTRY', 'OPP_ORG_AREA', 'TR_GO_COUNTRY', 'TR_GO_AREA',
        'TR_IPV6', 'IP', 'TR_MAC', 'RSRV_01', 'RSRV_04'
    ]
    
    # 尝试不同的编码格式
    encodings = ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']
    data_list = []
    
    for encoding in encodings:
        try:
            with open(csv_file_path, 'r', encoding=encoding) as csv_file:
                csv_reader = csv.reader(csv_file)
                
                for row in csv_reader:
                    # 创建字典，将列名与数据对应
                    row_dict = {}
                    for i, column_name in enumerate(column_names):
                        if i < len(row):
                            row_dict[column_name] = row[i]
                        else:
                            row_dict[column_name] = ""  # 如果数据不足，使用空字符串填充
                    
                    data_list.append(row_dict)
                break  # 成功读取，跳出编码尝试循环
        except UnicodeDecodeError:
            data_list = []  # 重置数据列表，尝试下一种编码
            continue
    
    if not data_list:  # 如果data_list为空，说明所有编码尝试都失败了
        # 如果常见编码都失败，尝试二进制模式检测编码
        try:
            import chardet
            with open(csv_file_path, 'rb') as f:
                raw_data = f.read()
                detected = chardet.detect(raw_data)
                encoding = detected['encoding']
                with open(csv_file_path, 'r', encoding=encoding) as csv_file:
                    csv_reader = csv.reader(csv_file)
                    
                    for row in csv_reader:
                        # 创建字典，将列名与数据对应
                        row_dict = {}
                        for i, column_name in enumerate(column_names):
                            if i < len(row):
                                row_dict[column_name] = row[i]
                            else:
                                row_dict[column_name] = ""  # 如果数据不足，使用空字符串填充
                        
                        data_list.append(row_dict)
        except ImportError:
            raise ValueError(f"无法使用常见编码格式读取文件 {csv_file_path}，且未安装chardet库进行编码检测")
    
    # 转换为JSON字符串
    json_string = json.dumps(data_list, ensure_ascii=False, indent=2)
    return json_string


def csv_to_json_generator(csv_file_path: str) -> Generator[Dict, None, None]:
    """
    将CSV文件逐行转换为JSON对象的生成器，适用于大文件
    
    Args:
        csv_file_path: CSV文件路径
        
    Yields:
        每行数据的字典表示
    """
    # 定义列名
    column_names = [
        'case_id', 'stat_dt', 'main_cust_id', 'main_cust_name', 'main_CERT_TYPE',
        'main_CERT_No', 'main_PBC_OCP/INDUS', 'main_GENDER', 'main_CREATE_DT',
        'MODEL_ID', 'MODEL_NAME', 'fetr_id', 'FETR_NAME', 'CUST_ID', 'CUST_NAME',
        'ACCT_ID', 'TR_ID', 'TR_DT', 'TR_TM', 'TR_ORG_ID', 'CUST_TYPE',
        'CARD_NO', 'CARD_STYLE', 'TR_CHNL', 'S_TR_CHNL', 'TR_CD', 'S_TR_CD',
        'IS_CASH', 'DEBIT_CREDIT', 'RCV_PAY', 'CURR_CD', 'TR_AMT', 'TR_CNY_AMT',
        'TR_USD_AMT', 'TR_BAL_AMT', 'TR_COUNTRY', 'TR_AREA', 'FUND_USE',
        'OPP_NAME', 'OPP_ACCT_ID', 'OPP_ACCT_TYPE', 'OPP_IS_CUST', 'OPP_CUST_ID',
        'OPP_CUST_TYPE', 'OPP_CARD_NO', 'OPP_ORG_ID', 'OPP_ORG_NAME',
        'OPP_ORG_COUNTRY', 'OPP_ORG_AREA', 'TR_GO_COUNTRY', 'TR_GO_AREA',
        'TR_IPV6', 'IP', 'TR_MAC', 'RSRV_01', 'RSRV_04'
    ]
    
    # 尝试不同的编码格式
    encodings = ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']
    
    for encoding in encodings:
        try:
            with open(csv_file_path, 'r', encoding=encoding) as csv_file:
                csv_reader = csv.reader(csv_file)
                
                for row in csv_reader:
                    # 创建字典，将列名与数据对应
                    row_dict = {}
                    for i, column_name in enumerate(column_names):
                        if i < len(row):
                            row_dict[column_name] = row[i]
                        else:
                            row_dict[column_name] = ""  # 如果数据不足，使用空字符串填充
                    
                    yield row_dict
                return  # 成功读取，结束函数
        except UnicodeDecodeError:
            continue  # 尝试下一种编码
    
    # 如果常见编码都失败
    try:
        import chardet
        with open(csv_file_path, 'rb') as f:
            raw_data = f.read()
            detected = chardet.detect(raw_data)
            encoding = detected['encoding']
            with open(csv_file_path, 'r', encoding=encoding) as csv_file:
                csv_reader = csv.reader(csv_file)
                
                for row in csv_reader:
                    # 创建字典，将列名与数据对应
                    row_dict = {}
                    for i, column_name in enumerate(column_names):
                        if i < len(row):
                            row_dict[column_name] = row[i]
                        else:
                            row_dict[column_name] = ""  # 如果数据不足，使用空字符串填充
                    
                    yield row_dict
    except ImportError:
        raise ValueError(f"无法使用常见编码格式读取文件 {csv_file_path}，且未安装chardet库进行编码检测")


def csv_to_json_file(csv_file_path: str, output_file_path: str = None) -> str:
    """
    将CSV文件转换为JSON格式并保存到文件
    
    Args:
        csv_file_path: 输入的CSV文件路径
        output_file_path: 输出的JSON文件路径，如果为None则使用CSV文件名+json扩展名
        
    Returns:
        输出文件的路径
    """
    import os
    
    if output_file_path is None:
        base_name = os.path.splitext(csv_file_path)[0]
        output_file_path = f"{base_name}.json"
    
    json_string = csv_to_json_string(csv_file_path)
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_file_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    with open(output_file_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_string)
    
    logger.info(f"CSV文件已成功转换为JSON格式，保存至: {output_file_path}")
    return output_file_path


def dify_csv_to_json(csv_content: str = None, csv_file_path: str = None) -> dict:
    """
    专为Dify脚本执行节点设计的CSV转JSON函数
    可以处理直接传入的CSV内容字符串或文件路径
    
    Args:
        csv_content: CSV内容字符串（可选）
        csv_file_path: CSV文件路径（可选）
        
    Returns:
        包含转换结果的字典
    """
    # 定义列名
    column_names = [
        'case_id', 'stat_dt', 'main_cust_id', 'main_cust_name', 'main_CERT_TYPE',
        'main_CERT_No', 'main_PBC_OCP/INDUS', 'main_GENDER', 'main_CREATE_DT',
        'MODEL_ID', 'MODEL_NAME', 'fetr_id', 'FETR_NAME', 'CUST_ID', 'CUST_NAME',
        'ACCT_ID', 'TR_ID', 'TR_DT', 'TR_TM', 'TR_ORG_ID', 'CUST_TYPE',
        'CARD_NO', 'CARD_STYLE', 'TR_CHNL', 'S_TR_CHNL', 'TR_CD', 'S_TR_CD',
        'IS_CASH', 'DEBIT_CREDIT', 'RCV_PAY', 'CURR_CD', 'TR_AMT', 'TR_CNY_AMT',
        'TR_USD_AMT', 'TR_BAL_AMT', 'TR_COUNTRY', 'TR_AREA', 'FUND_USE',
        'OPP_NAME', 'OPP_ACCT_ID', 'OPP_ACCT_TYPE', 'OPP_IS_CUST', 'OPP_CUST_ID',
        'OPP_CUST_TYPE', 'OPP_CARD_NO', 'OPP_ORG_ID', 'OPP_ORG_NAME',
        'OPP_ORG_COUNTRY', 'OPP_ORG_AREA', 'TR_GO_COUNTRY', 'TR_GO_AREA',
        'TR_IPV6', 'IP', 'TR_MAC', 'RSRV_01', 'RSRV_04'
    ]
    
    data_list = []
    
    if csv_content:
        # 处理直接传入的CSV内容
        import io
        csv_file = io.StringIO(csv_content)
        csv_reader = csv.reader(csv_file)
        
        for row_num, row in enumerate(csv_reader):
            row_dict = {}
            for i, column_name in enumerate(column_names):
                if i < len(row):
                    row_dict[column_name] = row[i]
                else:
                    row_dict[column_name] = ""  # 如果数据不足，使用空字符串填充
            
            # 记录交易流水号（第五列）
            transaction_id = row[4] if len(row) > 4 else "N/A"
            logger.info(f"处理CSV行 {row_num + 1}, 交易流水号: {transaction_id}")
            
            data_list.append(row_dict)
    
    elif csv_file_path:
        # 处理文件路径
        encodings = ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']
        
        for encoding in encodings:
            try:
                with open(csv_file_path, 'r', encoding=encoding) as csv_file:
                    csv_reader = csv.reader(csv_file)
                    
                    for row_num, row in enumerate(csv_reader):
                        row_dict = {}
                        for i, column_name in enumerate(column_names):
                            if i < len(row):
                                row_dict[column_name] = row[i]
                            else:
                                row_dict[column_name] = ""  # 如果数据不足，使用空字符串填充
                        
                        # 记录交易流水号（第五列）
                        transaction_id = row[4] if len(row) > 4 else "N/A"
                        logger.info(f"处理CSV行 {row_num + 1}, 交易流水号: {transaction_id}")
                        
                        data_list.append(row_dict)
                    break  # 成功读取，跳出编码尝试循环
            except UnicodeDecodeError:
                data_list = []  # 重置数据列表，尝试下一种编码
                continue
        
        if not data_list:  # 如果data_list为空，说明所有编码尝试都失败了
            # 如果常见编码都失败，尝试二进制模式检测编码
            try:
                import chardet
                with open(csv_file_path, 'rb') as f:
                    raw_data = f.read()
                    detected = chardet.detect(raw_data)
                    encoding = detected['encoding']
                    with open(csv_file_path, 'r', encoding=encoding) as csv_file:
                        csv_reader = csv.reader(csv_file)
                        
                        for row_num, row in enumerate(csv_reader):
                            row_dict = {}
                            for i, column_name in enumerate(column_names):
                                if i < len(row):
                                    row_dict[column_name] = row[i]
                                else:
                                    row_dict[column_name] = ""  # 如果数据不足，使用空字符串填充
                            
                            # 记录交易流水号（第五列）
                            transaction_id = row[4] if len(row) > 4 else "N/A"
                            logger.info(f"处理CSV行 {row_num + 1}, 交易流水号: {transaction_id}")
                            
                            data_list.append(row_dict)
            except ImportError:
                return {
                    "error": f"无法使用常见编码格式读取文件 {csv_file_path}，且未安装chardet库进行编码检测",
                    "success": False
                }
    else:
        return {
            "error": "必须提供csv_content或csv_file_path参数之一",
            "success": False
        }
    
    # 转换为JSON字符串
    try:
        json_string = json.dumps(data_list, ensure_ascii=False, indent=2)
        return {
            "json_data": json_string,
            "data_list": data_list,
            "record_count": len(data_list),
            "success": True
        }
    except Exception as e:
        return {
            "error": f"JSON转换失败: {str(e)}",
            "success": False
        }


# 用于测试的变量
CSV_FILE_PATH = r"D:\AML_daily_task\scripts\111\构建测试一条.csv"  # CSV文件路径
OUTPUT_JSON_PATH = r"D:\AML_daily_task\scripts\111\111.json"  # 输出JSON文件路径


def test_csv_to_json():
    """
    测试函数，使用预设的变量进行测试
    """
    logger.info(f"开始测试CSV转JSON功能")
    logger.info(f"CSV文件路径: {CSV_FILE_PATH}")
    logger.info(f"输出JSON路径: {OUTPUT_JSON_PATH}")
    
    try:
        # 测试文件转换功能
        result = csv_to_json_file(CSV_FILE_PATH, OUTPUT_JSON_PATH)
        logger.info(f"文件转换成功: {result}")
        
        # 测试字符串转换功能
        json_str = csv_to_json_string(CSV_FILE_PATH)
        data_list = json.loads(json_str)
        logger.info(f"转换完成，共处理 {len(data_list)} 条记录")
        logger.info("前3条记录预览:")
        for i, item in enumerate(data_list[:3]):
            transaction_id = item.get('main_CERT_No', 'N/A')  # 使用第6列作为交易流水号示例
            logger.info(f"第{i+1}条: {item}")
            logger.info(f"  - 交易流水号: {transaction_id}")
        
        # 测试生成器函数
        logger.info("测试生成器函数:")
        count = 0
        for row_data in csv_to_json_generator(CSV_FILE_PATH):
            if count < 3:  # 只显示前3条
                logger.info(f"生成器第{count + 1}条: {row_data}")
            count += 1
        logger.info(f"生成器处理完成，共处理 {count} 条记录")
        
        # 测试Dify函数
        dify_result = dify_csv_to_json(csv_file_path=CSV_FILE_PATH)
        if dify_result['success']:
            logger.info(f"Dify函数测试成功，处理了 {dify_result['record_count']} 条记录")
        else:
            logger.error(f"Dify函数测试失败: {dify_result['error']}")
            
        return True
    except FileNotFoundError:
        logger.error(f"找不到CSV文件: {CSV_FILE_PATH}")
        return False
    except Exception as e:
        logger.error(f"测试过程中发生错误: {str(e)}")
        return False


if __name__ == "__main__":
    # 运行测试
    success = test_csv_to_json()
    if success:
        logger.info("测试完成")
    else:
        logger.error("测试失败")