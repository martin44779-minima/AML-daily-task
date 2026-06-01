#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试UNL环境变量配置加载
"""

import os
import sys
from config.settings import Settings
from services.download_unl_service import DownloadUnlService

def test_env_loading():
    """测试环境变量加载情况"""
    print("=== 环境变量加载测试 ===")
    
    # 直接从环境变量读取
    print("1. 直接从os.environ读取:")
    print(f"   UNL_DOWNLOAD_URL: {os.getenv('UNL_DOWNLOAD_URL', 'NOT SET')}")
    print(f"   UNL_FILE_NAME_LIST: {os.getenv('UNL_FILE_NAME_LIST', 'NOT SET')}")
    print(f"   UNL_FILE_SVR_ID: {os.getenv('UNL_FILE_SVR_ID', 'NOT SET')}")
    print(f"   UNL_RMT_PUB_PATH: {os.getenv('UNL_RMT_PUB_PATH', 'NOT SET')}")
    
    # 从Settings类读取
    print("\n2. 从Settings类读取:")
    print(f"   UNL_DOWNLOAD_URL: {Settings.UNL_DOWNLOAD_URL}")
    print(f"   UNL_FILE_NAME_LIST: {Settings.UNL_FILE_NAME_LIST}")
    print(f"   UNL_FILE_SVR_ID: {Settings.UNL_FILE_SVR_ID}")
    print(f"   UNL_RMT_PUB_PATH: {Settings.UNL_RMT_PUB_PATH}")
    
    # 测试DownloadUnlService
    print("\n3. DownloadUnlService实例配置:")
    service = DownloadUnlService()
    print(f"   download_url: {service.download_url}")
    print(f"   file_name_list: {service.file_name_list}")
    print(f"   file_svr_id: {service.file_svr_id}")
    print(f"   rmt_pub_path: {service.rmt_pub_path}")
    
    # 验证配置
    print("\n4. 配置验证结果:")
    is_valid = service.validate_config()
    print(f"   配置是否有效: {is_valid}")
    
    if not is_valid:
        print("\n❌ 配置存在问题，请检查以下项:")
        if not service.download_url:
            print("   - UNL_DOWNLOAD_URL 未配置或为空")
        if not service.file_name_list:
            print("   - UNL_FILE_NAME_LIST 未配置或为空")
        if not service.file_svr_id:
            print("   - UNL_FILE_SVR_ID 未配置或为空")
        if not service.rmt_pub_path:
            print("   - UNL_RMT_PUB_PATH 未配置或为空")

if __name__ == "__main__":
    test_env_loading()