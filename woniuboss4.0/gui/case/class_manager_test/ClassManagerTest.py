import time
import unittest
from parameterized import parameterized
from selenium.webdriver.common.by import By
from gui.common.class_manager.ClassManager import ClassManager
from gui.util.Utility import Utility


from gui.util.Service import Service




class_manager_query_data = Service.get_excell_data(
    "C:/Users/wang/Desktop/woniuboss4.0/gui/test_data/personnel_management_data/testCase.xlsx",
    "class_manager_query", 3, 4)
class_manager_add_data = Service.get_excell_data(
    "C:/Users/wang/Desktop/woniuboss4.0/gui/test_data/personnel_management_data/testCase.xlsx",
    "class_manager_add", 3, 4)

# 页面数据
class_manager_page_data = Utility.read_json(
    "C:/Users/wang/Desktop/woniuboss4.0/gui/test_data/class_manager_data/class_manager_data")


class ClassManagerTest(unittest.TestCase):
    # 初始化
    def setUp(self):
        self.driver = Service.get_driver()
        Service.jump_target_module(
            self.driver, class_manager_page_data["setUp"]["url_path"],
            class_manager_page_data["setUp"]["cookie_path"],
            class_manager_page_data["setUp"]["locate_mode"], class_manager_page_data["setUp"]["locate_msg"]
        )
        # 班级管理
        Service.get_ele_location_method(self.driver, class_manager_page_data["setUp"]["resource_locate"],
                                        class_manager_page_data["setUp"]["resource_locate_msg"]).click()
        # 解密
        Service.page_decode(self.driver, class_manager_page_data["setUp"]["decode_url"])

    # 测试用例
    @parameterized.expand(class_manager_query_data)
    @unittest.skip(u"省略")
    def test_class_manager_query(self, query_info):
        # 调用操作
        ClassManager.class_manager_query(self.driver, query_info)

        # 当前条件，页面显示的数量
        query_count = Service.search_recode_result(
            self.driver, class_manager_page_data["test_class_manager_query"]["locate_mode"],
            class_manager_page_data["test_class_manager_query"]["locate_msg"],
            class_manager_page_data["test_class_manager_query"]["result_locate_mode"],
            class_manager_page_data["test_class_manager_query"]["result_locate_msg"]
        )
        # 数据库对比
        sql_result_again = Service.class_manager_query_sql(
            query_info, class_manager_page_data["test_class_manager_query"]["sql_bath"])

        if sql_result_again == int(query_count):
            actual = "query-class-success"
        else:
            actual = "query-class-fail"

        # 预期不符，截图
        Service.get_screen(self.driver, actual, query_info["expect"],
                           "/query_class", "C:/Users/wang/Desktop/woniuboss4.0/gui/error")

        self.assertEqual(actual, query_info["expect"])

    # 新增
    @parameterized.expand(class_manager_add_data)
    def test_class_manager_add(self, add_info):
        # 新增按钮
        Service.get_ele_location_method(
            self.driver, "xpath",
            "//*[@id='cmDiv']/div[1]/button"
        ).click()

        # 调用新增班级
        ClassManager.class_manager_add(self.driver, add_info)

        true_window_ele = Service.is_Element_present(
            self.driver, By.CSS_SELECTOR,
            "body > div.bootbox.modal.fade.mydialog.in > div > div > div.modal-footer > button")

        if true_window_ele:
            actual = "add-class-success"
            true_window_ele.click()
        else:
            actual = "add-class-fail"

        # 预期不符，截图
        Service.get_screen(self.driver, actual, add_info["expect"],
                           "/add_class", "C:/Users/wang/Desktop/woniuboss4.0/gui/error")

        self.assertEqual(actual, add_info["expect"])

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)