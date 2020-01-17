
from selenium.webdriver.common.by import By
from gui.util.Service import Service

'''学员管理子模块  课程安排'''
class CourseArrangement:

    # 讲师 元素
    @classmethod
    def teacher_ele(cls,driver,data):
        teacher_select_ele = Service.get_ele(driver, By.CSS_SELECTOR,
                        "#course > div.col-lg-12.col-md-12.col-sm-12.col-xs-12.con-body-padding.text-left > select")
        Service.get_select_result(teacher_select_ele,data)

    # 修改 元素
    @classmethod
    def modify_function_ele(cls,driver,modify_direction,modify_number):
        Service.get_ele(driver, By.CSS_SELECTOR,
                        "#course_table > tbody > tr:nth-child(1) > td:nth-child(10) > button").click()
        modify_function_direction = Service.get_ele(driver,By.CSS_SELECTOR,
                        "#modifyCourseForm > div > div > div:nth-child(5) > select")
        Service.get_select_result(modify_function_direction, modify_direction)
        modify_function_number = Service.get_ele(driver, By.CSS_SELECTOR,
                                                 "#modifyCourseForm > div > div > div:nth-child(7) > select")
        Service.get_select_result(modify_function_number, modify_number)

    # 新增排课  时间 元素
    @classmethod
    def input_time(cls,driver,data):
        start_time_ele = Service.get_ele(driver,By.CSS_SELECTOR,"#addcourse > div > div:nth-child(1) > input")
        end_time_ele = Service.get_ele(driver,By.CSS_SELECTOR,"#addcourse > div > div:nth-child(2) > input")
        # 值
        Service.input_value_ele(start_time_ele,data["starttime"])
        Service.input_value_ele(end_time_ele, data["endtime"])

    #  多位老师排课
    @classmethod
    def teacher_cource_info(cls,driver,count_data,count):
        # 状态
        teacher_status = Service.get_ele(driver, By.CSS_SELECTOR,
                                         "#addCourse-table > tr:nth-child(%d) > td:nth-child(3) > "
                                         "select"%count)
        Service.get_select_result(teacher_status, count_data["status"])
        # 教室
        teacher_room = Service.get_ele(driver, By.CSS_SELECTOR,
                                       "#addCourse-table > tr:nth-child(%d) > td:nth-child(4) > "
                                       "select"%count)
        Service.get_select_result(teacher_room, count_data["room"])
        # 班号
        teacher_room_number = Service.get_ele(driver, By.CSS_SELECTOR,
                                              "#addCourse-table > tr:nth-child(%d) > td:nth-child(5) > "
                                              "select"%count)
        Service.get_select_result(teacher_room_number, count_data["number"])
        # 方向
        teacher_room_direction = Service.get_ele(driver, By.CSS_SELECTOR,
                                                 "#addCourse-table > tr:nth-child(%d) > td:nth-child(6) > "
                                                 "select"%count)
        Service.get_select_result(teacher_room_direction, count_data["direction"])

        # 课程安排
        teacher_source_plan = Service.get_ele(driver, By.CSS_SELECTOR,
                                              "#addCourse-table > tr:nth-child(%d) > td:nth-child(7) > "
                                              "select"%count)
        Service.get_select_result(teacher_source_plan, count_data["plan"])

    # 教师排课
    @classmethod
    def teacher_cource(cls,driver,data_list):
        # teacher_cource_count = Service.get_eles(driver,By.CSS_SELECTOR,"tbody#addCourse-table > tr")

        # 循环写入老师排课内容
        # addCourse-table > tr:nth-child(9)
        for count in range(len(data_list)):
            CourseArrangement.teacher_cource_info(driver,data_list[count],count+1)
        Service.get_ele(driver,By.CSS_SELECTOR,
                        "#course-add > div > div > div.modal-footer > button:nth-child(2)").click()

    # 新增排课 操作
    @classmethod
    def add_curriculum(cls,driver,time_info,data_list):
        Service.get_ele(driver,By.CSS_SELECTOR,
                        "#course > div.col-lg-12.col-md-12.col-sm-12.col-xs-12.con-body-padding.text-left > "
                        "button").click()
        # 安排课程
        CourseArrangement.input_time(driver,time_info)
        CourseArrangement.teacher_cource(driver,data_list)

    # 修改 操作
    @classmethod
    def modify_course(cls, driver, modify_data):
        CourseArrangement.teacher_ele(driver, modify_data["singleteacher"])
        CourseArrangement.modify_function_ele(driver, modify_data["singledirection"], modify_data["singlenumber"])

        # 保存
        Service.get_ele(driver,By.CSS_SELECTOR,"#modifyCourse > div > div > div.modal-footer > button").click()


