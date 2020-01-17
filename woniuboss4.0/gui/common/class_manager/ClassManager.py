from selenium.webdriver.common.by import By

from gui.util.Service import Service
from gui.util.Utility import Utility


class ClassManager:

    # 查询
    @classmethod
    def class_manager_query(cls, driver, query_info):
        # 校区
        select_region_ele = Service.get_ele_location_method(
            driver, "css",
            "#cmDiv > div.col-lg-12.col-md-12.col-sm-12.col-xs-12.con-body-padding.text-left > "
            "select:nth-child(1)")
        Service.get_select_result(select_region_ele, query_info['region'])

        # 班级
        select_class_ele = Service.get_ele_location_method(
            driver, "css",
            "#cmDiv > div.col-lg-12.col-md-12.col-sm-12.col-xs-12.con-body-padding.text-left > "
            "select:nth-child(2)")
        Service.get_select_result(select_class_ele, query_info['class_status'])

    # 新增
    @classmethod
    def class_manager_add(cls, driver, add_info):
        # 班号
        class_number_ele = Service.get_ele_location_method(
            driver, "css", "#addClass-form > div > div:nth-child(1) > input")
        Service.input_value_ele(class_number_ele, add_info['class_number'])

        # 方向
        select_direction_ele = Service.get_ele_location_method(
            driver, "css", "#addClass-form > div > div:nth-child(2) > select")
        Service.get_select_result(select_direction_ele, add_info['direction'])

        # 开班时间
        Service.get_ele_location_method(
            driver, "css", "#addClass-form > div > div:nth-child(3) > input").click()
        Service.get_ele_location_method(
            driver, "css", "body > div.datetimepicker.datetimepicker-dropdown-bottom-right.dropdown-menu > "
                           "div.datetimepicker-days > table > tbody > tr:nth-child(2) > td:nth-child(5)"
        ).click()

        # 班主任
        teacher_ele = Service.get_ele_location_method(
            driver, "css", "#addClass-form > div > div:nth-child(4) > select")
        Service.get_select_result(teacher_ele, add_info['teacher'])

        # 保存
        Service.get_ele_location_method(
            driver, "css", "#addClass-modal > div > div > div.modal-footer > button").click()