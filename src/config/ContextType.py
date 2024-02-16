from enum import Enum, auto

class ServiceType(Enum):
  USER_STATUS_SERVICE = auto()
  WORK_TIME_SERVICE = auto()
  OPERATION_RATE_SERVICE = auto()
  PRODUCTION_RATE_SERVICE = auto()
  PRODUCTION_CONTEXT_SERVICE = auto()
  ERROR_CONTEXT_SERVICE = auto()
  SALE_CONTEXT_SERVICE = auto()

class RepositoryType(Enum):
  USER_STATUS_REPOSITORY = auto()
  WORK_TIME_REPOSITORY = auto()
  OPERATION_RATE_REPOSITORY = auto()
  PRODUCTION_RATE_REPOSITORY = auto()
  PRODUCTION_CONTEXT_REPOSITORY = auto()
  ERROR_CONTEXT_REPOSITORY = auto()
  SALE_CONTEXT_REPOSITORY = auto()