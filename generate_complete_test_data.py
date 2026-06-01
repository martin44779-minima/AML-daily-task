#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成完整的AML测试CSV数据
基于column_mapping生成包含所有字段的测试数据
包含约20个案例，总计约10万条交易记录
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import json
import uuid

def generate_test_data(total_rows=100000, num_cases=20):
    """
    生成完整的测试数据
    
    Args:
        total_rows: 总行数（交易记录数）
        num_cases: 案例数量
    """
    
    # 定义column_mapping（与csv_processing_service.py中的一致）
    column_mapping = {
        '案例编号': 'case_id',
        '数据日期': 'data_date',
        '主客户编号': 'main_cust_id',
        '主客户名称': 'main_cust_name',
        '证件类型': 'id_type',
        '证件号': 'id_number',
        '对公对私标志':'main_cust_type',
        '主客户职业行业': 'main_cust_industry',
        '主客户性别': 'main_cust_gender',
        '主客户开户日期': 'main_cust_open_date',
        '主客户地址': 'main_cust_addr',
        '主客户联系电话': 'main_cust_phone_number',
        '对公客户营业地址':'main_biz_addr',
        '注册资本':'main_reg_fund_am',
        '经营范围':'main_biz_scope',
        '法定代表人名称':'main_legal_name',
        '法定代表人证件类型':'main_legal_cert_type',
        '法定代表人证件号码':'main_legal_cert',
        '可疑模型编号': 'model_id',
        '可疑模型名称': 'model_name',
        '可疑特征规则编号': 'suspect_rule_id',
        '可疑特征规则特征名称': 'suspect_rule_name',
        '模型平台最高分数': 'highest_score',
        '机器学习匹配规则前10特征序号': 'serial_num',
        '机器学习匹配规则前10特征说明': 'features',
        '机器学习匹配规则前10特征风险值': 'feature_value',
        '可疑案例下所有客户号': 'all_case_cust_ids',
        '可疑案例下所有客户名称': 'all_case_cust_names',
        '可疑案例下所有账号': 'all_case_acct_nos',
        '交易主键': 'trans_key',
        '交易日期': 'trans_date',
        '交易日期和时间': 'trans_datetime',
        '交易机构': 'trans_org',
        '客户类型': 'cust_type',
        '卡号折号': 'card_no',
        '卡片类型': 'card_type',
        'am1交易渠道': 'aml_channel',
        '源系统交易渠道': 'src_channel',
        'am1交易代码': 'aml_trans_code',
        '源系统交易代码': 'src_trans_code',
        '现转标志': 'cash_transfer_flag',
        '借贷标志': 'debit_credit_flag',
        '收付标志': 'income_pay_flag',
        '币种': 'currency',
        '原币种交易金额': 'trans_amt',
        '折人民币交易金额': 'cny_amt',
        '折美元交易金额': 'usd_amt',
        '交易余额': 'trans_balance',
        '交易发生国家': 'trans_country',
        '交易发生地区': 'trans_region',
        '资金用途和来源': 'fund_usage',
        '对方名称': 'counterparty_name',
        '对方账号': 'counterparty_acct_no',
        '对手PBC账户类型': 'pbc_acct_type',
        '对方是否我行客户': 'is_our_cust',
        '对方客户编号': 'counterparty_cust_id',
        '对方客户类型': 'counterparty_cust_type',
        '对方卡号折号': 'counterparty_card_no',
        '对方金融机构编号': 'fin_inst_id',
        '对方金融机构名称': 'fin_inst_name',
        '对方金融机构网点国家': 'fin_inst_country',
        '对方金融机构网点地区': 'fin_inst_region',
        '交易IPV6地址': 'ipv6_addr',
        'IP地址': 'ip_addr',
        '交易MAC地址': 'mac_addr',
        '摘要码': 'summary_code',
        '交易备注': 'trans_remark'
    }
    
    # 获取列名列表
    columns = list(column_mapping.keys())
    
    # 基础数据池
    industries = ['制造业', '批发零售业', '金融业', '房地产业', '信息技术服务业', '教育', '医疗健康', '交通运输']
    genders = ['男', '女']
    id_types = ['身份证', '护照', '军官证', '港澳通行证', '台湾通行证']
    countries = ['中国', '美国', '日本', '韩国', '新加坡', '英国', '德国', '法国']
    regions = ['北京', '上海', '广州', '深圳', '杭州', '南京', '成都', '武汉']
    channels = ['网银', '手机银行', 'ATM', '柜台', 'POS机', '第三方支付']
    currencies = ['CNY', 'USD', 'EUR', 'JPY', 'HKD']
    fund_usages = ['工资收入', '投资收益', '经营收入', '转账汇款', '消费支出', '贷款还款']
    account_types = ['储蓄账户', '信用卡账户', '对公账户', '理财账户']
    
    # 生成案例基础信息
    case_base_data = []
    for i in range(num_cases):
        case_type = random.choice(['对私', '对公'])
        
        if case_type == '对私':
            main_cust_name = f"个人客户_{i+1:03d}"
            main_cust_id = f"CUST_P_{uuid.uuid4().hex[:8].upper()}"
            id_type = random.choice(id_types)
            id_number = f"{random.randint(110000, 820000)}{random.randint(1980, 2005)}{random.randint(10000000, 99999999)}"
            gender = random.choice(genders)
            industry = random.choice(industries)
            biz_addr = ""
            reg_fund = ""
            biz_scope = ""
            legal_name = ""
            legal_cert_type = ""
            legal_cert = ""
        else:  # 对公
            main_cust_name = f"企业客户_{i+1:03d}有限公司"
            main_cust_id = f"CUST_C_{uuid.uuid4().hex[:8].upper()}"
            id_type = "统一社会信用代码"
            id_number = f"91{random.randint(110000, 820000)}{random.randint(2010, 2023)}{random.randint(100000000, 999999999)}"
            gender = ""
            industry = random.choice(industries)
            biz_addr = f"{random.choice(regions)}市{random.choice(['朝阳区', '浦东新区', '天河区'])}{random.randint(1, 1000)}号"
            reg_fund = f"{random.randint(100, 10000)}万元"
            biz_scope = f"{industry}相关业务"
            legal_name = f"法人代表_{random.randint(100, 999)}"
            legal_cert_type = "身份证"
            legal_cert = f"{random.randint(110000, 820000)}{random.randint(1970, 1990)}{random.randint(10000000, 99999999)}"
        
        case_base_data.append({
            'case_id': f"CASE_{uuid.uuid4().hex[:12].upper()}",
            'data_date': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d'),
            'main_cust_id': main_cust_id,
            'main_cust_name': main_cust_name,
            'id_type': id_type,
            'id_number': id_number,
            'main_cust_type': case_type,
            'main_cust_industry': industry,
            'main_cust_gender': gender,
            'main_cust_open_date': (datetime.now() - timedelta(days=random.randint(365, 3650))).strftime('%Y-%m-%d'),
            'main_cust_addr': f"{random.choice(regions)}市{random.choice(['朝阳区', '浦东新区', '天河区'])}街道{random.randint(1, 1000)}号",
            'main_cust_phone_number': f"1{random.randint(3, 9)}{random.randint(100000000, 999999999)}",
            'main_biz_addr': biz_addr,
            'main_reg_fund_am': reg_fund,
            'main_biz_scope': biz_scope,
            'main_legal_name': legal_name,
            'main_legal_cert_type': legal_cert_type,
            'main_legal_cert': legal_cert,
            'model_id': f"MODEL_{random.randint(1, 20):02d}",
            'model_name': f"可疑交易模型_{random.randint(1, 20)}",
            'suspect_rule_id': f"RULE_{random.randint(1, 50):02d}",
            'suspect_rule_name': f"可疑规则_{random.randint(1, 50)}",
            'highest_score': round(random.uniform(60, 99), 2)
        })
    
    # 计算每案例平均交易数
    avg_transactions_per_case = total_rows // num_cases
    
    # 生成完整的数据
    data_rows = []
    
    for case_idx, case_info in enumerate(case_base_data):
        # 确定该案例的交易数量（允许一定波动）
        transactions_count = max(100, int(avg_transactions_per_case * random.uniform(0.7, 1.3)))
        
        # 为该案例生成交易数据
        for trans_idx in range(transactions_count):
            # 基础交易信息
            transaction_datetime = datetime.now() - timedelta(
                days=random.randint(1, 365),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            # 生成交易金额（对私和对公有不同的金额分布）
            if case_info['main_cust_type'] == '对私':
                trans_amount = round(random.uniform(100, 50000), 2)
            else:
                trans_amount = round(random.uniform(1000, 500000), 2)
            
            # 币种转换
            currency = random.choice(currencies)
            cny_rate = 1.0 if currency == 'CNY' else random.uniform(6.5, 7.5) if currency == 'USD' else random.uniform(7.5, 8.5)
            usd_rate = 1.0 if currency == 'USD' else random.uniform(0.1, 0.2)
            
            # 对手方信息
            counterparty_type = random.choice(['对私', '对公'])
            if counterparty_type == '对私':
                counterparty_name = f"个人_{random.randint(1000, 9999)}"
                counterparty_id = f"CP_P_{uuid.uuid4().hex[:8].upper()}"
            else:
                counterparty_name = f"公司_{random.randint(100, 999)}有限公司"
                counterparty_id = f"CP_C_{uuid.uuid4().hex[:8].upper()}"
            
            # 生成机器学习特征数据（部分行有数据）
            ml_features = []
            if random.random() < 0.3:  # 30%的记录有ML特征
                for j in range(random.randint(1, 5)):
                    ml_features.append({
                        'serial_num': j,
                        'features': f"特征描述_{j}_{random.randint(1, 100)}",
                        'feature_value': round(random.uniform(0.1, 1.0), 4),
                        'highest_score': case_info['highest_score']
                    })
            
            # 构造完整行数据
            row_data = {
                '案例编号': case_info['case_id'],
                '数据日期': case_info['data_date'],
                '主客户编号': case_info['main_cust_id'],
                '主客户名称': case_info['main_cust_name'],
                '证件类型': case_info['id_type'],
                '证件号': case_info['id_number'],
                '对公对私标志': case_info['main_cust_type'],
                '主客户职业行业': case_info['main_cust_industry'],
                '主客户性别': case_info['main_cust_gender'],
                '主客户开户日期': case_info['main_cust_open_date'],
                '主客户地址': case_info['main_cust_addr'],
                '主客户联系电话': case_info['main_cust_phone_number'],
                '对公客户营业地址': case_info['main_biz_addr'],
                '注册资本': case_info['main_reg_fund_am'],
                '经营范围': case_info['main_biz_scope'],
                '法定代表人名称': case_info['main_legal_name'],
                '法定代表人证件类型': case_info['main_legal_cert_type'],
                '法定代表人证件号码': case_info['main_legal_cert'],
                '可疑模型编号': case_info['model_id'],
                '可疑模型名称': case_info['model_name'],
                '可疑特征规则编号': case_info['suspect_rule_id'],
                '可疑特征规则特征名称': case_info['suspect_rule_name'],
                '模型平台最高分数': case_info['highest_score'],
                '机器学习匹配规则前10特征序号': json.dumps([f['serial_num'] for f in ml_features]) if ml_features else '',
                '机器学习匹配规则前10特征说明': json.dumps([f['features'] for f in ml_features]) if ml_features else '',
                '机器学习匹配规则前10特征风险值': json.dumps([f['feature_value'] for f in ml_features]) if ml_features else '',
                '可疑案例下所有客户号': json.dumps([case_info['main_cust_id'], counterparty_id]),
                '可疑案例下所有客户名称': json.dumps([case_info['main_cust_name'], counterparty_name]),
                '可疑案例下所有账号': json.dumps([f"ACC{random.randint(10000000, 99999999)}", f"ACC{random.randint(10000000, 99999999)}"]),
                '交易主键': f"TRANS_{uuid.uuid4().hex[:16].upper()}",
                '交易日期': transaction_datetime.strftime('%Y-%m-%d'),
                '交易日期和时间': transaction_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                '交易机构': f"机构_{random.randint(100, 999)}",
                '客户类型': case_info['main_cust_type'],
                '卡号折号': f"CARD{random.randint(1000000000000000, 9999999999999999)}",
                '卡片类型': random.choice(['借记卡', '贷记卡', '准贷记卡']),
                'am1交易渠道': random.choice(channels),
                '源系统交易渠道': random.choice(channels),
                'am1交易代码': f"TC{random.randint(1000, 9999)}",
                '源系统交易代码': f"STC{random.randint(1000, 9999)}",
                '现转标志': random.choice(['现金', '转账']),
                '借贷标志': random.choice(['借', '贷']),
                '收付标志': random.choice(['收', '付']),
                '币种': currency,
                '原币种交易金额': trans_amount,
                '折人民币交易金额': round(trans_amount * cny_rate, 2),
                '折美元交易金额': round(trans_amount * usd_rate, 2),
                '交易余额': round(random.uniform(0, 1000000), 2),
                '交易发生国家': random.choice(countries),
                '交易发生地区': random.choice(regions),
                '资金用途和来源': random.choice(fund_usages),
                '对方名称': counterparty_name,
                '对方账号': f"ACC{random.randint(10000000, 99999999)}",
                '对手PBC账户类型': random.choice(account_types),
                '对方是否我行客户': random.choice(['是', '否']),
                '对方客户编号': counterparty_id,
                '对方客户类型': counterparty_type,
                '对方卡号折号': f"CARD{random.randint(1000000000000000, 9999999999999999)}",
                '对方金融机构编号': f"BANK{random.randint(1000, 9999)}",
                '对方金融机构名称': f"银行_{random.randint(1, 100)}",
                '对方金融机构网点国家': random.choice(countries),
                '对方金融机构网点地区': random.choice(regions),
                '交易IPV6地址': f"2001:db8::{random.randint(1, 9999)}:{random.randint(1, 9999)}:{random.randint(1, 9999)}:{random.randint(1, 9999)}",
                'IP地址': f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}",
                '交易MAC地址': f"{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}:{random.randint(0, 255):02x}",
                '摘要码': f"SUM{random.randint(1000, 9999)}",
                '交易备注': f"交易备注_{random.randint(1, 1000)}"
            }
            
            data_rows.append(row_data)
    
    # 创建DataFrame
    df = pd.DataFrame(data_rows, columns=columns)
    
    return df

