"""
Dify工具：UNL格式转换工具
功能：将UNL.GZ文件转换为其他格式，或将CSV转换为UNL格式
"""
import os
import gzip
import csv
import logging
from typing import Dict, Any, Optional
from config.settings import Settings

logger = logging.getLogger(__name__)


def unl_gz_to_csv_tool(input_path: str, output_path: str = None) -> Dict[str, Any]:
    """
    Dify工具函数：将.unl.gz文件转换为CSV文件
    
    Args:
        input_path: 输入的.unl.gz文件路径
        output_path: 输出的CSV文件路径，如果为None则自动生成
    
    Returns:
        包含转换结果的字典
    """
    if not os.path.exists(input_path):
        logger.error(f"错误: 输入文件 '{input_path}' 不存在.")
        return {
            "success": False,
            "message": f"输入文件 '{input_path}' 不存在",
            "output_path": None
        }
    
    # 如果没有指定输出路径，生成一个CSV文件路径
    if output_path is None:
        base_name = os.path.splitext(os.path.splitext(input_path)[0])[0]
        output_path = f"{base_name}.csv"
    
    try:
        with gzip.open(input_path, 'rt', encoding='utf-8') as gz_file:
            with open(output_path, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                for line_num, line in enumerate(gz_file, 1):
                    line = line.strip()
                    if line:
                        fields = line.split('\x07')  # 使用^G作为分隔符
                        writer.writerow(fields)
                    # 每处理10000行打印一次进度
                    if line_num % 10000 == 0:
                        logger.info(f"已处理 {line_num} 行")
        
        logger.info(f"成功将 {input_path} 转换为 {output_path}")
        return {
            "success": True,
            "message": f"成功将 {input_path} 转换为 {output_path}",
            "output_path": output_path
        }
    
    except Exception as e:
        logger.error(f"转换.unl.gz到CSV时出错: {str(e)}")
        return {
            "success": False,
            "message": f"转换.unl.gz到CSV时出错: {str(e)}",
            "output_path": None
        }


def csv_to_unl_gz_tool(input_path: str, output_path: str = None) -> Dict[str, Any]:
    """
    Dify工具函数：将CSV文件转换为.unl.gz文件
    
    Args:
        input_path: 输入的CSV文件路径
        output_path: 输出的.unl.gz文件路径，如果为None则自动生成
    
    Returns:
        包含转换结果的字典
    """
    if not os.path.exists(input_path):
        logger.error(f"错误: 输入文件 '{input_path}' 不存在.")
        return {
            "success": False,
            "message": f"输入文件 '{input_path}' 不存在",
            "output_path": None
        }
    
    # 如果没有指定输出路径，生成一个UNL.GZ文件路径
    if output_path is None:
        base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}.unl.gz"
    
    try:
        with open(input_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            with gzip.open(output_path, 'wt', encoding='utf-8') as gz_file:
                for line_num, row in enumerate(reader, 1):
                    # 使用\x07作为字段分隔符
                    unl_line = '\x07'.join(row)
                    gz_file.write(unl_line + '\n')
                    
                    # 每处理10000行打印一次进度
                    if line_num % 10000 == 0:
                        logger.info(f"已处理 {line_num} 行")
        
        logger.info(f"成功将 {input_path} 转换为 {output_path}")
        return {
            "success": True,
            "message": f"成功将 {input_path} 转换为 {output_path}",
            "output_path": output_path
        }
    
    except Exception as e:
        logger.error(f"转换CSV到.unl.gz时出错: {str(e)}")
        return {
            "success": False,
            "message": f"转换CSV到.unl.gz时出错: {str(e)}",
            "output_path": None
        }


def convert_unl_encoding_tool(input_path: str, output_path: str = None, 
                           input_encoding: str = 'utf-8', 
                           output_encoding: str = 'utf-8') -> Dict[str, Any]:
    """
    Dify工具函数：转换UNL文件的编码格式
    
    Args:
        input_path: 输入的UNL文件路径（可以是压缩或未压缩的）
        output_path: 输出的UNL文件路径，如果为None则自动生成
        input_encoding: 输入文件编码
        output_encoding: 输出文件编码
    
    Returns:
        包含转换结果的字典
    """
    if not os.path.exists(input_path):
        logger.error(f"错误: 输入文件 '{input_path}' 不存在.")
        return {
            "success": False,
            "message": f"输入文件 '{input_path}' 不存在",
            "output_path": None
        }
    
    # 如果没有指定输出路径，生成一个输出文件路径
    if output_path is None:
        if input_path.endswith('.gz'):
            base_name = os.path.splitext(os.path.splitext(input_path)[0])[0]
            output_path = f"{base_name}_converted.gz"
        else:
            base_name = os.path.splitext(input_path)[0]
            output_path = f"{base_name}_converted.unl"
    
    try:
        is_input_compressed = input_path.endswith('.gz')
        is_output_compressed = output_path.endswith('.gz')
        
        # 打开输入文件
        if is_input_compressed:
            input_file = gzip.open(input_path, 'rt', encoding=input_encoding)
        else:
            input_file = open(input_path, 'r', encoding=input_encoding)
        
        # 打开输出文件
        if is_output_compressed:
            output_file = gzip.open(output_path, 'wt', encoding=output_encoding)
        else:
            output_file = open(output_path, 'w', encoding=output_encoding)
        
        try:
            for line_num, line in enumerate(input_file, 1):
                output_file.write(line)
                
                # 每处理10000行打印一次进度
                if line_num % 10000 == 0:
                    logger.info(f"已转换 {line_num} 行")
        finally:
            input_file.close()
            output_file.close()
        
        logger.info(f"成功将 {input_path} 从 {input_encoding} 转换为 {output_encoding} 编码，输出到 {output_path}")
        return {
            "success": True,
            "message": f"成功将 {input_path} 从 {input_encoding} 转换为 {output_encoding} 编码",
            "output_path": output_path
        }
    
    except Exception as e:
        logger.error(f"转换UNL文件编码时出错: {str(e)}")
        return {
            "success": False,
            "message": f"转换UNL文件编码时出错: {str(e)}",
            "output_path": None
        }


if __name__ == "__main__":
    # 示例调用
    result = unl_gz_to_csv_tool("./sample.unl.gz")
    print(result)