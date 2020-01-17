import time
from selenium.webdriver.common.by import By
from gui.util.Service import Service
from gui.util.Utility import Utility


class StudentsVacate:

    # 查询
    @classmethod
    def students_vacate_query(cls, driver, query_info):
        # 区域
        select_region_ele = Service.get_ele_location_method(
            driver, "css",
            "#content > div.row.con-margin.con-body-con > div > div > div > "
            "div.col-lg-12.col-md-12.col-xs-12.con-body-padding.text-left > select:nth-child(1)")
        Service.get_select_result(select_region_ele, query_info['region'])

        # 请假状态
        select_status_ele = Service.get_ele_location_method(
            driver, "css",
            "#content > div.row.con-margin.con-body-con > div > div > div > "
            "div.col-lg-12.col-md-12.col-xs-12.con-body-padding.text-left > select:nth-child(2)")
        Service.get_select_result(select_status_ele, query_info['status'])

        # 姓名
        class_name_ele = Service.get_ele_location_method(
            driver, "css", "#content > div.row.con-margin.con-body-con > div > div > div > "
                           "div.col-lg-12.col-md-12.col-xs-12.con-body-padding.text-left > input")
        Service.input_value_ele(class_name_ele, query_info['name'])

        # 点击查询
        Service.get_ele_location_method(
            driver, "css", "#content > div.row.con-margin.con-body-con > div > div > div > "
                           "div.col-lg-12.col-md-12.col-xs-12.con-body-padding.text-left > button").click()

    # 新增
    @classmethod
    def students_vacate_add(cls, driver, add_info):
        # 开始时间
        Service.get_ele_location_method(driver, "css", "#leave-form > div:nth-child(2)"
                                                            " > div:nth-child(1) > input:nth-child(2)").click()
        Service.get_ele_location_method(driver, "css", "div.datetimepicker:nth-child(23) > "
                                                            "div:nth-child(3) > table:nth-child(1) > tbody:nth-child(2) > "
                                                            "tr:nth-child(5) > td:nth-child(6)").click()

        # 结束时间
        Service.get_ele_location_method(driver, "css", "#leave-form > div:nth-child(2) >"
                                                            " div:nth-child(2) > input:nth-child(2)").click()

        Service.get_ele_location_method(driver, "css",
                                        "div.datetimepicker:nth-child(24) > div:nth-child(3) > table:nth-child(1) >"
                                        " tbody:nth-child(2) > tr:nth-child(6) > td:nth-child(1)").click()

        # 请假类型
        vacate_type_ele = Service.get_ele_location_method(driver, "css",
                                        "#leave-form > div:nth-child(3) > div:nth-child(1) > select")
        Service.get_select_result(vacate_type_ele, add_info['type'])

        # 请假天数
        time_ele = Service.get_ele_location_method(
            driver, "css", "#leave-form > div:nth-child(3) > div:nth-child(2) > input")
        Service.input_value_ele(time_ele, add_info['time'])

        # 姓名
        name_ele = Service.get_ele_location_method(
            driver, "css", "#leave-form > div:nth-child(4) > div > input")
        Service.input_value_ele(name_ele, add_info['name'])
        # 关联
        Service.get_ele_location_method(driver, "css", "#leave-form > div:nth-child(4) > div > ul > li > a").click()

        # 是否扣分
        score_ele = Service.get_ele_location_method(driver, "css",
                                                          "#leave-form > div:nth-child(4) > select")
        Service.get_select_result(score_ele, add_info['score'])

        # 请假原因
        reason_ele = Service.get_ele_location_method(
            driver, "css", "#leave-form > div:nth-child(5) > div > textarea")
        Service.input_value_ele(reason_ele, add_info['reason'])

        # 保存
        Service.get_ele_location_method(
            driver, "css", "#leave-modal > div > div > div.modal-footer > button").click()