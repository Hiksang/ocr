from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from ..domain.models import Base  # 모델 파일에서 Base 임포트

class DatabaseUtil:
  _engine = None
  _session_factory = None
  _scoped_session = None

  @classmethod
  def initialize(cls, db_url, echo=False):
    '''
    [최초 Initial]
    Application Loading Time에 한 번만 호출
    '''
    if cls._engine is None:
      cls._engine = create_engine(db_url, echo=echo)
      cls._session_factory = sessionmaker(bind=cls._engine)
      cls._scoped_session = scoped_session(cls._session_factory)
      
      Base.metadata.create_all(cls._engine)

  @classmethod
  def get_session(cls):
    '''
    [Scopre Thread]
    동일한 스레드 내에서는 같은 세션을 반환
    '''
    return cls._scoped_session()

  @classmethod
  def close_session(cls):
    cls._scoped_session.remove()
    
  @classmethod
  def clear_all_data(cls):
    """
    [Delete All Data]
    데이터베이스의 모든 테이블에서 모든 데이터를 삭제
    """
    session = cls.get_session()
    for table in reversed(Base.metadata.sorted_tables):
      session.execute(table.delete())
    session.commit()
