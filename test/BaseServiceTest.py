import src.config.IocConfig
from src.config.IocContainer import AppContext
from src.config.ContextType import ( RepositoryType, ServiceType )
from src.config.database_util import DatabaseUtil


def testData() :
  userService = AppContext.get(ServiceType.USER_STATUS_SERVICE)
  userService.save(first="test1", second="N3123o", midnight="No", absent="Yes", training="321312No", etc="Yes", rest="N3123o", early="Yes")
  userService.save(first="test1", second="N3123o", midnight="N23o", absent="Yes", training="No", etc="Yes", rest="No", early="Yes")
  userService.save(first="test1", second="N321o", midnight="32No", absent="Yes", training="No", etc="Yes", rest="No", early="Yes")
  userService.save(first="test1", second="N321o", midnight="N323o", absent="Ye321s", training="No", etc="Yes", rest="No", early="Yes")

def testData2() :
  data = {
    "first": "test2", 
    'second':"N3123o",
    'midnight':"No", 
    'absent':"Yes", 
    'training':"321312No", 
    'etc':"Yes", 
    'rest':"N3123o", 
    'early':"Yes"
  }
  userService = AppContext.get(ServiceType.USER_STATUS_SERVICE)
  userService.saveByDictionary(data)
  
def db_WorkTime(data):
    userService = AppContext.get(ServiceType.WORK_TIME_SERVICE)
    userService.saveByDictionary(data)

  
def printData() :
  userService = AppContext.get(ServiceType.USER_STATUS_SERVICE)
  userService.printDataAll()

if __name__ == "__main__":
  DatabaseUtil.clear_all_data()
  # testData()
  # testData2()
  # printData()
  db_WorkTime