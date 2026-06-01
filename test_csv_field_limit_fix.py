#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试CSV字段大小限制修复效果
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.csv_field_limit_handler import increase_csv_field_limit, safe_csv_reader, get_csv_field_stats
import csv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_csv_field_limit_fix():
    """测试CSV字段大小限制修复"""
    
    # 测试增加字段限制
    print("=== 测试CSV字段大小限制增加 ===")
    original_limit = csv.field_size_limit()
    print(f"原始字段限制: {original_limit}")
    
    new_limit = increase_csv_field_limit()
    print(f"新字段限制: {new_limit}")
    
    # 创建一个测试CSV文件，包含大字段
    test_file = "test_large_field.csv"
    print(f"\n=== 创建测试文件 {test_file} ===")
    
    # 创建包含大字段的测试数据
    large_field = "A" * 200000  # 20万个字符的字段
    test_data = [
        ["id", "name", "large_field", "description"],
        ["1", "test1", large_field, "这是第一个测试记录"],
        ["2", "test2", "normal_field", "这是第二个测试记录"],
        ["3", "test3", large_field, "这是第三个测试记录"]
    ]
    
    try:
        # 写入测试文件
        with open(test_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(test_data)
        print(f"测试文件已创建: {test_file}")
        
        # 测试安全读取
        print("\n=== 测试安全CSV读取 ===")
        row_count = 0
        for row in safe_csv_reader(test_file):
            row_count += 1
            print(f"行 {row_count}: 字段数 = {len(row)}")
            # 显示前几个字段的长度信息
            for i, field in enumerate(row[:3]):  # 只显示前3个字段
                print(f"  字段 {i}: 长度 = {len(field) if field else 0}")
        
        print(f"\n成功读取 {row_count} 行数据")
        
        # 测试字段统计
        print("\n=== 测试字段统计分析 ===")
        stats = get_csv_field_stats(test_file, sample_lines=10)
        if stats:
            print("字段统计信息:")
            print(f"  采样行数: {stats['total_lines_sampled']}")
            print(f"  最大字段数: {stats['max_fields_per_row']}")
            print("  各字段长度统计:")
            for field_stat in stats['field_length_stats']:
                print(f"    字段 {field_stat['field_index']}: "
                      f"最大={field_stat['max_length']}, "
                      f"平均={field_stat['avg_length']:.1f}, "
                      f"最小={field_stat['min_length']}")
        
        return True
        
    except Exception as e:
        logger.error(f"测试过程中出现错误: {str(e)}")
        return False
    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"\n已清理测试文件: {test_file}")

def test_with_real_file(file_path):
    """测试处理真实的大字段CSV文件"""
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return False
    
    print(f"=== 分析真实文件: {file_path} ===")
    
    try:
        # 获取文件统计信息
        stats = get_csv_field_stats(file_path, sample_lines=1000)
        if stats:
            print("文件统计信息:")
            print(f"  采样行数: {stats['total_lines_sampled']}")
            print(f"  最大字段数: {stats['max_fields_per_row']}")
            
            # 找出最大的字段
            max_length = 0
            max_field_idx = -1
            for field_stat in stats['field_length_stats']:
                if field_stat['max_length'] > max_length:
                    max_length = field_stat['max_length']
                    max_field_idx = field_stat['field_index']
            
            print(f"  最大字段长度: {max_length} (字段索引: {max_field_idx})")
            
            # 推荐字段限制
            from utils.csv_field_limit_handler import recommend_field_limit
            recommended_limit = recommend_field_limit(stats)
            print(f"  推荐字段限制: {recommended_limit}")
            
            # 调整字段限制
            actual_limit = increase_csv_field_limit(recommended_limit)
            print(f"  实际设置字段限制: {actual_limit}")
            
            # 尝试读取文件
            print("\n=== 尝试读取文件 ===")
            row_count = 0
            error_count = 0
            for row in safe_csv_reader(file_path):
                row_count += 1
                if row_count <= 3:  # 只显示前3行
                    print(f"行 {row_count}: 字段数 = {len(row)}")
                if row_count >= 1000:  # 限制读取行数进行测试
                    break
                    
            print(f"成功读取 {row_count} 行数据")
            return True
        else:
            print("无法获取文件统计信息")
            return False
            
    except Exception as e:
        logger.error(f"处理真实文件时出错: {str(e)}")
        return False

if __name__ == "__main__":
    print("开始测试CSV字段大小限制修复...")
    
    # 运行基本测试
    success = test_csv_field_limit_fix()
    
    if success:
        print("\n✓ 基本测试通过")
        
        # 如果用户提供了文件路径参数，测试真实文件
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            print(f"\n开始测试真实文件: {file_path}")
            test_with_real_file(file_path)
    else:
        print("\n✗ 基本测试失败")
        
    print("\n测试完成!")