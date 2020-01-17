import time
import unittest
from parameterized import parameterized
from gui.common.personnel_management.PersonnelManagement import PersonnelManagement
from gui.util.Service import Service
from gui.util.Utility import Utility

# 查询 测试用例，数据
query_employee_data = Service.get_excell_data(
    "C:/Users/wang/Desktop/woniuboss4.0/gui/test_data/personnel_management_data/testCase.xlsx", "query", 3, 4)

# 新增 测试用例，数据
add_employee_data = Service.get_excell_data(
    "C:/Users/wang/Desktop/woniuboss4.0/gui/test_data/personnel_management_data/testCase.xlsx", "add", 3, 4)

modify_employee_data = Service.get_excell_data(
    "C:/Users/wang/Desktop/woniuboss4.0/gui/test_data/personnel_management_data/testCase.xlsx", "modify", 3, 4)

# 页面数据
page_data = Utility.read_json(
    "C:/Users/wang/Desktop/woniuboss4.0/gui/test_data/personnel_management_data/page_obj_data")


class PersonnelManagementTest(unittest.TestCase):
    # get driver ,get url, add cookie
    def setUp(self):
        self.driver = Service.get_driver()
        Service.jump_target_module(
            self.driver, page_data["setUp"]["url_path"], page_data["setUp"]["cookie_path"],
            page_data["setUp"]["locate_mode"], page_data["setUp"]["locate_msg"])

    '''查询员工'''

    @parameterized.expand(query_employee_data)
    def test_query_employee(self, query_info):
        PersonnelManagement.query_employee(self.driver, query_info)
        query_count = Service.search_recode_result(
            self.driver, page_data["test_query_employee"]["locate_mode"],
            page_data["test_query_employee"]["locate_msg"], page_data["test_query_employee"]["result_locate_mode"],
            page_data["test_query_employee"]["result_locate_msg"])
        # 数据库对比
        sql_result = Service.person_query_sql(query_info, page_data["test_query_employee"]["sql_bath"])

        if int(query_count) == int(sql_result):
            actual = "query_employee-success"
        else:
            actual = "query_employee-fail"
        print(query_count, sql_result)
        self.assertEqual(actual, query_info["expect"])

    '''新增员工'''
    @parameterized.expand(add_employee_data)
    def test_add_employee(self, add_info):

        # 数据库员工数量
        add_sql = page_data["test_add_employee"]["add_sql"]
        sql_result = Utility.get_connect_one(add_sql, page_data["test_add_employee"]["sql_bath"])
        PersonnelManagement.add_employee(self.driver, add_info)

        # 数据库对比
        sql_result_again = Utility.get_connect_one(add_sql, page_data["test_add_employee"]["sql_bath"])

        if sql_result_again > sql_result:
            actual = "add_employee-success"
        else:
            actual = "add_employee-fail"

        self.assertEqual(actual, add_info["expect"])

    '''修改员工信息'''
    @parameterized.expand(modify_employee_data)
    def test_modify_employee(self, modify_info):
        PersonnelManagement.query_employee(self.driver, modify_info)
        time.sleep(3)
        query_count = Service.search_recode_result(
            self.driver, page_data["test_query_employee"]["locate_mode"],
            page_data["test_query_employee"]["locate_msg"], page_data["test_query_employee"]["result_locate_mode"],
            page_data["test_query_employee"]["result_locate_msg"])

        # 调用 修改
        Service.modify_person(self.driver, query_count,
                              page_data["test_query_employee"]["body_id"], page_data["test_query_employee"]["table_id"])
        PersonnelManagement.modify_employee(self.driver)

        # 保存后，确定 弹窗
        try:
            modify_reuslt_ele = Service.get_ele_location_method(
                self.driver, page_data["test_modify_employee"]["modify_reuslt_ele_locate"],
                page_data["test_modify_employee"]["modify_reuslt_ele_msg"])
            if modify_reuslt_ele.is_displayed():
                actual = "modify_employee-success"
                modify_reuslt_ele.click()
            else:
                actual = "modify_employee-fail"
            self.assertEqual(actual, modify_info["expect"])
        except:
            self.driver.get_screenshot_as_file(page_data["test_modify_employee"]["screen_path"])

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)