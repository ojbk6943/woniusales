from selenium.webdriver.common.by import By

from gui.util.Service import Service
from gui.util.Utility import Utility

today_attendance_test_data = Utility.read_json("../test_data/trainees_management_data/today_morning_exam_data")


class TodayMorningExam:
    # 姓名 元素
    @classmethod
    def today_morning_input_name(cls, driver, data):
        morning_input_name_ele = Service.get_ele(
            driver, By.CSS_SELECTOR, "#mornExam > "
                                     "div.col-lg-8.col-md-8.col-xs-12.con-body-padding.text-left > input")
        # 值
        Service.input_value_ele(morning_input_name_ele, data)

    # 搜索 按钮 元素
    @classmethod
    def button_morning_query(cls, driver):
        Service.get_ele(
            driver, By.CSS_SELECTOR, "#mornExam > "
                                     "div.col-lg-8.col-md-8.col-xs-12.con-body-padding.text-left > button").click()

    # 搜索操作
    @classmethod
    def today_attendance_query(cls, driver, query_info):
        TodayMorningExam.today_morning_input_name(driver, query_info)
        TodayMorningExam.button_morning_query(driver)