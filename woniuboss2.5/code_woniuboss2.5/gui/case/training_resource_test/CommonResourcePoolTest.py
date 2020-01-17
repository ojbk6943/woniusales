import re
import time
import unittest

from parameterized import parameterized
from selenium import webdriver
from selenium.webdriver.common.by import By

from gui.common.training_resource.CommonResourcePool import CommonResourcePool
from gui.util.Service import Service
from gui.util.Utility import Utility

common_resource_pool_data = Utility.read_json("../test_data/training_resource/query_common_resource_pool_data")

class CommonResourcePoolTest(unittest.TestCase):

    # 自定义，初始化driver，窗口最大化，隐式等待
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.url = Utility.read_json("../config/data_base")["BASEURL"]
        self.driver.get(self.url)

    # 添加cookie   #content > div.row.con-margin.con-body-header > ul > li.active > a
    def common_resource_pool_init(self):
        # 添加cookie信息，跳转到登陆后首页
        Service.add_cookie(self.driver, self.url, "../config/consulting_competent_data_cookie")
        # 点击市场营销，分配资源
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "培训资源").click()
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "公共资源池").click()

    # 判断当前页面（转让责任人）是否有元素
    @classmethod
    def verification_common_resource_pool_result(cls, driver):
        # 判断自身、区域有无数据
        query_result_submit = Service.get_ele(driver, By.CSS_SELECTOR, "table#public-pool-table  tbody").text
        if query_result_submit != "无符合条件的记录":
            # 前端页面显示数据数，根据状态（不同状态数量不同）
            query_count_result = Service.get_ele(driver, By.XPATH, "//span[@class='pagination-info']").text
            result = re.match('^显示.*，总.*?(\d+)', query_count_result).group(1)
        else:
            result = 0
        return result
    # 测试用例
    @parameterized.expand(common_resource_pool_data)
    def test_common_resource_pool(self,query_info,expect):
        # cookie
        self.common_resource_pool_init()

        # 调用查询操作
        CommonResourcePool.common_resource_pool_query(self.driver,query_info)

        # 先记录，当前查询条件下，学生人数
        common_resource_one_result = self.verification_common_resource_pool_result(self.driver)

        # 学生数量不为 0
        if int(common_resource_one_result) != 0:

            # 判断学生数量 一页数据大于10，分页
            if int(common_resource_one_result) > 10:

                # 翻页功能
                page_count_ele = Service.get_eles(self.driver, By.CSS_SELECTOR,
                                                  "#content > div.con-body > div > div.bootstrap-table > div.fixed-table-container > "
                                                  "div.fixed-table-pagination > div.pull-right.pagination > ul li")
                # 选择最后一页
                Service.get_tier_ele(page_count_ele[len(page_count_ele) - 1 - 1], By.TAG_NAME, "a").click()

                # 校验显示是否正确
                query_count_result_again = Service.get_ele(self.driver, By.XPATH,
                                                           "//span[@class='pagination-info']").text
                result_again = re.match('^显示.*到.*?(\d+)', query_count_result_again).group(1)

                if int(result_again) == int(common_resource_one_result):
                    pass
                else:
                    print("翻页功能异常")
                    self.driver.close()

                # 当前页展示信息个数
                query_result_count = Service.get_eles(self.driver, By.XPATH,
                                                      "//table[@id='public-pool-table']/tbody/tr")
                # 选中第一个
                Service.get_tier_ele(query_result_count[0], By.XPATH,
                                     "//table[@id='public-pool-table']/tbody/tr[1]/td[1]/input").click()
                # 本页最后一个
                css_count = "#public-pool-table > tbody:nth-child(2) > tr:nth-child(%d) > td:nth-child(1) > input:nth-child(1)" % (
                    len(query_result_count))
                time.sleep(2)
                Service.get_tier_ele(query_result_count[len(query_result_count) - 1], By.CSS_SELECTOR,
                                     css_count).click()

            # 不分页
            elif int(common_resource_one_result) > 1:
                # 当前页展示信息个数
                query_result_count = Service.get_eles(self.driver, By.XPATH,
                                                      "//table[@id='public-pool-table']/tbody/tr")
                # 选中第一个
                Service.get_tier_ele(query_result_count[0], By.XPATH,
                                     "//table[@id='public-pool-table']/tbody/tr[1]/td[1]/input").click()
                # 本页最后一个
                css_count = "#public-pool-table > tbody:nth-child(2) > tr:nth-child(%d) > td:nth-child(1) > input:nth-child(1)" % (
                    len(query_result_count))
                time.sleep(2)
                Service.get_tier_ele(query_result_count[len(query_result_count) - 1], By.CSS_SELECTOR,
                                     css_count).click()

            # 一条数据
            else:
                # 当前页展示信息个数
                query_result_count = Service.get_ele(self.driver, By.XPATH,
                                                     "//table[@id='public-pool-table']/tbody/tr")
                # 选中第一个
                Service.get_tier_ele(query_result_count, By.XPATH,
                                     "//table[@id='public-pool-table']/tbody/tr[1]/input").click()

        else:
            print("当前条件下，查询数据为空")
            self.driver.quit()
        time.sleep(3)
        # 执行认领 操作
        CommonResourcePool.common_resource_pool_claim(self.driver)

        Service.get_ele(self.driver, By.CSS_SELECTOR, "button.btn-primary:nth-child(2)").click()
        time.sleep(1)

        self.driver.refresh()

        # 二次验证判断，提交到的人或区域的学生人数

        # 查询
        CommonResourcePool.common_resource_pool_query(self.driver, query_info)
        common_resource_two_result = self.verification_common_resource_pool_result(self.driver)

        # print(int(common_resource_one_result))
        # print(int(common_resource_two_result))
        if int(common_resource_one_result) > int(common_resource_two_result):
            actual = "common-resource-pass"
        else:
            actual = "common-resource-fail"
        self.assertEqual(actual, expect)
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)