
from selenium.webdriver.common.by import By
from gui.util.Service import Service


'''学员管理子模块基本信息'''
class TraineesManagement:

    # 班级 元素
    @classmethod
    def class_ele(cls,driver,data):

        class_select_ele = Service.get_ele(driver,By.CSS_SELECTOR,
                                           "#stuInfo > div.col-lg-6.col-md-4.col-xs-12.con-body-padding.text-left > "
                                           "select.sel-text.stu-class")
        Service.get_select_result(class_select_ele, data)

    # 方向 元素
    @classmethod
    def direction_ele(cls, driver, data):

        direction_select_ele = Service.get_ele(driver, By.CSS_SELECTOR,
                                           "#stuInfo > div.col-lg-6.col-md-4.col-xs-12.con-body-padding.text-left > "
                                           "select.sel-text.stu-orientation")
        Service.get_select_result(direction_select_ele, data)

    # 最新状态 元素
    @classmethod
    def latest_status_ele(cls, driver, data):

        latest_status_select_ele = Service.get_ele(driver, By.CSS_SELECTOR,
                                               "#stuInfo > div.col-lg-6.col-md-4.col-xs-12.con-body-padding.text-left > "
                                               "select.sel-text.stuStatus")
        Service.get_select_result(latest_status_select_ele, data)

    # 姓名输入框 元素
    @classmethod
    def name_input_query(cls, driver, data):

        name_input_query_ele = Service.get_ele(driver, By.CSS_SELECTOR,
                                          "#stuInfo > div.col-lg-6.col-md-6.col-xs-12.con-body-padding.text-left > "
                                          "input.text")
        Service.input_value_ele(name_input_query_ele, data)

    # 学号输入框 元素
    @classmethod
    def student_number_input_query(cls, driver, data):

        student_number_input_query_ele = Service.get_ele(driver, By.CSS_SELECTOR,
                                          "#stuInfo > div.col-lg-6.col-md-6.col-xs-12.con-body-padding.text-left > "
                                          "input[type=text]:nth-child(2)")
        Service.input_value_ele(student_number_input_query_ele, data)

    @classmethod
    def basic_information_query_ele(cls,driver):
        # 点击 搜索
        Service.get_ele(driver, By.CSS_SELECTOR,
                        "#stuInfo > div.col-lg-6.col-md-6.col-xs-12.con-body-padding.text-left > button").click()

    # 查询 操作 包括（班级、方向、最新状态、姓名、学号）元素 class、direction、lateststatus、name、student_number
    @classmethod
    def basic_information_query(cls,driver,basic_information_query_info):
        # 元素
        TraineesManagement.class_ele(driver,basic_information_query_info["class"])
        TraineesManagement.direction_ele(driver,basic_information_query_info["direction"])
        TraineesManagement.latest_status_ele(driver,basic_information_query_info["lateststatus"])
        TraineesManagement.name_input_query(driver,basic_information_query_info["name"])
        TraineesManagement.student_number_input_query(driver,basic_information_query_info["student_number"])
        # 点击 搜索
        TraineesManagement.basic_information_query_ele(driver)


