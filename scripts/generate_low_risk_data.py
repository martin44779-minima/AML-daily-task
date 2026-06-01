#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成低风险、正常交易的聚合数据
基于demo高风险.csv的格式，生成符合正常交易行为的测试数据
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

class LowRiskDataGenerator:
    """低风险正常交易数据生成器"""
    
    def __init__(self):
        # 正常客户的个人信息模板
        self.normal_customers = [
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
        
        # 正常的资金用途
        self.normal_fund_usages = [
            '工资收入', '奖金收入', '投资收益', '利息收入', '商品购买', 
            '生活消费', '房租支出', '水电费', '通讯费', '交通费',
            '餐饮消费', '医疗费用', '教育培训', '保险缴费', '转账汇款',
            '理财投资', '基金定投', '房贷还款', '车贷还款'
        ]
        
        # 正常的交易对手方
        self.normal_counterparties = [
            '工商银行', '建设银行', '农业银行', '中国银行', '招商银行',
            '浦发银行', '中信银行', '光大银行', '华夏银行', '民生银行',
            '平安银行', '兴业银行', '广发银行', '浙商银行', '渤海银行'
        ]
        
        # 正常的交易渠道
        self.normal_channels = ['网上银行', '手机银行', 'ATM', '柜台', 'POS机']
        
        # 正常的交易地区
        self.normal_regions = ['北京', '上海', '广州', '深圳', '杭州', '南京', '成都', '武汉', '西安', '重庆']
        
        # 正常的IP地址池
        self.normal_ip_pool = [
            '192.168.1.100', '192.168.1.101', '192.168.1.102', '192.168.1.103',
            '10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4',
            '172.16.0.1', '172.16.0.2', '172.16.0.3', '172.16.0.4'
        ]
        
        # 正常的MAC地址池
        self.normal_mac_pool = [
            '00:1A:2B:3C:4D:5E', '00:1B:2C:3D:4E:5F', '00:1C:2D:3E:4F:60',
            'AA:BB:CC:DD:EE:FF', '11:22:33:44:55:66', '77:88:99:AA:BB:CC'
        ]

    def generate_normal_transaction_sample(self, case_id: str, customer_info: Dict) -> List[Dict]:
        """生成正常交易样本（固定6笔代表性交易，确保字段数量一致）"""
        transactions = []
        num_transactions = 6  # 固定6笔交易，确保所有案例字段数一致
        
        # 生成正常的时间分布（主要在工作日白天）
        base_date = datetime.now() - timedelta(days=random.randint(10, 45))
        
        for i in range(num_transactions):
            # 主要在工作日上午9-17点，偶尔有晚上交易
            hour = random.choices([9, 10, 11, 14, 15, 16, 17, 20, 21], 
                                weights=[15, 15, 15, 15, 15, 10, 10, 3, 2])[0]
            minute = random.randint(0, 59)
            trans_datetime = base_date + timedelta(days=i*2, hours=hour, minutes=minute)
            
            # 正常的交易金额分布（大部分小额，偶尔大额）
            if random.random() < 0.7:  # 70%小额交易
                amount = round(random.uniform(100, 5000), 2)
            else:  # 30%大额交易
                amount = round(random.uniform(5000, 50000), 2)
            
            transaction = {
                'TR_DT': trans_datetime.strftime('%Y-%m-%d'),
                'TR_TM': trans_datetime.strftime('%H:%M'),
                'TR_AMT': amount,
                'CURR_CD': 'CNY',
                'OPP_NAME': random.choice(self.normal_counterparties),
                'FUND_USE': random.choice(self.normal_fund_usages),
                'TR_CHNL': random.choice(self.normal_channels),
                'TR_AREA': random.choice(self.normal_regions),
                'SRC_CHNL': random.choice(self.normal_channels),
                'TR_ORG': random.choice(self.normal_counterparties),
                'REMARK': f'正常交易备注{i+1}'
            }
            transactions.append(transaction)
            
        return transactions

    def generate_low_risk_case(self, case_idx: int) -> str:
        """生成单个低风险案例的CSV行"""
        # 选择客户模板
        customer = self.normal_customers[case_idx % len(self.normal_customers)]
        
        # 生成案例基本信息
        case_id = f"case{case_idx+2:03d}"  # 从case002开始
        customer_name = customer['name']
        customer_id = f"CUST{1000 + case_idx:06d}"
        industry = customer['industry']
        gender = customer['gender']
        open_date = (datetime.now() - timedelta(days=random.randint(365, 1825))).strftime('%Y-%m-%d')  # 1-5年前开户
        address = customer['address']
        phone = customer['phone']
        id_type = '居民身份证'
        id_number = f"{random.randint(110000, 659000)}19{random.randint(85, 99)}{random.randint(1, 12):02d}{random.randint(1, 28):02d}{random.randint(1000, 9999)}"
        
        # 生成交易统计数据
        transaction_count = random.randint(50, 200)  # 正常交易笔数
        avg_amount = round(random.uniform(2000, 15000), 2)  # 正常平均金额
        total_amount = round(avg_amount * transaction_count, 2)
        max_amount = round(random.uniform(10000, 100000), 2)
        
        # 生成时间范围
        first_trans_date = (datetime.now() - timedelta(days=random.randint(30, 90))).strftime('%Y-%m-%d')
        last_trans_date = datetime.now().strftime('%Y-%m-%d')
        report_start = (datetime.strptime(first_trans_date, '%Y-%m-%d') - timedelta(days=7)).strftime('%Y年%m月%d日')
        report_end = datetime.now().strftime('%Y年%m月%d日')
        
        # 正常的夜间交易数量（很少）
        night_trans_count = random.randint(0, 5)
        
        # 正常的风险关键词（基本没有）
        risk_keywords = "正常交易"
        
        # 生成交易对手样本
        counterparties = random.sample(self.normal_counterparties, min(5, len(self.normal_counterparties)))
        counterparty_sample = ';'.join(counterparties)
        
        # 生成交易地区样本
        regions = random.sample(self.normal_regions, min(5, len(self.normal_regions)))
        top_opposing_areas = ';'.join(regions)
        
        # 生成主要交易渠道
        channels = random.sample(self.normal_channels, min(3, len(self.normal_channels)))
        main_tnx_channels = ';'.join(channels)
        
        # 生成交易样本（确保统一格式）
        transaction_samples = self.generate_normal_transaction_sample(case_id, customer)
        sample_trx_list = json.dumps(transaction_samples, ensure_ascii=False)
        
        # 确保JSON字段格式统一，避免解析问题
        sample_trx_list = sample_trx_list.replace(' ', '')  # 移除空格
        
        # 正常的借贷统计
        debit_count = random.randint(int(transaction_count * 0.4), int(transaction_count * 0.6))
        debit_amount = round(total_amount * random.uniform(0.4, 0.6), 2)
        credit_count = transaction_count - debit_count
        credit_amount = round(total_amount - debit_amount, 2)
        
        # 正常的模型信息
        model_name = "正常交易模型"
        is_gambling_suspected = "否"
        transaction_org = random.choice(self.normal_counterparties)
        
        # 正常的特征信息（统一格式）
        features_json = json.dumps([{
            'serial_num': '1',
            'features': '正常交易特征',
            'feature_value': f"{random.uniform(0.05, 0.3):.4f}",
            'highest_score': f"{random.uniform(15, 35):.2f}"
        }], ensure_ascii=False).replace(' ', '')
        
        highest_score = random.uniform(15, 35)
        
        # 生成IP和MAC地址
        ipv6_addresses = ';'.join([f"2001:db8::{random.randint(1000, 9999)}:{random.randint(1000, 9999)}" 
                                  for _ in range(random.randint(2, 4))])
        ip_addresses = ';'.join(random.sample(self.normal_ip_pool, random.randint(2, 4)))
        mac_addresses = ';'.join(random.sample(self.normal_mac_pool, random.randint(2, 3)))
        
        # 构造CSV行（严格按照原始36字段格式，对包含逗号的字段加引号）
        all_fields = [
            case_id,  # 1
            customer_name,  # 2
            customer_id,  # 3
            industry,  # 4
            gender,  # 5
            open_date,  # 6
            address,  # 7
            phone,  # 8
            id_type,  # 9
            id_number,  # 10
            str(total_amount),  # 11
            str(transaction_count),  # 12
            str(avg_amount),  # 13
            str(max_amount),  # 14
            first_trans_date,  # 15
            last_trans_date,  # 16
            report_start,  # 17
            report_end,  # 18
            str(night_trans_count),  # 19
            f'"{risk_keywords}"',  # 20 (加引号)
            f'"{counterparty_sample}"',  # 21 (加引号)
            f'"{top_opposing_areas}"',  # 22 (加引号)
            f'"{main_tnx_channels}"',  # 23 (加引号)
            f'{sample_trx_list}',  # 24 (JSON字段)
            str(debit_count),  # 25
            str(debit_amount),  # 26
            str(credit_count),  # 27
            str(credit_amount),  # 28
            model_name,  # 29
            is_gambling_suspected,  # 30
            transaction_org,  # 31
            f'{features_json}',  # 32 (JSON字段)
            f'{highest_score:.2f}',  # 33
            f'"{ipv6_addresses}"',  # 34 (加引号)
            f'"{ip_addresses}"',  # 35 (加引号)
            f'"{mac_addresses}"'   # 36 (加引号)
        ]
        
        # 构造最终CSV行
        csv_row = ','.join(all_fields)
        
        return csv_row

    def generate_multiple_cases(self, num_cases: int = 5) -> List[str]:
        """生成多个低风险案例"""
        cases = []
        for i in range(num_cases):
            case_data = self.generate_low_risk_case(i)
            cases.append(case_data)
            logger.info(f"已生成低风险案例: case{i+2:03d}")
        
        return cases

def main():
    """主函数"""
    generator = LowRiskDataGenerator()
    
    # 生成5个低风险案例
    low_risk_cases = generator.generate_multiple_cases(5)
    
    # 写入文件
    output_file = 'D:/AML_daily_task/demo低风险批量.csv'
    
    with open(output_file, 'w', encoding='utf-8-sig') as f:
        # 写入标题行（如果有需要的话）
        # f.write("case_id,main_cust_name,main_cust_id,...\n")
        
        # 写入数据行
        for case in low_risk_cases:
            f.write(case + '\n')
    
    logger.info(f"低风险数据已生成并保存到: {output_file}")
    logger.info(f"共生成 {len(low_risk_cases)} 个低风险案例")

if __name__ == "__main__":
    main()