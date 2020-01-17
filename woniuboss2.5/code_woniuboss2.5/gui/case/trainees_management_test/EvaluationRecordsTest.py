import re
import unittest
from parameterized import parameterized
from selenium import webdriver
from selenium.webdriver.common.by import By
from gui.common.trainees_management.EvaluationRecords import EvaluationRecords
from gui.util.Service import Service
from gui.util.Utility import Utility

evaluation_records_test_data = Utility.read_json("../test_data/trainees_management_data/evaluation_records_data")


'''学员管理 子模块 测评记录'''
class Evaluation_Records_Test(unittest.TestCase):

    # 自定义，初始化driver，窗口最大化，隐式等待
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.config_info = Utility.read_json("../config/data_base")
        self.url = self.config_info["BASEURL"]
        self.driver.get(self.url)

    # 添加cookie
    def evaluation_records_test_init(self):
        # 添加cookie信息，跳转到登陆后首页
        Service.add_cookie(self.driver, self.url, "../config/director_study_data_cookie")
        # 点击市场营销，分配资源
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "学员管理").click()
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "测评记录").click()

        # 解密
        Service.get_ele(self.driver, By.ID, "btn-decrypt").click()
        decode_input_ele = Service.get_ele(self.driver,
                                           By.CSS_SELECTOR, "#secondPass-modal > div > div > "
                                                            "div.modal-body.text-center > input[type=password]")
        Service.input_value_ele(decode_input_ele, self.config_info["DECODE"])
        # 点击确定
        Service.get_ele(self.driver, By.CSS_SELECTOR,
                        "#secondPass-modal > div > div > div.modal-footer > button").click()

    # 判断当前页面（测评记录）是否有数据
    def verification_evaluation_records_result(self):
        # 判断自身、区域有无数据
        query_result_class = Service.get_ele(self.driver, By.CSS_SELECTOR, "table#pe-result tbody").text
        if query_result_class != "无符合条件的记录":
            # 前端页面显示数据数，根据状态（不同状态数量不同）
            query_count_result = Service.get_ele(
                self.driver, By.CSS_SELECTOR,
                "#stagetest > div.bootstrap-table > div.fixed-table-container > div.fixed-table-pagination > "
                "div.pull-left.pagination-detail > span.pagination-info").text
            result = re.match('^显示.*，总.*?(\d+)', query_count_result).group(1)
        else:
            result = 0
        return result

    # 测试用例
    @parameterized.expand(evaluation_records_test_data)
    def test_evaluation_records(self, records_info, expect):
        # cookie
        self.evaluation_records_test_init()
        # 查询操作
        EvaluationRecords.staged_evaluation_query(self.driver, records_info)
        if self.verification_evaluation_records_result():
            actual = "records-pass"
        else:
            actual = "records-fail"
        self.assertEqual(actual, expect)
        self.driver.quit()
if __name__ == '__main__':
    unittest.main(verbosity=2)
