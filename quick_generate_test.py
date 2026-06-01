#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版测试数据生成器
快速生成符合column_mapping的测试CSV数据
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generate_complete_test_data import generate_test_data, save_test_data

def quick_generate(size='medium'):
    """
    快速生成不同规模的测试数据
    
    Args:
        size: 数据规模 ('small'=1万条, 'medium'=10万条, 'large'=50万条)
    """
    size_map = {
        'small': (10000, 10),
        'medium': (100000, 20), 
        'large': (500000, 50)
    }
    
    if size not in size_map:
        size = 'medium'
    
    rows, cases = size_map[size]
    print(f"生成{size}规模测试数据 ({rows}行, {cases}个案例)...")
    
    df = generate_test_data(total_rows=rows, num_cases=cases)
    filename = f'test_data_{size}_{rows}rows.csv'
    save_test_data(df, filename)
    
    return filename

if __name__ == "__main__":
    # 默认生成中等规模数据
    size = sys.argv[1] if len(sys.argv) > 1 else 'medium'
    quick_generate(size)