def save_test_data(df, filename='complete_test_data.csv'):
    """
    保存测试数据到CSV文件
    
    Args:
        df: DataFrame数据
        filename: 输出文件名
    """
    # 使用pandas的to_csv方法确保正确处理包含JSON等复杂字段的情况
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"测试数据已保存到: {filename}")
    print(f"总行数: {len(df)}")
    print(f"列数: {len(df.columns)}")
    print(f"案例数量: {df['案例编号'].nunique()}")

def main():
    """主函数"""
    print("开始生成完整的AML测试数据...")
    
    # 生成数据
    df = generate_test_data(total_rows=100000, num_cases=20)
    
    # 保存数据
    save_test_data(df, 'complete_test_data.csv')
    
    # 显示数据概览
    print("\n数据概览:")
    print(f"数据形状: {df.shape}")
    print(f"列名: {list(df.columns)}")
    print("\n前5行数据:")
    print(df.head())
    
    # 统计信息
    print(f"\n案例统计:")
    print(f"- 总案例数: {df['案例编号'].nunique()}")
    print(f"- 对私案例数: {len(df[df['对公对私标志'] == '对私']['案例编号'].unique())}")
    print(f"- 对公案例数: {len(df[df['对公对私标志'] == '对公']['案例编号'].unique())}")
    print(f"- 平均每案例交易数: {len(df) / df['案例编号'].nunique():.1f}")

if __name__ == "__main__":
    main()