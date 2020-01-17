import re
import time
import unittest

from parameterized import parameterized
from selenium import webdriver
from selenium.webdriver.common.by import By

from gui.common.training_resource.AllocatingResource import AllocatingResource
from gui.util.Service import Service
from gui.util.Utility import Utility


allocating_resource_test = Utility.read_json("../test_data/training_resource/query_allocating_resource_data")


'''培训资源子模块，分配资源'''

class AllocatingResourceTest(unittest.TestCase):
    # 自定义，初始化driver，窗口最大化，隐式等待
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.url = Utility.read_json("../config/data_base")["BASEURL"]
        self.driver.get(self.url)

    # 添加cookie   #content > div.row.con-margin.con-body-header > ul > li.active > a
    def allocating_resource_test_init(self):
        # 添加cookie信息，跳转到登陆后首页
        Service.add_cookie(self.driver, self.url, "../config/consulting_competent_data_cookie")
        # 点击市场营销，分配资源
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "培训资源").click()
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "分配资源").click()

    # 判断当前页面（转让责任人）是否有元素
    @classmethod
    def verification_allocating_result(cls, driver):
        # 判断自身、区域有无数据
        query_result_submit = Service.get_ele(driver, By.CSS_SELECTOR, "table#allot-table tbody").text
        if query_result_submit != "无符合条件的记录":
            # 前端页面显示数据数，根据状态（不同状态数量不同）
            query_count_result = Service.get_ele(driver, By.XPATH, "//span[@class='pagination-info']").text
            result = re.match('^显示.*，总.*?(\d+)', query_count_result).group(1)
        else:
            result = 0
        return result

    # 测试用例
    @parameterized.expand(allocating_resource_test)
    def test_allocating_resource(self,allocating_resource_info,expect):

        # cookie登录
        self.allocating_resource_test_init()

        # 查询
        AllocatingResource.allocating_resource_query_operation(self.driver, allocating_resource_info)

        # 先判断，当前查询条件下，学生人数
        allocating_one_result = self.verification_allocating_result(self.driver)

        # 学生数量不为 0
        if int(allocating_one_result) != 0:

            # 判断学生数量 一页数据大于10，分页
            if int(allocating_one_result) > 10:

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

                if int(result_again) == int(allocating_one_result):
                    pass
                else:
                    print("翻页功能异常")
                    self.driver.close()

                # 当前页展示信息个数
                query_result_count = Service.get_eles(self.driver, By.XPATH,
                                                      "//table[@id='allot-table']/tbody/tr")
                # 选中第一个
                Service.get_tier_ele(query_result_count[0], By.XPATH,
                                     "//table[@id='allot-table']/tbody/tr[1]/td[1]/input").click()
                # 本页最后一个
                css_count = "#allot-table > tbody:nth-child(2) > tr:nth-child(%d) > td:nth-child(1) > input:nth-child(1)" % (
                    len(query_result_count))
                time.sleep(2)
                Service.get_tier_ele(query_result_count[len(query_result_count) - 1], By.CSS_SELECTOR,
                                     css_count).click()

            # 不分页
            elif int(allocating_one_result) > 1:
                # 当前页展示信息个数
                query_result_count = Service.get_eles(self.driver, By.XPATH,
                                                      "//table[@id='allot-table']/tbody/tr")
                # 选中第一个
                Service.get_tier_ele(query_result_count[0], By.XPATH,
                                     "//table[@id='allot-table']/tbody/tr[1]/td[1]/input").click()
                # 本页最后一个
                css_count = "#allot-table > tbody:nth-child(2) > tr:nth-child(%d) > td:nth-child(1) > input:nth-child(1)" % (
                    len(query_result_count))
                time.sleep(2)
                Service.get_tier_ele(query_result_count[len(query_result_count) - 1], By.CSS_SELECTOR,
                                     css_count).click()

            # 一条数据
            else:
                # 当前页展示信息个数
                query_result_count = Service.get_ele(self.driver, By.XPATH,
                                                     "//table[@id='allot-table']/tbody/tr")
                # 选中第一个
                Service.get_tier_ele(query_result_count, By.XPATH,
                                     "//table[@id='allot-table']/tbody/tr[1]/td[1]/input").click()

        else:
            print("当前条件下，查询数据为空")
            self.driver.quit()
        # 执行提交
        AllocatingResource.allocating_resource_submit_operation(self.driver,allocating_resource_info)

        Service.get_ele(self.driver,By.CSS_SELECTOR
                        ,"html body.modal-open div.bootbox.modal.fade.mydialog.in "
                         "div.modal-dialog.modal-sm div.modal-content div.modal-footer button.btn.btn-primary").click()
        time.sleep(1)
        self.driver.refresh()

        # 二次验证判断，提交到的人或区域的学生人数

        # 查询
        AllocatingResource.allocating_resource_query_operation(self.driver, allocating_resource_info)
        allocating_two_result = self.verification_allocating_result(self.driver)

        # print(int(allocating_one_result))
        # print(int(allocating_two_result))
        if int(allocating_one_result) > int(allocating_two_result):
            actual = "allocation-pass"
        else:
            actual = "allocation-fail"
        self.assertEqual(actual, expect)
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)