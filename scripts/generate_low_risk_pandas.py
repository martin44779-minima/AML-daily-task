#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用pandas正确生成CSV格式的低风险数据
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import json
from typing import List, Dict, Any
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_low_risk_dataframe(num_cases: int = 5) -> pd.DataFrame:
    """生成低风险数据DataFrame"""
    
    # 正常客户模板
    normal_customers = [
        {
            'name': '李明',
            'industry': '金融服务',
            'gender': '男',
            'address': '上海市浦东新区陆家嘴环路1000号',
            'phone': '13900139000'
        },
        {
            'name': '王芳',
            'industry': '教育行业',
            'gender': '女',
            'address': '北京市海淀区中关村大街1号',
            'phone': '13800138001'
        },
        {
            'name': '张伟',
            'industry': '医疗健康',
            'gender': '男',
            'address': '广州市越秀区中山一路200号',
            'phone': '13700137001'
        },
        {
            'name': '刘敏',
            'industry': '文化传媒',
            'gender': '女',
            'address': '深圳市福田区深南大道1001号',
            'phone': '13600136001'
        },
        {
            'name': '陈强',
            'industry': '科学研究',
            'gender': '男',
            'address': '杭州市西湖区文三路300号',
            'phone': '13500135001'
        }
    ]
    
    # 准备数据列表
    data_rows = []
    
    for i in range(num_cases):
        customer = normal_customers[i % len(normal_customers)]
        
        # 生成案例数据
        case_id = f"case{i+2:03d}"
        customer_name = customer['name']
        customer_id = f"CUST{1000 + i:06d}"
        industry = customer['industry']
        gender = customer['gender']
        open_date = (datetime.now() - timedelta(days=random.randint(365, 1825))).strftime('%Y-%m-%d')
        address = customer['address']
        phone = customer['phone']
        id_type = '居民身份证'
        id_number = f"{random.randint(110000, 659000)}19{random.randint(85, 99)}{random.randint(1, 12):02d}{random.randint(1, 28):02d}{random.randint(1000, 9999)}"
        
        # 交易统计数据
        transaction_count = random.randint(50, 200)
        avg_amount = round(random.uniform(2000, 15000), 2)
        total_amount = round(avg_amount * transaction_count, 2)
        max_amount = round(random.uniform(10000, 100000), 2)
        
        # 时间信息
        first_trans_date = (datetime.now() - timedelta(days=random.randint(30, 90))).strftime('%Y-%m-%d')
        last_trans_date = datetime.now().strftime('%Y-%m-%d')
        report_start = (datetime.strptime(first_trans_date, '%Y-%m-%d') - timedelta(days=7)).strftime('%Y年%m月%d日')
        report_end = datetime.now().strftime('%Y年%m月%d日')
        
        # 正常行为特征
        night_trans_count = random.randint(0, 5)
        risk_keywords = "正常交易"
        
        # 交易对手和渠道
        counterparties = ['工商银行', '建设银行', '农业银行', '中国银行', '招商银行']
        counterparty_sample = ';'.join(random.sample(counterparties, min(3, len(counterparties))))
        
        regions = ['北京', '上海', '广州', '深圳', '杭州']
        top_opposing_areas = ';'.join(random.sample(regions, min(3, len(regions))))
        
        channels = ['网上银行', '手机银行', 'ATM', '柜台']
        main_tnx_channels = ';'.join(random.sample(channels, min(2, len(channels))))
        
        # 生成交易样本（6笔固定）
        transaction_samples = []
        base_date = datetime.now() - timedelta(days=30)
        for j in range(6):
            trans_datetime = base_date + timedelta(days=j*5, hours=random.randint(9, 17), minutes=random.randint(0, 59))
            transaction = {
                'TR_DT': trans_datetime.strftime('%Y-%m-%d'),
                'TR_TM': trans_datetime.strftime('%H:%M'),
                'TR_AMT': round(random.uniform(1000, 50000), 2),
                'CURR_CD': 'CNY',
                'OPP_NAME': random.choice(counterparties),
                'FUND_USE': random.choice(['工资收入', '商品购买', '生活消费', '投资收益', '转账汇款']),
                'TR_CHNL': random.choice(channels),
                'TR_AREA': random.choice(regions),
                'SRC_CHNL': random.choice(channels),
                'TR_ORG': random.choice(counterparties),
                'REMARK': f'正常交易备注{j+1}'
            }
            transaction_samples.append(transaction)
        
        sample_trx_list = json.dumps(transaction_samples, ensure_ascii=False)
        
        # 财务统计
        debit_count = random.randint(int(transaction_count * 0.4), int(transaction_count * 0.6))
        debit_amount = round(total_amount * random.uniform(0.4, 0.6), 2)
        credit_count = transaction_count - debit_count
        credit_amount = round(total_amount - debit_amount, 2)
        
        # 模型信息
        model_name = "正常交易模型"
        is_gambling_suspected = "否"
        transaction_org = random.choice(counterparties)
        
        # 特征信息
        features_json = json.dumps([{
            'serial_num': '1',
            'features': '正常交易特征',
            'feature_value': f"{random.uniform(0.05, 0.3):.4f}",
            'highest_score': f"{random.uniform(15, 35):.2f}"
        }], ensure_ascii=False)
        
        highest_score = random.uniform(15, 35)
        
        # 网络信息
        ipv6_addresses = ';'.join([f"2001:db8::{random.randint(1000, 9999)}:{random.randint(1000, 9999)}" 
                                  for _ in range(random.randint(2, 4))])
        ip_addresses = ';'.join([f"192.168.1.{random.randint(100, 103)}" for _ in range(random.randint(2, 4))])
        mac_addresses = ';'.join(['00:1A:2B:3C:4D:5E', 'AA:BB:CC:DD:EE:FF'][:random.randint(2, 3)])
        
        # 构造行数据
        row_data = {
            'case_id': case_id,
            'main_cust_name': customer_name,
            'main_cust_id': customer_id,
            'main_cust_industry': industry,
            'main_cust_gender': gender,
            'main_cust_open_date': open_date,
            'main_cust_addr': address,
            'main_cust_phone_number': phone,
            'id_type': id_type,
            'id_number': id_number,
            'total_trans_amt': total_amount,
            'trans_count': transaction_count,
            'avg_trans_amt': avg_amount,
            'max_trans_amt': max_amount,
            'first_trans_date': first_trans_date,
            'last_trans_date': last_trans_date,
            'report_start_date': report_start,
            'report_end_date': report_end,
            'night_trans_count': night_trans_count,
            'risk_keywords': risk_keywords,
            'counterparty_sample': counterparty_sample,
            'top_opposing_areas': top_opposing_areas,
            'main_tnx_channels': main_tnx_channels,
            'sample_trx_list': sample_trx_list,
            'debit_count': debit_count,
            'debit_amt': debit_amount,
            'credit_count': credit_count,
            'credit_amt': credit_amount,
            'model_name': model_name,
            'is_network_gambling_suspected': is_gambling_suspected,
            'tr_org': transaction_org,
            'features_json': features_json,
            'highest_score': round(highest_score, 2),
            'ipv6_addr': ipv6_addresses,
            'ip_addr': ip_addresses,
            'mac_addr': mac_addresses
        }
        
        data_rows.append(row_data)
        logger.info(f"已生成低风险案例: {case_id}")
    
    # 创建DataFrame
    df = pd.DataFrame(data_rows)
    return df

def main():
    """主函数"""
    # 生成数据
    df = generate_low_risk_dataframe(5)
    
    # 保存为CSV（使用正确的编码和格式）
    output_file = 'D:/AML_daily_task/demo低风险标准格式.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    logger.info(f"低风险数据已保存到: {output_file}")
    logger.info(f"数据形状: {df.shape}")
    logger.info(f"列名: {list(df.columns)}")
    
    # 验证生成的数据
    try:
        df_verify = pd.read_csv(output_file)
        logger.info(f"✓ 验证成功，读取到 {len(df_verify)} 行，{len(df_verify.columns)} 列")
    except Exception as e:
        logger.error(f"✗ 验证失败: {e}")

if __name__ == "__main__":
    main()