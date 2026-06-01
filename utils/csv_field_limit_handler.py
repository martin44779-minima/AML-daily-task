#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV字段大小限制处理工具
用于解决"field larger than field limit"错误
"""

import csv
import sys
import logging
from typing import Iterator, List

logger = logging.getLogger(__name__)

def increase_csv_field_limit(target_limit: int = None) -> int:
    """
    增加CSV字段大小限制
    
    Args:
        target_limit: 目标限制大小，如果为None则自动加倍当前限制
        
    Returns:
        新的字段限制大小
    """
    current_limit = csv.field_size_limit()
    
    if target_limit is None:
        # 自动加倍当前限制，但不超过系统最大值
        target_limit = min(current_limit * 2, sys.maxsize)
    
    try:
        csv.field_size_limit(target_limit)
        logger.info(f"CSV字段大小限制已从 {current_limit} 增加到 {target_limit}")
        return target_limit
    except OverflowError as e:
        logger.warning(f"无法设置字段限制到 {target_limit}: {e}")
        # 尝试设置为系统允许的最大值
        max_possible = sys.maxsize
        try:
            csv.field_size_limit(max_possible)
            logger.info(f"CSV字段大小限制已设置为系统最大值: {max_possible}")
            return max_possible
        except Exception as e2:
            logger.error(f"无法设置任何字段限制: {e2}")
            return current_limit

def safe_csv_reader(file_path: str, encoding: str = 'utf-8', max_attempts: int = 3) -> Iterator[List[str]]:
    """
    安全的CSV读取器，自动处理字段大小限制问题
    
    Args:
        file_path: CSV文件路径
        encoding: 文件编码
        max_attempts: 最大尝试次数
        
    Yields:
        CSV行数据列表
    """
    for attempt in range(max_attempts):
        try:
            with open(file_path, 'r', encoding=encoding, newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    yield row
            return  # 成功读取完毕
        except csv.Error as e:
            if "field larger than field limit" in str(e) and attempt < max_attempts - 1:
                logger.warning(f"CSV字段大小超出限制 (尝试 {attempt + 1}/{max_attempts}): {str(e)}")
                # 增加字段限制
                increase_csv_field_limit()
                continue
            else:
                logger.error(f"CSV读取失败: {str(e)}")
                raise e
        except UnicodeDecodeError:
            # 尝试其他编码
            if encoding != 'gbk':
                logger.warning(f"UTF-8解码失败，尝试GBK编码")
                yield from safe_csv_reader(file_path, encoding='gbk', max_attempts=1)
            else:
                raise

def get_csv_field_stats(file_path: str, sample_lines: int = 1000) -> dict:
    """
    分析CSV文件字段大小统计信息
    
    Args:
        file_path: CSV文件路径
        sample_lines: 采样行数
        
    Returns:
        包含字段大小统计信息的字典
    """
    field_lengths = []
    line_count = 0
    
    try:
        for row in safe_csv_reader(file_path):
            if line_count >= sample_lines:
                break
                
            # 记录每行各字段的长度
            row_lengths = [len(field) if field else 0 for field in row]
            field_lengths.append(row_lengths)
            line_count += 1
            
    except Exception as e:
        logger.error(f"分析CSV文件时出错: {str(e)}")
        return {}
    
    if not field_lengths:
        return {}
    
    # 计算统计信息
    max_fields = max(len(row) for row in field_lengths)
    stats = {
        'total_lines_sampled': line_count,
        'max_fields_per_row': max_fields,
        'field_length_stats': []
    }
    
    # 为每个字段计算统计信息
    for field_idx in range(max_fields):
        field_values = []
        for row in field_lengths:
            if field_idx < len(row):
                field_values.append(row[field_idx])
            else:
                field_values.append(0)
        
        if field_values:
            stats['field_length_stats'].append({
                'field_index': field_idx,
                'max_length': max(field_values),
                'avg_length': sum(field_values) / len(field_values),
                'min_length': min(field_values)
            })
    
    return stats

def recommend_field_limit(stats: dict, safety_factor: float = 2.0) -> int:
    """
    根据统计信息推荐合适的字段限制
    
    Args:
        stats: 由get_csv_field_stats返回的统计信息
        safety_factor: 安全系数
        
    Returns:
        推荐的字段限制大小
    """
    if not stats.get('field_length_stats'):
        return csv.field_size_limit()
    
    # 找到最大的字段长度
    max_length = max(stat['max_length'] for stat in stats['field_length_stats'])
    
    # 应用安全系数并确保不低于当前限制
    current_limit = csv.field_size_limit()
    recommended_limit = max(int(max_length * safety_factor), current_limit)
    
    return recommended_limit

# 使用示例
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # 示例：分析CSV文件并调整字段限制
    test_file = "path/to/your/large_file.csv"
    
    # 获取文件统计信息
    stats = get_csv_field_stats(test_file)
    print("CSV文件统计信息:", stats)
    
    # 推荐字段限制
    if stats:
        recommended_limit = recommend_field_limit(stats)
        print(f"推荐字段限制: {recommended_limit}")
        
        # 调整字段限制
        actual_limit = increase_csv_field_limit(recommended_limit)
        print(f"实际设置的字段限制: {actual_limit}")