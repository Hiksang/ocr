# app_config.py
from .IocContainer import AppContext
from .database_util import DatabaseUtil
from ..repository.BaseRepository import (
    UserStatusRepository, WorkTimeRepository, OperationRateRepository,
    ProductionRateRepository, ProductionContextRepository, ErrorContextRepository, SaleContextRepository
)
from ..service.BaseService import (
    UserStatusService, WorkTimeService, OperationRateService, ProductionContextService,
    ProductionRateService, ProductionContextService, ErrorContextService, SaleContextService
)
from .ContextType import ( ServiceType, RepositoryType ) 

DATABASE_NAME = 'sqlite:///your_database.db'

# 데이터베이스 초기화
DatabaseUtil.initialize(DATABASE_NAME)

AppContext.register(RepositoryType.USER_STATUS_REPOSITORY, UserStatusRepository())
AppContext.register(RepositoryType.WORK_TIME_REPOSITORY, WorkTimeRepository())
AppContext.register(RepositoryType.OPERATION_RATE_REPOSITORY, OperationRateRepository())
AppContext.register(RepositoryType.PRODUCTION_RATE_REPOSITORY, ProductionRateRepository())
AppContext.register(RepositoryType.PRODUCTION_CONTEXT_REPOSITORY, ProductionContextRepository())
AppContext.register(RepositoryType.ERROR_CONTEXT_REPOSITORY, ErrorContextRepository())
AppContext.register(RepositoryType.SALE_CONTEXT_REPOSITORY, SaleContextRepository())

# 서비스 인스턴스 생성 및 IoC 컨테이너에 등록
AppContext.register(ServiceType.USER_STATUS_SERVICE, UserStatusService(AppContext.get(RepositoryType.USER_STATUS_REPOSITORY)))
AppContext.register(ServiceType.WORK_TIME_SERVICE, WorkTimeService(AppContext.get(RepositoryType.WORK_TIME_REPOSITORY)))
AppContext.register(ServiceType.OPERATION_RATE_SERVICE, OperationRateService(AppContext.get(RepositoryType.OPERATION_RATE_REPOSITORY)))
AppContext.register(ServiceType.PRODUCTION_RATE_SERVICE, ProductionRateService(AppContext.get(RepositoryType.PRODUCTION_RATE_REPOSITORY)))
AppContext.register(ServiceType.PRODUCTION_CONTEXT_SERVICE, ProductionContextService(AppContext.get(RepositoryType.PRODUCTION_CONTEXT_REPOSITORY)))
AppContext.register(ServiceType.ERROR_CONTEXT_SERVICE, ErrorContextService(AppContext.get(RepositoryType.ERROR_CONTEXT_REPOSITORY)))
AppContext.register(ServiceType.SALE_CONTEXT_SERVICE, SaleContextService(AppContext.get(RepositoryType.SALE_CONTEXT_REPOSITORY)))

