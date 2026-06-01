"""
Dify工具：工作流调用工具
功能：调用Dify工作流API处理数据
"""
import os
import requests
import json
import logging
from typing import Dict, Any, Optional
from config.settings import Settings

logger = logging.getLogger(__name__)


def call_dify_workflow_tool(file_content: str, case_id: str = "unknown", workflow_run_endpoint: str = None, api_key: str = None) -> Dict[str, Any]:
    """
    Dify工具函数：调用Dify工作流API处理单个数据
    
    Args:
        file_content: 要处理的文件内容（通常是CSV格式的单行数据）
        case_id: 案例ID，用于追踪交易流水号
        workflow_run_endpoint: 工作流运行端点URL
        api_key: Dify API密钥
    
    Returns:
        包含工作流调用结果的字典
    """
    try:
        # 从环境变量或参数获取配置
        if not workflow_run_endpoint:
            api_endpoint = os.getenv('DIFY_API_ENDPOINT', 'http://localhost:5000/v1')
            workflow_run_endpoint = f"{api_endpoint}/workflows/run"
        
        if not api_key:
            api_key = os.getenv('DIFY_API_KEY', '')

        if not api_key:
            logger.error("错误：缺少DIFY_API_KEY环境变量或api_key参数")
            return {
                "success": False,
                "message": "缺少API密钥",
                "result": None
            }

        # 准备上传的文件（单行数据）
        import io
        import tempfile
        
        # 创建临时文件来存储单行数据
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8') as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name

        try:
            # 第一步：上传文件
            headers = {
                'Authorization': f'Bearer {api_key}'
            }
            
            with open(temp_file_path, 'rb') as f:
                files = {
                    'file': (f'data_row_{case_id}.csv', f, 'text/csv')
                }
                
                # 准备表单数据
                data = {'case_id': case_id}
                
                upload_response = requests.post(
                    f"{workflow_run_endpoint.replace('/workflows/run', '/files/upload')}",
                    headers=headers,
                    files=files,
                    data=data
                )
                
                logger.info(f"文件上传结果 (案例 {case_id}): {upload_response.status_code}")
                
                if upload_response.status_code not in [200, 201]:
                    return {
                        "success": False,
                        "message": f"文件上传失败，状态码: {upload_response.status_code}",
                        "result": None
                    }
                
                # 解析上传响应以获取文件ID
                upload_response_data = upload_response.json()
                file_id = upload_response_data.get('id')
                
                if not file_id:
                    # 如果直接获取不到，尝试解析content字段中的JSON
                    try:
                        content_str = upload_response.text
                        content_data = json.loads(content_str)
                        file_id = content_data.get('id')
                    except json.JSONDecodeError:
                        logger.error(f"无法从响应中解析文件ID (案例 {case_id})")
                        return {
                            "success": False,
                            "message": "无法从上传响应中解析文件ID",
                            "result": None
                        }
                
                if file_id:
                    logger.info(f"获取到上传文件ID: {file_id} (案例 {case_id})")
                    
                    # 构建工作流运行请求
                    workflow_headers = {
                        'Authorization': f'Bearer {api_key}',
                        'Content-Type': 'application/json'
                    }
                    
                    workflow_data = {
                        "inputs": {
                            "AML_message": {
                                "transfer_method": "local_file",
                                "upload_file_id": file_id,
                                "type": "document"
                            },
                            "case_id": case_id  # 添加案例ID到输入
                        },
                        "response_mode": "blocking",  # 使用阻塞模式以便获得即时结果
                        "user": os.getenv('DIFY_USER', 'aml_system')
                    }
                    
                    # 调用工作流运行接口
                    workflow_response = requests.post(
                        workflow_run_endpoint,
                        headers=workflow_headers,
                        json=workflow_data
                    )
                    
                    logger.info(f"工作流运行结果 (案例 {case_id}): {workflow_response.status_code}")
                    
                    if workflow_response.status_code == 200:
                        # 成功执行工作流
                        response_data = workflow_response.json()
                        
                        # 提取结果，特别是 outputs.RES 的值
                        outputs = response_data.get('data', {}).get('outputs', {})
                        res_value = outputs.get('RES')
                        
                        return {
                            "success": True,
                            "message": "工作流执行成功",
                            "result": {
                                "status_code": workflow_response.status_code,
                                "content": workflow_response.text,
                                "headers": dict(workflow_response.headers),
                                "url": workflow_response.url,
                                "outputs": outputs,
                                "parsed_result": res_value  # 这是最重要的结果
                            }
                        }
                    else:
                        return {
                            "success": False,
                            "message": f"工作流执行失败，状态码: {workflow_response.status_code}",
                            "result": {
                                "status_code": workflow_response.status_code,
                                "content": workflow_response.text
                            }
                        }
                else:
                    logger.warning(f"未能获取文件ID，跳过工作流运行 (案例 {case_id})")
                    return {
                        "success": False,
                        "message": "未能获取文件ID",
                        "result": None
                    }
                    
        finally:
            # 清理临时文件
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    except Exception as e:
        logger.error(f"工作流调用失败 (案例 {case_id}): {str(e)}")
        return {
            "success": False,
            "message": f"工作流调用失败: {str(e)}",
            "result": None
        }


def parse_workflow_result_tool(workflow_response_data: Dict[str, Any]) -> Any:
    """
    Dify工具函数：解析工作流结果，提取 outputs.RES 的值
    
    Args:
        workflow_response_data: 工作流响应数据
        
    Returns:
        解析后的结果，通常是 outputs.RES 的值
    """
    if not workflow_response_data:
        return None

    try:
        # 解析 content 字段中的 JSON 字符串
        content_str = workflow_response_data.get('content', '{}')
        content_data = json.loads(content_str)

        # 提取 outputs.RES
        outputs = content_data.get('data', {}).get('outputs', {})
        res_value = outputs.get('RES')

        # 递归处理 unicode 转义
        res_value = _handle_unicode_in_dict(res_value)
        return res_value

    except Exception as e:
        # 解析失败时，返回 None 或原始数据
        logger.error(f"解析工作流结果异常: {e}")
        return None


def _handle_unicode_in_dict(data):
    """递归处理字典、列表或字符串中的 Unicode 转义序列"""
    if isinstance(data, str):
        # 若字符串包含 \uXXX 转义形式，解码一次
        if "\\u" in data:
            try:
                # 用 JSON 处理 Unicode 转义更安全
                return json.loads(f'"{data}"')
            except json.JSONDecodeError:
                # 备用方案：直接用 unicode_escape 解码
                return data.encode('utf-8').decode('unicode_escape')
        else:
            return data  # 已是正常中文，直接返回

    elif isinstance(data, dict):
        return {k: _handle_unicode_in_dict(v) for k, v in data.items()}

    elif isinstance(data, list):
        return [_handle_unicode_in_dict(v) for v in data]

    else:
        return data


if __name__ == "__main__":
    # 示例调用
    sample_content = "case123,张三,1000.00,2023-01-01"
    result = call_dify_workflow_tool(file_content=sample_content, case_id="case123")
    print(json.dumps(result, ensure_ascii=False, indent=2))