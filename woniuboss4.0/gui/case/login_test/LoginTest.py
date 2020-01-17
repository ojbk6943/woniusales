import time
from parameterized import parameterized
from selenium.webdriver.common.by import By
from gui.common.login.Login import Login
from gui.util.Service import Service
import unittest
from selenium import webdriver
from gui.util.Utility import Utility

# 打开首页
open_page_data = Utility.read_json("../test_data/login_data/open_page_data")
# 登陆数据
login_data = Utility.read_json("../test_data/login_data/login_data")

class LoginTest(unittest.TestCase):

    # 自定义，初始化driver，窗口最大化，隐式等待
    def setUp(self):
        self.driver = Service.get_driver()
        self.url = Utility.read_json("../config/data_base")["BASEURL"]

    '''测试首页'''
    @parameterized.expand(open_page_data)
    def test_open_page(self,expect):
        open_page_url = self.url
        Login.open_page(self.driver,open_page_url)
        if Service.is_Element_present(self.driver,By.CSS_SELECTOR,
                                      "#form-login > div > div > div.modal-header.text-center"):
            actual = "open-page-pass"
        else:
            actual = "open_page-fail"
        self.assertEqual(actual,expect)

    '''验证登录'''
    @parameterized.expand(login_data)
    def test_login(self,login_data,expect):
        # 每次用例执行，强制等待1s
        time.sleep(1)
        login_url = self.url
        Login.login(self.driver,login_url,login_data)
        if Service.is_Element_present(self.driver,By.PARTIAL_LINK_TEXT,"注销"):
            actual = "login-pass"
        else:
            actual = "login-fail"
        self.assertEqual(actual,expect)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)