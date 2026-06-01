#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
在实际应用中添加调试信息的示例
将此代码添加到您遇到问题的地方
"""

import os
import logging
from config.settings import Settings

logger = logging.getLogger(__name__)

def debug_unl_config():
    """调试UNL配置的函数"""
    logger.info("=== UNL配置调试信息 ===")
    
    # 直接检查环境变量
    logger.info(f"环境变量 UNL_RMT_PUB_PATH: {os.getenv('UNL_RMT_PUB_PATH', 'NOT_SET')}")
    
    # 检查Settings类
    logger.info(f"Settings.UNL_RMT_PUB_PATH: {getattr(Settings, 'UNL_RMT_PUB_PATH', 'NOT_FOUND')}")
    
    # 检查当前工作目录
    logger.info(f"当前工作目录: {os.getcwd()}")
    
    # 检查.env文件是否存在
    env_file_exists = os.path.exists('.env')
    logger.info(f".env文件存在: {env_file_exists}")
    
    if env_file_exists:
        # 读取.env文件内容
        try:
            with open('.env', 'r', encoding='utf-8') as f:
                env_content = f.read()
                # 查找UNL相关配置
                for line in env_content.split('\n'):
                    if 'UNL_' in line and '=' in line:
                        logger.info(f"配置行: {line}")
        except Exception as e:
            logger.error(f"读取.env文件出错: {str(e)}")

# 使用示例 - 在您的代码中调用这个函数
# debug_unl_config()