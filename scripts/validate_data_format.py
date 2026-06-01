#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证生成的低风险数据格式是否正确
"""

import pandas as pd

def validate_csv_format(file_path):
    """验证CSV文件格式"""
    print(f"验证文件: {file_path}")
    
    try:
        # 尝试读取文件（跳过表头）
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        print(f"✓ 成功读取文件")
        print(f"  行数: {len(df)} (不含表头)")
        print(f"  列数: {len(df.columns)}")
        
        # 显示前几列的内容
        print("\n前5列内容预览:")
        for i in range(min(5, len(df.columns))):
            print(f"  列{i}: {df.iloc[0, i]}")
            
        # 检查是否有空值
        null_counts = df.isnull().sum()
        if null_counts.sum() > 0:
            print(f"\n空值统计:")
            for i, count in enumerate(null_counts):
                if count > 0:
                    print(f"  列{i}: {count}个空值")
        else:
            print("\n✓ 无空值")
            
        return True
        
    except Exception as e:
        print(f"✗ 读取失败: {e}")
        return False

def compare_with_high_risk():
    """与高风险数据进行对比"""
    print("=" * 50)
    print("对比分析:")
    print("=" * 50)
    
    # 验证两个文件
    high_risk_valid = validate_csv_format('demo高风险.csv')
    low_risk_valid = validate_csv_format('demo低风险标准格式.csv')
    
    if high_risk_valid and low_risk_valid:
        # 读取数据进行详细对比
        df_high = pd.read_csv('demo高风险.csv', header=None)
        df_low = pd.read_csv('demo低风险批量.csv', header=None)
        
        print(f"\n格式对比:")
        print(f"  高风险数据列数: {len(df_high.columns)}")
        print(f"  低风险数据列数: {len(df_low.columns)}")
        print(f"  列数是否一致: {len(df_high.columns) == len(df_low.columns)}")
        
        # 检查数据类型一致性
        print(f"\n数据特征对比:")
        print(f"  高风险总交易金额: {df_high.iloc[0, 10]}")
        print(f"  低风险总交易金额: {df_low.iloc[0, 10]}")
        print(f"  高风险交易笔数: {df_high.iloc[0, 11]}")
        print(f"  低风险交易笔数: {df_low.iloc[0, 11]}")
        print(f"  高风险风险关键词: {df_high.iloc[0, 19]}")
        print(f"  低风险风险关键词: {df_low.iloc[0, 19]}")

if __name__ == "__main__":
    compare_with_high_risk()