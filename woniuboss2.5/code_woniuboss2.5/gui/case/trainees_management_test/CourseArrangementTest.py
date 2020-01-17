import unittest

from parameterized import parameterized
from selenium import webdriver
from selenium.webdriver.common.by import By

from gui.common.trainees_management.CourseArrangement import CourseArrangement
from gui.util.Service import Service
from gui.util.Utility import Utility

course_arrangement_test_data = Utility.read_json("../test_data/trainees_management_data/course_arrangement_data")


class CourseArrangementTest(unittest.TestCase):
    # 自定义，初始化driver，窗口最大化，隐式等待
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.config_info = Utility.read_json("../config/data_base")
        self.url = self.config_info["BASEURL"]
        self.driver.get(self.url)

    # 添加cookie
    def course_arrangement_init(self):
        # 添加cookie信息，跳转到登陆后首页
        Service.add_cookie(self.driver, self.url, "../config/director_study_data_cookie")
        # 点击市场营销，分配资源
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "学员管理").click()
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "课程安排").click()

        # 解密
        Service.get_ele(self.driver, By.ID, "btn-decrypt").click()
        decode_input_ele = Service.get_ele(self.driver,
                                           By.CSS_SELECTOR, "#secondPass-modal > div > div > "
                                                            "div.modal-body.text-center > input[type=password]")
        Service.input_value_ele(decode_input_ele, self.config_info["DECODE"])
        # 点击确定
        Service.get_ele(self.driver, By.CSS_SELECTOR,
                        "#secondPass-modal > div > div > div.modal-footer > button").click()

    # 测试用例
    @parameterized.expand(course_arrangement_test_data)
    def test_course_arrangement(self,time_info,course_arrangement_test_info,modify_data,expect):
        # cookie
        self.course_arrangement_init()

        # 调用新增排课 操作
        CourseArrangement.add_curriculum(self.driver,time_info,course_arrangement_test_info)

        # 调用修改排课
        CourseArrangement.modify_course(self.driver,modify_data)

        # 修改后，判断修改是否成功过
        class_number = Service.get_ele(self.driver,By.CSS_SELECTOR,
                                       "#course_table > tbody > tr:nth-child(1) > td:nth-child(4)").text
        if class_number == modify_data["singlenumber"]:
            actual = "modify-pass"
        else:
            actual = "modify-fail"

        # 断言
        self.assertEqual(actual,expect)

        self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)