import unittest

from parameterized import parameterized
from selenium import webdriver
from selenium.webdriver.common.by import By

from gui.common.trainees_management.StagedEvaluation import StagedEvaluation
from gui.util.Service import Service
from gui.util.Utility import Utility

staged_evaluation_test_data = Utility.read_json("../test_data/trainees_management_data/staged_evaluation_data")


class StagedEvaluationTest(unittest.TestCase):

    # 自定义，初始化driver，窗口最大化，隐式等待
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.config_info = Utility.read_json("../config/data_base")
        self.url = self.config_info["BASEURL"]
        self.driver.get(self.url)

    # 添加cookie
    def staged_evaluation_test_init(self):
        # 添加cookie信息，跳转到登陆后首页
        Service.add_cookie(self.driver, self.url, "../config/director_study_data_cookie")
        # 点击市场营销，分配资源
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "学员管理").click()
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "阶段测评").click()

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
    @parameterized.expand(staged_evaluation_test_data)
    def test_staged_evaluation(self, query_info, staged_ifo, expect):
        # cookie
        self.staged_evaluation_test_init()
        # 调用查询操作
        StagedEvaluation.staged_evaluation_query(self.driver, query_info)
        # 调用测评操作
        StagedEvaluation.staged_evaluation_staged(self.driver, staged_ifo)

        print(expect)

if __name__ == '__main__':
    unittest.main(verbosity=2)