import re
import unittest

from parameterized import parameterized
from selenium import webdriver
from selenium.webdriver.common.by import By

from gui.common.trainees_management.StudentsVacate import StudentsVacate
from gui.util.Service import Service
from gui.util.Utility import Utility

students_vacate_test_data = Utility.read_json("../test_data/trainees_management_data/students_vacate_data")



class StudentsVacateTest(unittest.TestCase):
    # 自定义，初始化driver，窗口最大化，隐式等待
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.config_info = Utility.read_json("../config/data_base")
        self.url = self.config_info["BASEURL"]
        self.driver.get(self.url)

    # 添加cookie
    def students_vacate_init(self):
        # 添加cookie信息，跳转到登陆后首页
        Service.add_cookie(self.driver, self.url, "../config/director_study_data_cookie")
        # 点击市场营销，分配资源
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "学员管理").click()
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "学员请假").click()

        # 解密
        Service.get_ele(self.driver, By.ID, "btn-decrypt").click()
        decode_input_ele = Service.get_ele(self.driver,
                                           By.CSS_SELECTOR, "#secondPass-modal > div > div > "
                                                            "div.modal-body.text-center > input[type=password]")
        Service.input_value_ele(decode_input_ele, self.config_info["DECODE"])
        # 点击确定
        Service.get_ele(self.driver, By.CSS_SELECTOR,
                        "#secondPass-modal > div > div > div.modal-footer > button").click()

    # 判断当前页面（今日晨考）是否有数据
    def verification_students_vacate_result(self):
        # 判断自身、区域有无数据
        query_result_students_vacate= Service.get_ele(self.driver, By.CSS_SELECTOR, "#leave-table > tbody").text
        if query_result_students_vacate != "无符合条件的记录":
            # 前端页面显示数据数，根据状态（不同状态数量不同）
            query_count_result = Service.get_ele(
                self.driver, By.CSS_SELECTOR,
                "#leave > div.bootstrap-table > div.fixed-table-container > "
                "div.fixed-table-pagination > div.pull-left.pagination-detail > span.pagination-info").text
            result = re.match('^显示.*，总.*?(\d+)', query_count_result).group(1)
        else:
            result = 0
        return result
    # 测试用例
    @parameterized.expand(students_vacate_test_data)
    def test_students_vacate(self, vacate_ing_count, vacate_end_count,
                             add_vacate_info, check_vacate_ing_count, check_vacate_end_count, expect):

        # cookie
        self.students_vacate_init()

        # 调用查询，记录下：请假中 的人数，销假人数
        StudentsVacate.students_vacate_query(self.driver,vacate_ing_count)
        vacate_ing_count_query = self.verification_students_vacate_result()
        # 销假
        StudentsVacate.students_vacate_query(self.driver, vacate_end_count)
        vacate_end_count_query = self.verification_students_vacate_result()

        # 调用 新增 操作
        StudentsVacate.students_add_vacate(self.driver, add_vacate_info)

        # 新增后，再验证
        # 调用查询，记录下：请假中 的人数，销假人数
        StudentsVacate.students_vacate_query(self.driver, check_vacate_ing_count)
        check_vacate_ing_count_query = self.verification_students_vacate_result()

        # 调用假条操作, 有问题
        StudentsVacate.students_vacate_update(self.driver)

        # 调用销假操作，再次记录
        StudentsVacate.students_vacate_delete(self.driver)
        StudentsVacate.students_vacate_query(self.driver, check_vacate_end_count)
        check_vacate_end_count_query = self.verification_students_vacate_result()

        if int(check_vacate_ing_count_query) > int(vacate_ing_count_query)\
                and int(check_vacate_end_count_query) > int(vacate_end_count_query):
            actual = "students-vacate-pass"
        else:
            actual = "students-vacate-fail"
        self.assertEqual(actual,expect)
        # print(check_vacate_ing_count_query,check_vacate_end_count_query)
        # print(vacate_ing_count_query,vacate_end_count_query)
        self.driver.quit()
if __name__ == '__main__':
    unittest.main(verbosity=2)