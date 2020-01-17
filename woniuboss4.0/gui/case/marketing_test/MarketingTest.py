import unittest
from parameterized import parameterized
from selenium.webdriver.common.by import By

from gui.common.marketing.Marketing import Marketing
from gui.util.Service import Service
from gui.util.Utility import Utility



# 查询 测试用例，数据


marketing_query_data = Service.get_excell_data(
    "C:/Users/wang/Desktop/woniuboss4.0/gui/test_data/personnel_management_data/testCase.xlsx",
    "marketing_query", 3, 4)

marketing_add_data = Service.get_excell_data(
    "C:/Users/wang/Desktop/woniuboss4.0/gui/test_data/personnel_management_data/testCase.xlsx",
    "marketing_add", 3, 4)

# 页面数据
marketing_page_data = Utility.read_json(
    "C:/Users/wang/Desktop/woniuboss4.0/gui/test_data/marketing_data/class_manager_data")


# 不同区域、不同状态、入库时间
# class_manager_data = Utility.read_json("../../test_data/marketing_data/class_manager_data")

class MarketingTest(unittest.TestCase):

    # 自定义，初始化driver，窗口最大化，隐式等待
    def setUp(self):
        self.driver = Service.get_driver()
        #   Jump targets module
        Service.jump_target_module(
            self.driver, marketing_page_data["setUp"]["url_path"], marketing_page_data["setUp"]["cookie_path"],
            marketing_page_data["setUp"]["locate_mode"], marketing_page_data["setUp"]["locate_msg"])
        # 简历资源
        Service.get_ele_location_method(self.driver, marketing_page_data["setUp"]["resource_locate"],
                                        marketing_page_data["setUp"]["resource_locate_msg"]).click()
        # 解密
        Service.page_decode(self.driver, marketing_page_data["setUp"]["decode_url"])

    # 查询功能，不同区域、不同状态、入库时间，查询  area,status,starttime,endtime
    @parameterized.expand(marketing_query_data)
    @unittest.skip("忽略")
    def test_marketing_query(self, marketing_query_info):
        # 调用查询操作
        Marketing.marketing_query(self.driver,marketing_query_info)
        # 当前条件查询出的数量
        query_count = Service.search_recode_result(
            self.driver, marketing_page_data["test_marketing_query"]["locate_mode"],
            marketing_page_data["test_marketing_query"]["locate_msg"],
            marketing_page_data["test_marketing_query"]["result_locate_mode"],
            marketing_page_data["test_marketing_query"]["result_locate_msg"]
        )
        # 数据库对比
        sql_result_again = Service.marketing_query_sql(
            marketing_query_info, marketing_page_data["test_marketing_query"]["sql_bath"])

        if sql_result_again == int(query_count):
            actual = "query_customer-success"
        else:
            actual = "query_customer-success"

        self.assertEqual(actual, marketing_query_info["expect"])

    @parameterized.expand(marketing_add_data)
    def test_add_source(self, marketing_query_info):

        # 点击新增
        Service.get_ele_location_method(self.driver,
                                        'css', '#queryDiv > div:nth-child(2) > button:nth-child(9)').click()

        # 调用新增操作
        Marketing.marketing_add(self.driver, marketing_query_info)

        # 判断出现保存成功框
        commit_window_ele = Service.is_Element_present(
            self.driver, By.CSS_SELECTOR, "body > div.bootbox.modal.fade.mydialog.in > "
                                                                 "div > div > div.modal-footer > button")
        if commit_window_ele:
            actual = "add-customer-success"
            commit_window_ele.click()
        else:
            actual = "add-customer-fail"

        # 预期不符，截图
        if actual != marketing_query_info["expect"]:
            file_name = "add_error" + Service.format_date() + '.png'
            self.driver.get_screenshot_as_file(
                "C:\\Users\wang\Desktop\woniuboss4.0\gui\error\\'%s'" % (file_name))
        # 断言
        self.assertEqual(actual, marketing_query_info["expect"])


    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)