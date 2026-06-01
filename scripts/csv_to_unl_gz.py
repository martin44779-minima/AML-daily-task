#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CSV to UNL.GZ Converter Script
Converts a CSV file to UNL format with \x07 field separator and compresses it to .unl.gz
"""

import csv
import gzip
import os
import sys
import argparse


def csv_to_unl_gz(input_csv_path, output_unl_gz_path=None):
    """
    Convert a CSV file to UNL format and compress it as .gz file
    
    Args:
        input_csv_path (str): Path to the input CSV file
        output_unl_gz_path (str, optional): Path to the output .unl.gz file. 
                                          If None, uses input path with .unl.gz extension
    
    Returns:
        str: Path to the output .unl.gz file
    """
    # 如果没有提供输出路径，则基于输入路径生成输出路径
    if output_unl_gz_path is None:
        base_name = os.path.splitext(input_csv_path)[0]
        output_unl_gz_path = f"{base_name}.unl.gz"
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_unl_gz_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 读取CSV文件并将其转换为UNL格式，然后压缩
        with open(input_csv_path, 'r', encoding='utf-8', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            
            with gzip.open(output_unl_gz_path, 'wt', encoding='utf-8') as gz_file:
                for row in csv_reader:
                    # 使用\x07作为字段分隔符连接行数据
                    unl_line = '\x07'.join(row)
                    gz_file.write(unl_line + '\n')
        
        print(f'Successfully converted {input_csv_path} to {output_unl_gz_path}')
        return output_unl_gz_path
    
    except FileNotFoundError:
        print(f"Error: Input file '{input_csv_path}' does not exist.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def csv_to_unl(input_csv_path, output_unl_path=None):
    """
    Convert a CSV file to UNL format (without compression)
    
    Args:
        input_csv_path (str): Path to the input CSV file
        output_unl_path (str, optional): Path to the output .unl file. 
                                       If None, uses input path with .unl extension
    
    Returns:
        str: Path to the output .unl file
    """
    if output_unl_path is None:
        base_name = os.path.splitext(input_csv_path)[0]
        output_unl_path = f"{base_name}.unl"
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_unl_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    try:
        with open(input_csv_path, 'r', encoding='utf-8', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            
            with open(output_unl_path, 'w', encoding='utf-8', newline='') as unl_file:
                for row in csv_reader:
                    # 使用\x07作为字段分隔符连接行数据
                    unl_line = '\x07'.join(row)
                    unl_file.write(unl_line + '\n')
        
        print(f'Successfully converted {input_csv_path} to {output_unl_path}')
        return output_unl_path
    
    except FileNotFoundError:
        print(f"Error: Input file '{input_csv_path}' does not exist.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description='Convert CSV file to UNL.GZ format')
    parser.add_argument('input_csv', help='Input CSV file path')
    parser.add_argument('-o', '--output', help='Output UNL.GZ file path (optional)')
    parser.add_argument('--unl-only', action='store_true', 
                       help='Generate UNL file only (without compression)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_csv):
        print(f"Error: Input file '{args.input_csv}' does not exist.")
        sys.exit(1)
    
    if args.unl_only:
        # 只生成UNL文件，不压缩
        output_path = os.path.splitext(args.input_csv)[0] + '.unl' if not args.output else args.output
        result = csv_to_unl(args.input_csv, output_path)
    else:
        # 生成压缩的UNL.GZ文件
        output_path = os.path.splitext(args.input_csv)[0] + '.unl.gz' if not args.output else args.output
        result = csv_to_unl_gz(args.input_csv, output_path)
    
    if result:
        print(f'Conversion completed successfully. Output file: {result}')
    else:
        print('Conversion failed.')
        sys.exit(1)


if __name__ == '__main__':
    main()