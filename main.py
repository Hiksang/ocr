import tb.OcrToTableTool as ottt
import tb.TableExtractor as te
import tb.TableLinesRemover as tlr
import cv2
import ReadTable as rt
import src.config.IocConfig
from src.config.IocContainer import AppContext
from src.config.ContextType import ( RepositoryType, ServiceType )
from src.config.database_util import DatabaseUtil



path_to_image = "./figure/0.jpg"

def Table_ex(table_name, table):
    
    table_extractor = te.TableExtractor(table)
    perspective_corrected_image = table_extractor.execute()
    gray = cv2.cvtColor(perspective_corrected_image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5,5,), 0)
    edged = cv2.Canny(blurred, 75, 200)
    
    cv2.imwrite(f'./tmp_figure/{table_name}.jpg', perspective_corrected_image)
    

    return perspective_corrected_image


def db_USER_STATUS_SERVICE(data):
    userService = AppContext.get(ServiceType.USER_STATUS_SERVICE)
    userService.saveByDictionary(data)

def db_WORK_TIME_SERVICE(data):
    userService = AppContext.get(ServiceType.WORK_TIME_SERVICE)
    userService.saveByDictionary(data)
    
def db_OPERATION_SERVICE(data):
    userService = AppContext.get(ServiceType.OPERATION_RATE_SERVICE)
    userService.saveByDictionary(data)

def db_PRODUCTION_SERVICE(data):
    userService = AppContext.get(ServiceType.PRODUCTION_RATE_SERVICE)
    userService.saveByDictionary(data)

def db_PRODUCTION_CONTEXT_SERVICE(data):
    userService = AppContext.get(ServiceType.PRODUCTION_CONTEXT_SERVICE)
    userService.saveByDictionary(data)

def db_ERROR_CONTEXT_SERVICE(data):
    userService = AppContext.get(ServiceType.ERROR_CONTEXT_SERVICE)
    userService.saveByDictionary(data)

def db_SALE_CONTEXT_SERVICE(data):
    userService = AppContext.get(ServiceType.SALE_CONTEXT_SERVICE)
    userService.saveByDictionary(data)


def printData() :
    userService = AppContext.get(ServiceType.USER_STATUS_SERVICE)
    userService.printDataAll()
    print('*'*20)
    userService = AppContext.get(ServiceType.WORK_TIME_SERVICE)
    userService.printDataAll()
    print('*'*20)
    userService = AppContext.get(ServiceType.OPERATION_RATE_SERVICE)
    userService.printDataAll()
    print('*'*20)
    userService = AppContext.get(ServiceType.PRODUCTION_RATE_SERVICE)
    userService.printDataAll()
    print('*'*20)
    userService = AppContext.get(ServiceType.PRODUCTION_CONTEXT_SERVICE)
    userService.printDataAll()
    print('*'*20)
    userService = AppContext.get(ServiceType.ERROR_CONTEXT_SERVICE)
    userService.printDataAll()
    print('*'*20)
    userService = AppContext.get(ServiceType.SALE_CONTEXT_SERVICE)
    userService.printDataAll()
    
def update_value(dict):
    for key, value in dict.items():
        if len(value) == 0:
            dict[key] = 'None'
        else:
            dict[key] = value[0]
    return dict

if __name__=='__main__':
    
    ## 이미지에서 테이블 분리
    dict_table = rt.ReadDailyTable(path_to_image).execute()
    ## 분리된 테이블에서 테이블만 저장
    img_dict = {}
    
    for keys in dict_table:
        # print(keys)
        img = Table_ex(keys, dict_table[keys])
        img_dict[keys] = img
        
    ocr = rt.setting_ocr()
    
    result_UserStatus = ocr.ocr_UserStatus(img_dict['user_statuses'])
    result_WorkTime_unit_1, result_WorkTime_unit_2  = ocr.ocr_WorkTime(img_dict['work_time'])
    result_operation_unit_1, result_operation_unit_2, result_production_unit_1, result_production_unit_2 = ocr.ocr_WorkYeild(img_dict['work_yeild'])
    result_ProductionContext_unit_1, result_ProductionContext_unit_2 = ocr.ocr_ProductionContext(img_dict['production_context'])
    result_ErrorContext_unit_1, result_ErrorContext_unit_2  = ocr.ocr_ErrorContext(img_dict['error_context'])
    result_SaleContext_11,result_SaleContext_12, result_SaleContext_21, result_SaleContext_22  = ocr.ocr_SaleContext(img_dict['sale_context'])

    DatabaseUtil.clear_all_data()

    db_USER_STATUS_SERVICE(update_value(result_UserStatus))
    
    db_WORK_TIME_SERVICE(update_value(result_WorkTime_unit_1))
    db_WORK_TIME_SERVICE(update_value(result_WorkTime_unit_2))
    
    db_OPERATION_SERVICE(update_value(result_operation_unit_1))
    db_OPERATION_SERVICE(update_value(result_operation_unit_2))
    
    db_PRODUCTION_SERVICE(update_value(result_production_unit_1))
    db_PRODUCTION_SERVICE(update_value(result_production_unit_2))
    
    db_PRODUCTION_CONTEXT_SERVICE(update_value(result_ProductionContext_unit_1))
    db_PRODUCTION_CONTEXT_SERVICE(update_value(result_ProductionContext_unit_2))
    
    db_ERROR_CONTEXT_SERVICE(update_value(result_ErrorContext_unit_1))
    db_ERROR_CONTEXT_SERVICE(update_value(result_ErrorContext_unit_2))
    
    db_SALE_CONTEXT_SERVICE(update_value(result_SaleContext_11))
    db_SALE_CONTEXT_SERVICE(update_value(result_SaleContext_12))
    db_SALE_CONTEXT_SERVICE(update_value(result_SaleContext_21))
    db_SALE_CONTEXT_SERVICE(update_value(result_SaleContext_22))
    
    printData()
