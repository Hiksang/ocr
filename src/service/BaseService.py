from datetime import datetime

class BaseService:
  """
  Repository Layer에 의존합니다.
  """
  def __init__(self, repository) :
    self._repository = repository

  def printDataAll(self) :
    """
    [모든 데이터를 격자 형태로 출력합니다.]
    """
    instances = self._repository.findAll()
    self.__validate(instances)
    self.__printGrid(instances)
  
  def printDataByDate(self, date=datetime.utcnow().date()) :
    """
    [주어진 날짜의 데이터를 격자 형태로 출력합니다.]
    Args:
        date (_type_, optional): _description_. Defaults to datetime.utcnow().date().
    """
    instances = self.repository.findByDate()
    self.__validate(instances)
    self.__printGrid(instances)
    
  def save(self, **kwargs) : 
    """
    [가장 기본적인 저장 메소드]
    example :
      userService = AppContext.get(UserStatus.USER_STATUS_SERVICE)
      userService.save(name="name", age=20 ... )
    """
    self._repository.save(**kwargs)
    
  def saveByDictionary(self, arg) :
    if type(arg) is not dict :
      print(f"[service] 딕셔너리 타입만 가능합니다.")
      return
    self._repository.save(**arg)
  
  def __printGrid(self, instances) :
    """
    [Entity를 받아서 실제로 격자로 출력합니다.]

    Args:
        instances (_type_): Entity Data
    """
    # 열 이름과 각 열의 데이터를 포함한 리스트를 생성합니다.
    headers = [column.name for column in self._repository.model.__table__.columns]
    rows = [[str(getattr(instance, col)) for col in headers] for instance in instances]

    # 각 열의 최대 너비를 계산합니다.
    column_widths = [max(map(len, [row[i] for row in rows] + [header])) for i, header in enumerate(headers)]

    # 헤더를 출력합니다.
    header_row = " | ".join([header.ljust(column_widths[i]) for i, header in enumerate(headers)])
    print(header_row)
    print("-" * len(header_row))

    # 데이터 행을 출력합니다.
    for row in rows:
      print(" | ".join([cell.ljust(column_widths[i]) for i, cell in enumerate(row)]))
  
  def __validate(self, instances) :
    if not instances:
      print("[service] No data available.")
      return
    

class UserStatusService(BaseService):
  def __init__(self, repository):
    super().__init__(repository)
    
class WorkTimeService(BaseService):
  def __init__(self, repository):
    super().__init__(repository)

class OperationRateService(BaseService):
  def __init__(self, repository):
    super().__init__(repository)

class ProductionRateService(BaseService):
  def __init__(self, repository):
    super().__init__(repository)
    
class ProductionContextService(BaseService):
  def __init__(self, repository):
    super().__init__(repository)
    
class ErrorContextService(BaseService):
  def __init__(self, repository):
    super().__init__(repository)
    
class SaleContextService(BaseService):
  def __init__(self, repository):
    super().__init__(repository)



