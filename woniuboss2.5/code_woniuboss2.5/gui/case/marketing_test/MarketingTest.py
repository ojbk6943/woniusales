import unittest
from parameterized import parameterized
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from gui.common.marketing.Marketing import Marketing
from gui.util.Service import Service
from gui.util.Utility import Utility
import re

# 不同区域、不同状态、入库时间
marketing_query_data = Utility.read_json("../test_data/marketing_data/marketing_query_data")

class MarketingTest(unittest.TestCase):

    # 自定义，初始化driver，窗口最大化，隐式等待
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.url = Utility.read_json("../config/data_base")["BASEURL"]
        self.driver.get(self.url)
    # 查询功能，不同区域、不同状态、入库时间，查询  area,status,starttime,endtime
    # 查询除内容后，判断是否能解密成功"area":"西安","status":"新入库",
    @parameterized.expand(marketing_query_data)
    def test_marketing_query(self,marketing_query_info,expect):
        # 添加cookie信息，跳转到登陆后首页
        Service.add_cookie(self.driver, self.url, "../config/data_cookie")
        # 点击市场营销
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "市场营销").click()

        Marketing.marketing_query(self.driver,marketing_query_info)
        # 判断是否查询出数据
        query_result = Service.get_ele(self.driver, By.CSS_SELECTOR, "table#netCus-table tbody").text
        # 市场营销有上传过数据
        if query_result != "无符合条件的记录":
            # 前端页面显示数据数，根据状态（不同状态数量不同）
            query_count_result = Service.get_ele(self.driver, By.XPATH, "//span[@class='pagination-info']").text
            result = re.match('^显示.*，总.*?(\d+)', query_count_result)

            # 查询数据库，对比数据条数是否正确
            if marketing_query_info['status']=="全部" and marketing_query_info['area']=="全部":
                sql = 'select count(customer_id) from customer where source="%s" and ' \
                      'create_time between "%s" and "%s"'%('网络',marketing_query_info['starttime'],marketing_query_info['endtime'])
                query_connect_count = Utility.get_connect_one(sql,"../config/data_base")
            elif marketing_query_info['status']=="全部" and marketing_query_info['area']!="全部":
                sql = 'select count(customer_id) from customer where source="%s" and region="%s" and create_time between "%s" and "%s"' \
                      %('网络',marketing_query_info['area'],marketing_query_info['starttime'],marketing_query_info['endtime'])
                query_connect_count = Utility.get_connect_one(sql, "../config/data_base")
            elif marketing_query_info['status']!="全部" and marketing_query_info['area']=="全部":
                sql = 'select count(customer_id) from customer where source="%s" and last_status="%s" and create_time between "%s" and "%s"' \
                      % ('网络', marketing_query_info['status'],marketing_query_info['starttime'],marketing_query_info['endtime'])
                query_connect_count = Utility.get_connect_one(sql, "../config/data_base")
            else:
                sql = 'select count(customer_id) from customer where source="%s" and last_status="%s" and region="%s" and create_time between "%s" and "%s"' \
                      % ('网络', marketing_query_info['status'],marketing_query_info['area'],marketing_query_info['starttime'],marketing_query_info['endtime'])
                query_connect_count = Utility.get_connect_one(sql, "../config/data_base")


            if int(result.group(1)) == int(query_connect_count[0]):
                actual = 'query-pass'
            else:
                actual = 'query-fail'
            self.assertEqual(actual,expect)
        else:
            print("查询为空")
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)