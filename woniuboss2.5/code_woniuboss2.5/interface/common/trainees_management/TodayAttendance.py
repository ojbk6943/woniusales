from selenium.webdriver.common.by import By
from gui.util.Service import Service



'''学员管理 子模块 今日考勤'''

class TodayAttendance:

    # 姓名 元素
    @classmethod
    def today_input_name(cls, driver, data):
        today_input_name_ele = Service.get_ele(driver, By.CSS_SELECTOR, "#atten > div.col-lg-12.col-md-12.col-xs-12.con-body-padding.text-left > input[type=text]")
        # 值
        Service.input_value_ele(today_input_name_ele, data)

    # 搜索 按钮 元素
    @classmethod
    def button_today_query(cls, driver):
        Service.get_ele(
            driver, By.CSS_SELECTOR, "#atten > div.col-lg-12.col-md-12.col-xs-12.con-body-padding.text-left > "
                                     "button:nth-child(2)").click()

    # 搜索操作
    @classmethod
    def today_attendance_query(cls, driver, query_info):
        TodayAttendance.today_input_name(driver, query_info)
        TodayAttendance.button_today_query(driver)

    # 批量考勤 操作(元素+操作)
    @classmethod
    def today_attendance_check(cls, driver):
        Service.get_ele(
            driver, By.CSS_SELECTOR, "#atten > div.col-lg-12.col-md-12.col-xs-12.con-body-padding.text-left > "
                                     "button.btn.btn-info.btn-padding.pull-right").click()
        # 弹窗，点击确定
        Service.get_ele(driver, By.CSS_SELECTOR, "body > div.bootbox.modal.fade.mydialog.in > "
                                                 "div > div > div.modal-footer > button.btn.btn-primary").click()

        # 弹窗，点击完毕
        Service.get_ele(driver,By.CSS_SELECTOR ,"body > div.bootbox.modal.fade.mydialog.in > "
                                                "div > div > div.modal-footer > button").click()