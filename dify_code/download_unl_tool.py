"""
Dify工具：UNL文件下载工具
功能：从远程服务器下载UNL格式的压缩文件
"""
import os
import requests
import logging
from typing import List, Dict, Any
from urllib.parse import urlparse
import tempfile

logger = logging.getLogger(__name__)


def download_unl_files_tool() -> Dict[str, Any]:
    """
    Dify工具函数：下载UNL文件
    
    Returns:
        包含下载结果的字典
    """
    try:
        # 从环境变量获取配置
        download_url = os.getenv('UNL_DOWNLOAD_URL', '')
        file_name_list = os.getenv('UNL_FILE_NAME_LIST', '').split(',') if os.getenv('UNL_FILE_NAME_LIST') else []
        file_svr_id = os.getenv('UNL_FILE_SVR_ID', '')
        rmt_pub_path = os.getenv('UNL_RMT_PUB_PATH', '')
        
        # 验证配置
        if not download_url:
            return {
                "success": False,
                "message": "未配置UNL_DOWNLOAD_URL环境变量",
                "files": []
            }
        if not file_name_list:
            return {
                "success": False,
                "message": "未配置UNL_FILE_NAME_LIST环境变量",
                "files": []
            }
        if not file_svr_id:
            return {
                "success": False,
                "message": "未配置UNL_FILE_SVR_ID环境变量",
                "files": []
            }
        if not rmt_pub_path:
            return {
                "success": False,
                "message": "未配置UNL_RMT_PUB_PATH环境变量",
                "files": []
            }

        # 准备POST请求体
        payload = {
            "fileNameList": file_name_list,
            "fileSvrId": file_svr_id,
            "rmtPubPath": rmt_pub_path
        }

        logger.info(f"开始下载UNL文件，请求URL: {download_url}")
        logger.info(f"请求参数: fileNameList={file_name_list}, fileSvrId={file_svr_id}, rmtPubPath={rmt_pub_path}")

        # 发送POST请求
        response = requests.post(
            url=download_url,
            json=payload,
            headers={
                'Content-Type': 'application/json'
            },
            timeout=300  # 设置5分钟超时
        )

        if response.status_code != 200:
            logger.error(f"下载请求失败，状态码: {response.status_code}, 响应: {response.text}")
            return {
                "success": False,
                "message": f"下载请求失败，状态码: {response.status_code}",
                "files": []
            }

        # 检查响应内容类型
        content_type = response.headers.get('Content-Type', '')
        logger.info(f"响应内容类型: {content_type}")

        # 保存响应内容到临时文件
        downloaded_files = []
        
        # 如果响应是二进制内容（如压缩文件），直接保存
        if ('application/gzip' in content_type or 
            'application/x-gzip' in content_type or 
            response.content[:2] == b'\x1f\x8b'):
            # 生成唯一的临时文件名
            temp_dir = os.getenv('CSV_PROCESSING_TEMP_DIR', './temp_csv_processing')
            os.makedirs(temp_dir, exist_ok=True)
            
            filename = f"downloaded_{file_svr_id}_{len(file_name_list)}files_{os.getpid()}_{abs(hash(str(file_name_list)))}.unl.gz"
            filepath = os.path.join(temp_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"UNL文件已保存到: {filepath}")
            downloaded_files.append(filepath)
        else:
            # 如果响应是JSON格式，可能是包含了文件下载链接或其他信息
            try:
                json_response = response.json()
                logger.info(f"接收到JSON响应: {json_response}")
                
                # 尝试从JSON响应中提取文件URL并下载
                if 'fileUrl' in json_response or 'downloadUrl' in json_response:
                    file_urls = []
                    if 'fileUrl' in json_response:
                        file_urls = [json_response['fileUrl']] if isinstance(json_response['fileUrl'], str) else json_response['fileUrl']
                    elif 'downloadUrl' in json_response:
                        file_urls = [json_response['downloadUrl']] if isinstance(json_response['downloadUrl'], str) else json_response['downloadUrl']
                    
                    for idx, file_url in enumerate(file_urls):
                        downloaded_file = _download_from_url(file_url, f"downloaded_file_{idx}.unl.gz")
                        if downloaded_file:
                            downloaded_files.append(downloaded_file)
            except Exception as e:
                logger.error(f"解析JSON响应失败: {str(e)}")
                return {
                    "success": False,
                    "message": f"解析JSON响应失败: {str(e)}",
                    "files": []
                }

        return {
            "success": True,
            "message": f"成功下载 {len(downloaded_files)} 个文件",
            "files": downloaded_files
        }

    except requests.exceptions.Timeout:
        logger.error(f"下载UNL文件超时")
        return {
            "success": False,
            "message": "下载UNL文件超时",
            "files": []
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"下载UNL文件请求异常: {str(e)}")
        return {
            "success": False,
            "message": f"下载UNL文件请求异常: {str(e)}",
            "files": []
        }
    except Exception as e:
        logger.error(f"下载UNL文件过程中发生未知错误: {str(e)}")
        return {
            "success": False,
            "message": f"下载UNL文件过程中发生未知错误: {str(e)}",
            "files": []
        }


def _download_from_url(file_url: str, filename: str) -> str:
    """从指定URL下载文件"""
    try:
        response = requests.get(file_url, timeout=300)
        if response.status_code == 200:
            temp_dir = os.getenv('CSV_PROCESSING_TEMP_DIR', './temp_csv_processing')
            os.makedirs(temp_dir, exist_ok=True)
            
            filepath = os.path.join(temp_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"文件已从 {file_url} 下载到 {filepath}")
            return filepath
        else:
            logger.error(f"从 {file_url} 下载文件失败，状态码: {response.status_code}")
            return ""
    except Exception as e:
        logger.error(f"从 {file_url} 下载文件时发生错误: {str(e)}")
        return ""


if __name__ == "__main__":
    # 示例调用
    result = download_unl_files_tool()
    print(result)