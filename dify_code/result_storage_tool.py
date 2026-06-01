"""
Dify工具：结果存储工具
功能：将处理结果存储到数据库
"""
import os
import logging
from typing import Dict, Any, List
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import Settings
from models.dify_result import DifyCallResult

logger = logging.getLogger(__name__)

# 使用连接池参数优化长期运行的连接管理
engine = create_engine(Settings.DATABASE_URL, pool_pre_ping=True, pool_recycle=300, pool_timeout=30, max_overflow=10)
SessionLocal = sessionmaker(bind=engine)


def store_dify_result_tool(task_id: int, upload_api_response: Dict[str, Any] = None, 
                          run_response: Dict[str, Any] = None, parsed_result: str = None, 
                          case_id: str = None) -> Dict[str, Any]:
    """
    Dify工具函数：将Dify处理结果存储到数据库
    
    Args:
        task_id: 任务ID
        upload_api_response: 上传API响应
        run_response: 工作流运行响应
        parsed_result: 解析结果
        case_id: 案例ID
    
    Returns:
        包含存储结果的字典
    """
    db_session = SessionLocal()
    
    try:
        # 创建结果记录
        result_record = DifyCallResult(
            task_id=task_id,
            upload_api_response=upload_api_response,
            run_response=run_response,
            parsed_result=parsed_result,
            case_id=case_id,
            status='completed' if run_response and run_response.get('success', False) else 'failed',
            execution_time=datetime.utcnow()
        )

        db_session.add(result_record)
        db_session.commit()
        
        logger.info(f"Dify结果已保存到数据库，记录ID: {result_record.id}")
        
        return {
            "success": True,
            "message": "结果已成功保存",
            "record_id": result_record.id
        }

    except Exception as e:
        logger.error(f"保存到数据库失败: {str(e)}")
        db_session.rollback()
        return {
            "success": False,
            "message": f"保存到数据库失败: {str(e)}"
        }

    finally:
        db_session.close()  # 会话关闭，连接归还到连接池


def query_dify_results_tool(task_id: int = None, case_id: str = None, limit: int = 100) -> Dict[str, Any]:
    """
    Dify工具函数：查询Dify处理结果
    
    Args:
        task_id: 任务ID
        case_id: 案例ID
        limit: 返回结果的最大数量
    
    Returns:
        包含查询结果的字典
    """
    db_session = SessionLocal()
    
    try:
        query = db_session.query(DifyCallResult)
        
        if task_id:
            query = query.filter(DifyCallResult.task_id == task_id)
        if case_id:
            query = query.filter(DifyCallResult.case_id == case_id)
        
        # 按执行时间倒序排列，取最新的结果
        results = query.order_by(DifyCallResult.execution_time.desc()).limit(limit).all()
        
        # 转换为字典列表
        result_list = []
        for result in results:
            result_list.append({
                'id': result.id,
                'task_id': result.task_id,
                'case_id': result.case_id,
                'parsed_result': result.parsed_result,
                'execution_time': result.execution_time.isoformat() if result.execution_time else None,
                'status': result.status
            })
        
        logger.info(f"查询到 {len(result_list)} 条Dify结果")
        
        return {
            "success": True,
            "message": f"查询成功，找到 {len(result_list)} 条记录",
            "results": result_list
        }
        
    except Exception as e:
        logger.error(f"查询数据库失败: {str(e)}")
        return {
            "success": False,
            "message": f"查询数据库失败: {str(e)}",
            "results": []
        }
        
    finally:
        db_session.close()


def batch_store_dify_results_tool(results_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Dify工具函数：批量存储Dify处理结果
    
    Args:
        results_data: 包含多个结果记录的列表
    
    Returns:
        包含批量存储结果的字典
    """
    db_session = SessionLocal()
    
    success_count = 0
    failed_count = 0
    
    try:
        for result_data in results_data:
            try:
                # 提取参数
                task_id = result_data.get('task_id')
                upload_api_response = result_data.get('upload_api_response')
                run_response = result_data.get('run_response')
                parsed_result = result_data.get('parsed_result')
                case_id = result_data.get('case_id')
                
                # 创建结果记录
                result_record = DifyCallResult(
                    task_id=task_id,
                    upload_api_response=upload_api_response,
                    run_response=run_response,
                    parsed_result=parsed_result,
                    case_id=case_id,
                    status='completed' if run_response and run_response.get('success', False) else 'failed',
                    execution_time=datetime.utcnow()
                )

                db_session.add(result_record)
                success_count += 1
            except Exception as e:
                logger.error(f"添加单个记录失败: {str(e)}")
                failed_count += 1
        
        # 一次性提交所有更改
        db_session.commit()
        
        logger.info(f"批量存储完成，成功: {success_count}，失败: {failed_count}")
        
        return {
            "success": True,
            "message": f"批量存储完成，成功: {success_count}，失败: {failed_count}",
            "success_count": success_count,
            "failed_count": failed_count
        }

    except Exception as e:
        logger.error(f"批量保存到数据库失败: {str(e)}")
        db_session.rollback()
        return {
            "success": False,
            "message": f"批量保存到数据库失败: {str(e)}",
            "success_count": 0,
            "failed_count": len(results_data)
        }

    finally:
        db_session.close()


if __name__ == "__main__":
    # 示例调用
    result = store_dify_result_tool(
        task_id=1,
        upload_api_response={"status": 200},
        run_response={"success": True},
        parsed_result="Sample parsed result",
        case_id="CASE001"
    )
    print(result)