import time

from selenium.webdriver.common.by import By

from gui.util.Service import Service


class StudentsVacate:

    # 请假状态 下拉框 元素
    @classmethod
    def students_status(cls,driver,data):
        students_select_ele = Service.get_ele(
            driver, By.CSS_SELECTOR,"#leave > div.col-lg-6.col-md-6.col-xs-12.con-body-padding.text-left > select")
        Service.get_select_result(students_select_ele, data)

    # 姓名 元素
    @classmethod
    def students_input_name(cls, driver, data):
        students_input_name_ele = Service.get_ele(
            driver, By.CSS_SELECTOR, "#leave > div.col-lg-6.col-md-6.col-xs-12.con-body-padding.text-left > input")
        # 值
        Service.input_value_ele(students_input_name_ele, data)

    # 查询按钮 元素
    @classmethod
    def button_today_query(cls, driver):
        Service.get_ele(
            driver, By.CSS_SELECTOR, "#leave > div.col-lg-6.col-md-6.col-xs-12.con-body-padding.text-left > button"
        ).click()

    # 新增 操作
    @classmethod
    def students_add_vacate(cls,driver,add_vacate_info):
        # 新增请假 按钮
        Service.get_ele(driver, By.CSS_SELECTOR, "#leave > button").click()
        # 时间 (开始、结束)
        add_vacate_start_time_ele = Service.get_ele(driver, By.CSS_SELECTOR, "#leave-form > div:nth-child(2) > div:nth-child(1) > input")
        Service.get_input(add_vacate_start_time_ele, add_vacate_info["starttime"])
        time.sleep(1)
        add_vacate_end_time_ele = Service.get_ele(driver, By.CSS_SELECTOR,
                                                    "#leave-form > div:nth-child(2) > div:nth-child(2) > input")
        Service.get_input(add_vacate_end_time_ele, add_vacate_info["endtime"])

        # 请假类型
        add_vacate_type_ele = Service.get_ele(
            driver, By.CSS_SELECTOR, "#leave-form > div:nth-child(3) > div:nth-child(1) > select")
        Service.get_select_result(add_vacate_type_ele, add_vacate_info["type"])

        # 请假天数
        add_vacate_days_ele = Service.get_ele(driver, By.CSS_SELECTOR,
                                                  "#leave-form > div:nth-child(3) > div:nth-child(2) > input")
        Service.input_value_ele(add_vacate_days_ele, add_vacate_info["days"])

        # 请假姓名
        add_vacate_name_ele = Service.get_ele(driver, By.CSS_SELECTOR,
                                              "#leave-form > div:nth-child(4) > div > input")
        Service.input_value_ele(add_vacate_name_ele, add_vacate_info["name"])

        # 人名输入正确，会有提示关联的信息
        Service.get_ele(driver, By.CSS_SELECTOR,
                        "#leave-form > div:nth-child(4) > div > ul > li > a").click()

        # 请假原因
        add_vacate_cause_ele = Service.get_ele(driver, By.CSS_SELECTOR,
                                              "#leave-form > div:nth-child(5) > div > textarea")
        Service.input_value_ele(add_vacate_cause_ele, add_vacate_info["cause"])

        # 请假意见
        add_vacate_opinion_ele = Service.get_ele(driver, By.CSS_SELECTOR,
                                               "#leave-form > div:nth-child(6) > div > textarea")
        Service.input_value_ele(add_vacate_opinion_ele, add_vacate_info["opinion"])

        # 保存 按钮
        Service.get_ele(driver, By.CSS_SELECTOR,
                        "#leave-modal > div > div > div.modal-footer > button").click()

    # 查询 操作
    @classmethod
    def students_vacate_query(cls,driver,query_info):
        StudentsVacate.students_status(driver,query_info["status"])
        StudentsVacate.students_input_name(driver, query_info["name"])
        StudentsVacate.button_today_query(driver)

    # 销假操作
    @classmethod
    def students_vacate_delete(cls, driver):
        # 销假
        Service.get_ele(
            driver, By.CSS_SELECTOR, "#leave-table > tbody > tr > td:nth-child(13) > button:nth-child(3)"
        ).click()
        # 确定
        Service.get_ele(
            driver, By.CSS_SELECTOR,
            "body > div.bootbox.modal.fade.mydialog.in > div > div > div.modal-footer > button.btn.btn-primary"
        ).click()
        # 再次确定
        Service.get_ele(
            driver, By.CSS_SELECTOR,
            "body > div.bootbox.modal.fade.mydialog.in > div > div > div.modal-footer > button"
        ).click()

    # 假条、修改操作
    @classmethod
    def students_vacate_update(cls, driver):
        # 假条
        Service.get_ele(
            driver, By.CSS_SELECTOR, "#leave-table > tbody > tr > td:nth-child(13) > button:nth-child(1)"
        ).click()
        # 上传假条图片, "selectStuLeave", "../../test_data/trainees_management_data/student_vacat.jpg"
        Service.get_ele(driver, By.CSS_SELECTOR ,"#selectStuLeave").send_keys("C:\\Users\wang\Desktop\woniuboss_automation\gui_interface\\test_data\\trainees_management_data\student_vacat.jpg")
        # Service.input_value(driver)
        # Service.input_value_ele(img_ele, "../../test_data/trainees_management_data/student_vacat.jpg")

        Service.get_ele(
            driver, By.CSS_SELECTOR, "#leavePermit-modal > div > div > div.modal-footer > button"
        ).click()
