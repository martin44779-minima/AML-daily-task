#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细诊断UNL配置问题
"""

import os
import sys
import logging
from config.settings import Settings
from services.download_unl_service import DownloadUnlService

# 设置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def detailed_diagnosis():
    """详细诊断配置问题"""
    print("=== 详细配置诊断 ===")
    
    # 1. 检查当前工作目录
    print(f"当前工作目录: {os.getcwd()}")
    print(f".env文件是否存在: {os.path.exists('.env')}")
    
    # 2. 检查环境变量加载
    print("\n=== 环境变量检查 ===")
    env_vars = ['UNL_DOWNLOAD_URL', 'UNL_FILE_NAME_LIST', 'UNL_FILE_SVR_ID', 'UNL_RMT_PUB_PATH']
    for var in env_vars:
        value = os.getenv(var, 'NOT_SET')
        print(f"{var}: {value}")
        if value == 'NOT_SET':
            print(f"  ❌ {var} 未设置")
        elif not value:
            print(f"  ⚠️  {var} 为空字符串")
        else:
            print(f"  ✓ {var} 已设置")
    
    # 3. 检查Settings类
    print("\n=== Settings类配置 ===")
    settings_attrs = ['UNL_DOWNLOAD_URL', 'UNL_FILE_NAME_LIST', 'UNL_FILE_SVR_ID', 'UNL_RMT_PUB_PATH']
    for attr in settings_attrs:
        try:
            value = getattr(Settings, attr)
            print(f"Settings.{attr}: {value}")
            if not value:
                print(f"  ⚠️  Settings.{attr} 为空")
            else:
                print(f"  ✓ Settings.{attr} 已设置")
        except AttributeError:
            print(f"  ❌ Settings.{attr} 不存在")
    
    # 4. 测试DownloadUnlService
    print("\n=== DownloadUnlService测试 ===")
    try:
        service = DownloadUnlService()
        print("✓ DownloadUnlService实例创建成功")
        print(f"  download_url: {service.download_url}")
        print(f"  file_name_list: {service.file_name_list}")
        print(f"  file_svr_id: {service.file_svr_id}")
        print(f"  rmt_pub_path: {service.rmt_pub_path}")
        
        # 验证配置
        is_valid = service.validate_config()
        print(f"  配置验证结果: {is_valid}")
        
        if not is_valid:
            print("\n❌ 配置验证失败，具体原因:")
            if not service.download_url:
                print("   - download_url 为空")
            if not service.file_name_list:
                print("   - file_name_list 为空")
            if not service.file_svr_id:
                print("   - file_svr_id 为空")
            if not service.rmt_pub_path:
                print("   - rmt_pub_path 为空")
                
    except Exception as e:
        print(f"❌ DownloadUnlService创建失败: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # 5. 模拟实际调用场景
    print("\n=== 模拟实际调用场景 ===")
    try:
        # 模拟在不同目录下调用
        original_cwd = os.getcwd()
        
        # 测试在项目根目录
        print("在项目根目录测试:")
        os.chdir(original_cwd)
        from config.settings import Settings as RootSettings
        print(f"  UNL_RMT_PUB_PATH: {RootSettings.UNL_RMT_PUB_PATH}")
        
        # 测试在其他目录
        test_dirs = ['./scripts', './services', '.']
        for test_dir in test_dirs:
            if os.path.exists(test_dir):
                print(f"在 {test_dir} 目录测试:")
                os.chdir(test_dir)
                # 重新导入以确保环境变量重新加载
                import importlib
                import config.settings
                importlib.reload(config.settings)
                from config.settings import Settings as TestSettings
                print(f"  UNL_RMT_PUB_PATH: {TestSettings.UNL_RMT_PUB_PATH}")
                os.chdir(original_cwd)
                
    except Exception as e:
        print(f"目录切换测试出错: {str(e)}")
        os.chdir(original_cwd)

if __name__ == "__main__":
    detailed_diagnosis()