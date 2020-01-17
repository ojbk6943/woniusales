from selenium import webdriver
import unittest

from selenium.webdriver.common.by import By

from gui.util.Service import Service
from gui.util.Utility import Utility


class ReportCenter(unittest.TestCase):

    # 自定义，初始化driver，窗口最大化，隐式等待
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.url = Utility.read_json("../../config/data_base")["BASEURL"]

        # 跳转到报表中心
        Service.add_cookie(self.driver,self.url)
        # 点击报表中心
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "报表中心")
