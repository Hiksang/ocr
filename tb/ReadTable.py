import cv2
import easyocr

class ReadDailyTable:
    
    def __init__(self, image_path):
        self.image_path = image_path
        
    def execute(self):
        self.read_image()
        self.TableSeparator()
        
        return self.dict_table
    
    def read_image(self):
        self.image = cv2.imread(self.image_path)
        
    def TableSeparator(self):
        img = self.image
        self.user_statuses = img[220:300, 150:1500]
        self.work_time = img[320:430, 300:850]
        self.work_yeild = img[300:430, 850:1500]
        self.production_context = img[435:790, 150:1500]
        self.error_context = img[795:1060, 150:1500]
        self.sale_context = img[1095:2265, 150:1500]
        self.list_table = [self.user_statuses, self.work_time, self.work_yeild,
                           self.production_context,
                           self.error_context, self.sale_context]
        self.dict_table = {
            'user_statuses': self.user_statuses,
            'work_time': self.work_time,
            'work_yeild': self.work_yeild,
            'production_context': self.production_context,
            'error_context': self.error_context,
            'sale_context': self.sale_context
        }
        
class setting_ocr:
    
    reader = easyocr.Reader(['ko', 'en']) 

    def cut_roi(self, img, coor_list):
        x = coor_list[0]
        y = coor_list[1]
        w = coor_list[2]
        h = coor_list[3]
        return img[y:y+h, x:x+w]
    
    def do_ocr(self, img):
        result = self.reader.readtext(img, detail=0)
        return result
    
    def cut_ocr(self, img, coor_list):
        
        img = self.cut_roi(img, coor_list)
        result = self.do_ocr(img)
        
        return result
        
        
    
    def ocr_UserStatus(self, img):
        first = [245, 47, 84, 35]
        second = [332, 45, 90, 37]
        midnight = [424, 46, 99, 36]
        absent = [526, 46, 105, 36]
        training = [630, 46, 105, 36]
        etc = [735, 46, 105, 36]
        rest = [844, 46, 98, 36]
        early = [945, 46, 260, 36]


        self.UserStatus_dict = {'first' : self.cut_ocr(img, first),
                                'second' : self.cut_ocr(img,second),
                                'midnight' : self.cut_ocr(img,midnight),
                                'absent' : self.cut_ocr(img,absent),
                                'training' : self.cut_ocr(img,training),
                                'etc' : self.cut_ocr(img,etc),
                                'rest' : self.cut_ocr(img,rest),
                                'early' : self.cut_ocr(img,early)}
        
        return self.UserStatus_dict
    
    def ocr_WorkTime(self, img):
        unit_number = 1 
        normal_unit_1 = [93, 25, 64, 17]
        overtime_unit_1 = [193, 42, 64, 20]

        unit_number = 2
        normal_unit_2 = [261, 24, 68, 17]
        overtime_unit_2 = [261, 42,  64, 20]
        
        self.WorkTime_dict_unit_1 = {
            'unit_number' : "1",
            'normal' : self.cut_ocr(img, normal_unit_1),
            'overtime' : self.cut_ocr(img, overtime_unit_1),
           
        }
        self.WorkTime_dict_unit_2 = {
            'unit_number' : "2",
            'normal' : self.cut_ocr(img, normal_unit_2),
            'overtime' : self.cut_ocr(img, overtime_unit_2)
        }
        
        return self.WorkTime_dict_unit_1, self.WorkTime_dict_unit_2
        
        
    def ocr_WorkYeild(self, img):

        # operationrate
        today_operate_unit_1 = [85, 60, 105, 30]
        today_operate_unit_2 = [85, 90, 105, 25]

        # productionrate
        today_product_unit_1 = [300, 65, 104, 26]
        today_product_unit_2 = [300, 95, 104, 26]
        
        self.operation_dict_unit_1 = {
            'unit_number' : '1',
            'today' : self.cut_ocr(img, today_operate_unit_1)
        }
        
        self.operation_dict_unit_2 = {
            'unit_number' : '2',
            'today' : self.cut_ocr(img, today_operate_unit_2),
        }
        
        self.production_dict_unit_1 = {
            'unit_number' : '1',
            'today' : self.cut_ocr(img, today_product_unit_1)
        }
        
        self.production_dict_unit_2 = {
            'unit_number' : '2',
            'today' : self.cut_ocr(img, today_product_unit_2)
        }
        return self.operation_dict_unit_1, self.operation_dict_unit_2, self.production_dict_unit_1, self.production_dict_unit_2
    
    
    def ocr_ProductionContext(self, img):

        width_unit_1 = [141, 78, 102, 24]
        texture_unit_1 = [246, 78, 84, 24]
        input_unit_1 = [333, 78, 86, 24]
        outer_diameter_unit_1 = [430, 78, 92, 24]
        thickness_unit_1 = [527, 81, 112, 24]
        length_unit_1 = [642, 81, 98, 24]
        count_unit_1 = [744, 81, 98, 24]
        weight_unit_1 = [844, 81, 100, 24]

        width_unit_2 = [141, 250, 101, 21]
        texture_unit_2 = [246, 250, 83, 21]
        input_unit_2 = [332, 250, 90, 21]
        outer_diameter_unit_2 = [425, 250, 100, 21]
        thickness_unit_2 = [ 527, 250, 110, 21]
        length_unit_2 = [ 641, 250, 100, 21]
        count_unit_2 = [744, 250, 100, 21]
        weight_unit_2 = [845, 250, 100, 21]
        
        self.ProductionContext_unit_1 = {
            'unit_number' : '1',
            'width' : self.cut_ocr(img, width_unit_1),
            'texture' : self.cut_ocr(img,texture_unit_1),
            'input' : self.cut_ocr(img, input_unit_1),
            'outer_diameter' : self.cut_ocr(img, outer_diameter_unit_1),
            'thickness': self.cut_ocr(img, thickness_unit_1),
            'length' : self.cut_ocr(img, length_unit_1),
            'count' : self.cut_ocr(img, count_unit_1),
            'weight' : self.cut_ocr(img, weight_unit_1)
        }
        self.ProductionContext_unit_2 = {
            'unit_number' : '2',
            'width' : self.cut_ocr(img, width_unit_2),
            'texture' : self.cut_ocr(img,texture_unit_2),
            'input' : self.cut_ocr(img, input_unit_2),
            'outer_diameter' : self.cut_ocr(img, outer_diameter_unit_2),
            'thickness': self.cut_ocr(img, thickness_unit_2),
            'length' : self.cut_ocr(img, length_unit_2),
            'count' : self.cut_ocr(img, count_unit_2),
            'weight' : self.cut_ocr(img, weight_unit_2)
        }
        return self.ProductionContext_unit_1, self.ProductionContext_unit_2
    
    def ocr_ErrorContext(self, img):
        
        test_unit_1 = [140, 71, 102, 24]
        production_unit_1 = [245, 71, 84, 24]
        outer_diameter_unit_1 = [332, 70, 191, 24]
        thickness_unit_1 = [526, 70, 111, 24]
        length_unit_1 = [641, 73, 97, 19]
        count_unit_1 = [743, 73, 97, 19]
        weight_unit_1 = [844, 73, 98, 19]

        test_unit_2 = [140, 191, 102, 19]
        production_unit_2 = [245, 191, 83, 19]
        outer_diameter_unit_2 = [331, 191, 191, 19]
        thickness_unit_2 = [525, 191, 111, 19]
        length_unit_2 = [640, 191, 98, 19]
        count_unit_2 = [743, 191, 98, 19]
        weight_unit_2 = [844, 193, 98, 19]

        self.ErrorContext_unit_1 = {
            'unit_number' : '1',
            'test' : self.cut_ocr(img, test_unit_1),
            'production' : self.cut_ocr(img, production_unit_1),
            'outer_diameter' : self.cut_ocr(img, outer_diameter_unit_1),
            'thickness' : self.cut_ocr(img, thickness_unit_1),
            'length' : self.cut_ocr(img, length_unit_1),
            'count' : self.cut_ocr(img, count_unit_1),
            'weight' : self.cut_ocr(img, weight_unit_1),
        }
        
        self.ErrorContext_unit_2 = {
            'unit_number' : '2',
            'test' : self.cut_ocr(img, test_unit_2),
            'production' : self.cut_ocr(img, production_unit_2),
            'outer_diameter' : self.cut_ocr(img, outer_diameter_unit_2),
            'thickness' : self.cut_ocr(img, thickness_unit_2),
            'length' : self.cut_ocr(img, length_unit_2),
            'count' : self.cut_ocr(img, count_unit_2),
            'weight' : self.cut_ocr(img, weight_unit_2)
        }

        return self.ErrorContext_unit_1, self.ErrorContext_unit_2
        
    def ocr_SaleContext(self, img):

        _11_texture = [245, 415, 84, 24]  # h 24
        _11_outer_diameter = [332, 415, 191, 24]
        _11_thickness = [526, 415, 111, 24]
        _11_length = [640, 415, 98, 24]
        _11_count = [746, 415, 98, 24]
        _11_weight = [844, 415, 98, 24]
        _11_per_price = [945, 415, 99, 24]
        
        _12_texture = [245, 565, 84, 24]
        _12_outer_diameter = [332, 565, 191, 24]
        _12_thickness = [526, 565, 111, 24]
        _12_length = [640, 565, 98, 24]
        _12_count = [746, 565, 98, 24]
        _12_weight = [844, 565, 98, 24]
        _12_per_price = [945, 565, 99, 24]
        
        _21_texture = [245, 65, 84, 24]  # h 24
        _21_outer_diameter = [332, 65, 191, 24]
        _21_thickness = [526, 66, 111, 24]
        _21_length = [640, 65, 98, 24]
        _21_count = [746, 66, 98, 24]
        _21_weight = [844, 66, 98, 24]
        _21_per_price = [945, 66, 99, 24]

        _22_texture = [245, 265, 84, 24]
        _22_outer_diameter = [332, 265, 191, 24]
        _22_thickness = [526, 265, 111, 24]
        _22_length = [640, 265, 98, 24]
        _22_count = [746, 265, 98, 24]
        _22_weight = [844, 265, 98, 24]
        _22_per_price = [945, 265, 99, 24]


        
        
        self.SaleContext_11 = {
            'department' : '1',
            'unit_number' : '1',
            'texture' : self.cut_ocr(img, _11_texture),
            'outer_diameter' : self.cut_ocr(img, _11_outer_diameter),
            'thickness' : self.cut_ocr(img, _11_thickness),
            'length' : self.cut_ocr(img, _11_length),
            'count' : self.cut_ocr(img, _11_count),
            'weight' : self.cut_ocr(img, _11_weight),
            'per_price' : self.cut_ocr(img, _11_per_price),
        }
        self.SaleContext_12 = {
            'department' : '1',
            'unit_number' : '2',
            'texture' : self.cut_ocr(img, _12_texture),
            'outer_diameter' : self.cut_ocr(img, _12_outer_diameter),
            'thickness' : self.cut_ocr(img, _12_thickness),
            'length' : self.cut_ocr(img, _12_length),
            'count' : self.cut_ocr(img, _12_count),
            'weight' : self.cut_ocr(img, _12_weight),
            'per_price' : self.cut_ocr(img, _12_per_price),
        }
        self.SaleContext_21 = {
            'department' : '2',
            'unit_number' : '1',
            'texture' : self.cut_ocr(img, _21_texture),
            'outer_diameter' : self.cut_ocr(img, _21_outer_diameter),
            'thickness' : self.cut_ocr(img, _21_thickness),
            'length' : self.cut_ocr(img, _21_length),
            'count' : self.cut_ocr(img, _21_count),
            'weight' : self.cut_ocr(img, _21_weight),
            'per_price' : self.cut_ocr(img, _21_per_price),
        }
        self.SaleContext_22 = {
            'department' : '2',
            'unit_number' : '2',
            'texture' : self.cut_ocr(img, _22_texture),
            'outer_diameter' : self.cut_ocr(img, _22_outer_diameter),
            'thickness' : self.cut_ocr(img, _22_thickness),
            'length' : self.cut_ocr(img, _22_length),
            'count' : self.cut_ocr(img, _22_count),
            'weight' : self.cut_ocr(img, _22_weight),
            'per_price' : self.cut_ocr(img, _22_per_price)
        }
        return self.SaleContext_11, self.SaleContext_12, self.SaleContext_21, self.SaleContext_22