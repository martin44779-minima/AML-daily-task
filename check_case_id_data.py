from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import Settings
from models.dify_result import DifyCallResult

def check_case_id_data():
    engine = create_engine(Settings.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # 查询所有不同的case_id值，查看前20个
        results = session.query(DifyCallResult.case_id).distinct().limit(20).all()
        print('数据库中不同的case_id值:')
        for i, (case_id,) in enumerate(results):
            if case_id:
                print(f'{i+1}. repr: {repr(case_id)}, str: {str(case_id)}')
            else:
                print(f'{i+1}. None value')
        
        print('\n' + '='*50)
        
        # 查询包含CASE001的记录
        case001_results = session.query(DifyCallResult).filter(
            DifyCallResult.case_id.like('%CASE001%')
        ).limit(5).all()
        
        if case001_results:
            print('找到包含CASE001的记录:')
            for i, result in enumerate(case001_results):
                print(f'{i+1}. ID: {result.id}, case_id repr: {repr(result.case_id)}, str: {str(result.case_id)}')
        else:
            print('没有找到包含CASE001的记录')
        
        print('\n' + '='*50)
        
        # 检查是否所有case_id都是column_0格式（由我们修改后的无列名处理逻辑产生）
        column_results = session.query(DifyCallResult).filter(
            DifyCallResult.case_id.like('column_%')
        ).limit(5).all()
        
        if column_results:
            print('找到column_x格式的case_id记录（可能由无列名CSV处理逻辑产生）:')
            for i, result in enumerate(column_results):
                print(f'{i+1}. ID: {result.id}, case_id: {result.case_id}')
        
        print('\n' + '='*50)
        
        # 检查前几个记录的实际情况
        first_results = session.query(DifyCallResult).limit(5).all()
        print('前5个记录的详细情况:')
        for i, result in enumerate(first_results):
            print(f'{i+1}. ID: {result.id}, case_id repr: {repr(result.case_id)}, parsed_result length: {len(str(result.parsed_result)) if result.parsed_result else 0}')

    finally:
        session.close()
        engine.dispose()

if __name__ == "__main__":
    check_case_id_data()