from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,  Date
from sqlalchemy import create_engine
from datetime import datetime

# SQLite 데이터베이스에 연결하는 엔진 생성
engine = create_engine('sqlite:///example.db', echo=True)

Base = declarative_base()

class UserStatus(Base):
  __tablename__ = 'user_statuses'  # 테이블 이름 수정

  id = Column(Integer, primary_key=True)
  first = Column(String)
  second = Column(String)
  midnight = Column(String)
  absent = Column(String)
  training = Column(String)  
  etc = Column(String)
  rest = Column(String)
  early = Column(String)
  date = Column(Date, default=datetime.utcnow)

  def __repr__(self):
      return f"<UserStatus(id={self.id})>"

class WorkTime(Base):
  __tablename__ = 'work_time'
  
  id = Column(Integer, primary_key=True)
  unit_number = Column(Integer)
  normal = Column(String)
  overtime = Column(String)
  date = Column(Date, default=datetime.utcnow)
  
  def __repr__(self):
      return f"<WorkTime(id={self.id}, unit_number={self.unit_number})>"

class OperationRate(Base):
  __tablename__ = 'operation_rate'
  
  id = Column(Integer, primary_key=True)
  unit_number = Column(Integer)
  today = Column(String)
  date = Column(Date, default=datetime.utcnow)
  
  def __repr__(self):
      return f"<OperationRate(id={self.id}, unit_number={self.unit_number})>"

class ProductionRate(Base):
  __tablename__ = 'production_rate'
  
  id = Column(Integer, primary_key=True)
  unit_number = Column(Integer)
  today = Column(String)
  date = Column(Date, default=datetime.utcnow)
  
  def __repr__(self):
      return f"<ProductionRate(id={self.id}, unit_number={self.unit_number})>"

class ProductionContext(Base):  # Base 상속 추가
  __tablename__ = 'production_context'
  
  id = Column(Integer, primary_key=True)
  unit_number = Column(Integer)
  width = Column(String)
  texture = Column(String)
  input = Column(String)
  outer_diameter = Column(String)
  thickness = Column(String)
  length = Column(String)
  count = Column(String)
  weight = Column(String)
  date = Column(Date, default=datetime.utcnow)
  
  def __repr__(self):
      return f"<ProductionContext(id={self.id}, unit_number={self.unit_number})>"

class ErrorContext(Base):  # Base 상속 추가
  __tablename__ = 'error_context'
  
  id = Column(Integer, primary_key=True)
  unit_number = Column(Integer)
  test = Column(String)
  production = Column(String)
  outer_diameter = Column(String)
  thickness = Column(String)
  length = Column(String)
  count = Column(String)
  weight = Column(String)
  date = Column(Date, default=datetime.utcnow)
  
  def __repr__(self):
      return f"<ErrorContext(id={self.id}, unit_number={self.unit_number})>"

class SaleContext(Base):  # Base 상속 추가
  __tablename__ = 'sale_context'
  
  id = Column(Integer, primary_key=True)
  department = Column(String)
  unit_number = Column(Integer)
  texture = Column(String)
  outer_diameter = Column(String)
  thickness = Column(String)
  length = Column(String)
  count = Column(String)
  weight = Column(String)
  per_price = Column(String)
  date = Column(Date, default=datetime.utcnow)
  
  def __repr__(self):
    return f"<SaleContext(id={self.id}, unit_number={self.unit_number})>"