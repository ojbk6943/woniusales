import time
import unittest
from parameterized import parameterized
from gui.common.class_manager.StudentsVacate import StudentsVacate
from gui.util.Service import Service
from gui.util.Utility import Utility


# 查询数据
students_vacate_query_data = Service.get_excell_data(
    "C:/Users/wang/Desktop/woniuboss4.0/gui/test_data/personnel_management_data/testCase.xlsx",
    "students_vacate_query", 3, 4)

students_vacate_add_data = Service.get_excell_data(
    "C:/Users/wang/Desktop/woniuboss4.0/gui/test_data/personnel_management_data/testCase.xlsx",
    "students_vacate_add", 3, 4)

# 页面数据
students_vacate_page_data = Utility.read_json(
    "C:/Users/wang/Desktop/woniuboss4.0/gui/test_data/class_manager_data/students_vacate_data")

# class test:
#     def __init__(self):
#         self.driver=Service.get_driver()
#
#     # class Add_Income():
#     def test(self):
#         Service.jump_target_module(self.driver, "../../config/data_base", "../../config/student_teacher_cookie", "link",
#                                    "班务管理")
#         # Service.login_use_cookie(driver,"../../config/data_base","../../config/data_cookie")
#
#         Service.get_ele_location_method(self.driver, "link", "学员请假").click()
#
#         Service.get_ele_location_method(self.driver,"css","button.btn-padding:nth-child(1)").click()
#
#         Service.get_ele_location_method(self.driver,"css","#leave-form > div:nth-child(2)"
#                                                      " > div:nth-child(1) > input:nth-child(2)").click()
#         Service.get_ele_location_method(self.driver,"css","div.datetimepicker:nth-child(23) > "
#                                                      "div:nth-child(3) > table:nth-child(1) > tbody:nth-child(2) > "
#                                                      "tr:nth-child(5) > td:nth-child(6)").click()
#
#         Service.get_ele_location_method(self.driver,"css","#leave-form > div:nth-child(2)"
#                                                      " > div:nth-child(2) > input:nth-child(2)").click()
#         Service.get_ele_location_method(self.driver,"css","div.datetimepicker:nth-child(24) > "
#                                                      "div:nth-child(3) > table:nth-child(1) > tbody:nth-child(2) > "
#                                                      "tr:nth-child(5) > td:nth-child(6)").click()

class StudentsVacateTest(unittest.TestCase):
    # 初始化
    def setUp(self):
        self.driver = Service.get_driver()
#
        # 跳转 班务管理
        Service.jump_target_module(
            self.driver, students_vacate_page_data["setUp"]["url_path"],
            students_vacate_page_data["setUp"]["cookie_path"],
            students_vacate_page_data["setUp"]["locate_mode"], students_vacate_page_data["setUp"]["locate_msg"]
        )
        # 学员请假
        Service.get_ele_location_method(self.driver, students_vacate_page_data["setUp"]["resource_locate"],
                                        students_vacate_page_data["setUp"]["resource_locate_msg"]).click()
#         # 解密
#         Service.page_decode(self.driver, students_vacate_page_data["setUp"]["decode_url"])
#         Service.get_ele_location_method(self.driver, 'css',
#                                         "#content > div.row.con-margin.con-body-con > div > div > div > "
#                                         "div.col-lg-12.col-md-12.col-xs-12.con-body-padding.text-left > div > button").click()
#
#         # 新增操作
#         # StudentsVacate.students_vacate_add(self.driver, add_info)
#         # 新增按钮
#         Service.get_ele_location_method(self.driver, 'css',
#                                         "#content > div.row.con-margin.con-body-con > div > div > div > "
#                                         "div.col-lg-12.col-md-12.col-xs-12.con-body-padding.text-left > div > button").click()
#         Service.get_ele_location_method(self.driver, "css", "#leave-form > div:nth-child(2)"
#                                                             " > div:nth-child(1) > input:nth-child(2)").click()
#         Service.get_ele_location_method(self.driver, "css", "div.datetimepicker:nth-child(23) > "
#                                                             "div:nth-child(3) > table:nth-child(1) > tbody:nth-child(2) > "
#                                                             "tr:nth-child(5) > td:nth-child(6)").click()
#
    # 查询 用例
    @parameterized.expand(students_vacate_query_data)
    @unittest.skip("省略")
    def test_students_vacate_query(self, query_info):
        # 调用操作
        StudentsVacate.students_vacate_query(self.driver, query_info)

        # 当前条件，页面显示的数量
        query_count = Service.search_recode_result(
            self.driver, students_vacate_page_data["test_students_vacate_query"]["locate_mode"],
            students_vacate_page_data["test_students_vacate_query"]["locate_msg"],
            students_vacate_page_data["test_students_vacate_query"]["result_locate_mode"],
            students_vacate_page_data["test_students_vacate_query"]["result_locate_msg"]
        )
        # 数据库对比
        sql_result_again = Service.students_vacate_query_sql(
            query_info, students_vacate_page_data["test_students_vacate_query"]["sql_bath"])

        if sql_result_again == int(query_count):
            actual = "query-students-vacate-success"
        else:
            actual = "query-students-vacate-fail"

        # 预期不符，截图
        Service.get_screen(self.driver, actual, query_info["expect"],
                           "/query_students_vacate", "C:/Users/wang/Desktop/woniuboss4.0/gui/error")
        self.assertEqual(actual, query_info["expect"])

    # 新增 用例
    @parameterized.expand(students_vacate_add_data)
    def test_students_vacate_add(self, add_info):
        # 新增按钮
        Service.get_ele_location_method(self.driver, 'css',
                                        "#content > div.row.con-margin.con-body-con > div > div > div > "
                                        "div.col-lg-12.col-md-12.col-xs-12.con-body-padding.text-left > div > button").click()

        # 新增操作
        StudentsVacate.students_vacate_add(self.driver, add_info)

        # 数据库数据量查询
        sql_result = Utility.get_connect_one(
            "select count(student_id) from student_leave",
            students_vacate_page_data["test_students_vacate_query"]["sql_bath"]
        )[0]
        # 新增操作
        # StudentsVacate.students_vacate_add(self.driver, add_info)

        # 数据库数据量查询
        sql_result_again = Utility.get_connect_one(
            "select count(student_id) from student_leave",
            students_vacate_page_data["test_students_vacate_query"]["sql_bath"]
        )[0]

        # 断言
        if sql_result < sql_result_again:
            actual = "add-students-vacate-success"
        else:
            actual = "add-students-vacate-fail"

        # 预期不符，截图
        Service.get_screen(self.driver, actual, add_info["expect"],
                           "/query_students_vacate", "C:/Users/wang/Desktop/woniuboss4.0/gui/error")

        self.assertEqual(actual, add_info["expect"])

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)