import time
import unittest
from parameterized import parameterized
from selenium import webdriver
from selenium.webdriver.common.by import By
from gui.common.training_resource.Transferee import Transferee
from gui.util.Service import Service
from gui.util.Utility import Utility
import re


# 数据
transferee_data = Utility.read_json("C:/Users/wang/Desktop/woniuboss_automation/gui/test_data/training_resource/transferee_data")


class TransfereeTest(unittest.TestCase):

    # 自定义，初始化driver，窗口最大化，隐式等待
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.url = Utility.read_json("../config/data_base")["BASEURL"]
        self.driver.get(self.url)

    # 添加cookie   #content > div.row.con-margin.con-body-header > ul > li.active > a
    def training_feree_init(self):
        # 添加cookie信息，跳转到登陆后首页
        Service.add_cookie(self.driver, self.url, "../config/data_cookie")
        # 点击市场营销
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "培训资源").click()


    # 判断当前页面（转让责任人）是否有元素
    @classmethod
    def verification_submit_result(cls,driver):
        # 判断自身、区域有无数据
        query_result_submit = Service.get_ele(driver, By.CSS_SELECTOR, "table#transmit-table tbody").text
        if query_result_submit != "无符合条件的记录":
            # 前端页面显示数据数，根据状态（不同状态数量不同）
            query_count_result = Service.get_ele(driver, By.XPATH, "//span[@class='pagination-info']").text
            result = re.match('^显示.*，总.*?(\d+)', query_count_result).group(1)
        else:
            result = 0
        return result

    # 查询，数据验证，提交三步骤
    @parameterized.expand(transferee_data)
    def test_transferee(self,transferee_submit_info,transferee_info,expect):

        # 获取cookie
        self.training_feree_init()
        # 选择加载资源模块
        Service.get_ele(self.driver, By.CSS_SELECTOR,
                        "#content > div.row.con-margin.con-body-header > div:nth-child(1) > ul > li:nth-child(2) > a").click()
        time.sleep(3)

        # 先判断，提交到的人或区域的学生人数
        Transferee.query_commit(self.driver, transferee_submit_info)
        submit_one_result = self.verification_submit_result(self.driver)

        # 执行提交
        Transferee.query_commit(self.driver,transferee_info)

        # 判断有无数据
        query_result = Service.get_ele(self.driver, By.CSS_SELECTOR, "table#transmit-table tbody").text

        # 当前查询条件下有学生资料，有，则可进行寻找数据
        if query_result != "无符合条件的记录":

            # 全选按钮 (不建议全部咨询师，状态下，选择，这样会造成资源会乱，数据单个资源时，选择)
            if transferee_info["empname"] != "全部":
                Service.get_ele(self.driver,By.CSS_SELECTOR,"th.bs-checkbox > div:nth-child(1) > input:nth-child(1)").click()
            # 默认选中第一条，还有一页多少条数据显示，还有翻页功能
            else:
                # 前端页面显示数据数，根据状态（不同状态数量不同）
                query_count_result = Service.get_ele(self.driver, By.XPATH, "//span[@class='pagination-info']").text
                result = re.match('^显示.*，总.*?(\d+)', query_count_result).group(1)

                # 一页数据大于10，分页
                if int(result) > 10:

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

                    if int(result_again) == int(result):
                        pass
                    else:
                        print("翻页功能异常")
                        self.driver.close()

                    # 当前页展示信息个数
                    query_result_count = Service.get_eles(self.driver, By.XPATH, "//table[@id='transmit-table']/tbody/tr")
                    # 选中第一个
                    Service.get_tier_ele(query_result_count[0],By.XPATH,
                                         "//table[@id='transmit-table']/tbody/tr[1]/td[1]/input").click()
                    # 本页最后一个
                    css_count = "#transmit-table > tbody:nth-child(2) > tr:nth-child(%d) > td:nth-child(1) > input:nth-child(1)" % (len(query_result_count))
                    time.sleep(2)
                    Service.get_tier_ele(query_result_count[len(query_result_count)-1], By.CSS_SELECTOR,
                                         css_count).click()

                # 不分页
                elif int(result) > 1:
                    # 当前页展示信息个数
                    query_result_count = Service.get_eles(self.driver, By.XPATH, "//table[@id='transmit-table']/tbody/tr")
                    # 选中第一个
                    Service.get_tier_ele(query_result_count[0], By.XPATH,
                                         "//table[@id='transmit-table']/tbody/tr[1]/td[1]/input").click()
                    # 本页最后一个
                    # 本页最后一个
                    css_count = "#transmit-table > tbody:nth-child(2) > tr:nth-child(%d) > td:nth-child(1) > input:nth-child(1)" % (
                        len(query_result_count))
                    time.sleep(2)
                    Service.get_tier_ele(query_result_count[len(query_result_count) - 1], By.CSS_SELECTOR,
                                         css_count).click()

                # 一条数据
                else:
                    # 当前页展示信息个数
                    query_result_count = Service.get_ele(self.driver, By.XPATH, "//table[@id='transmit-table']/tbody/tr")
                    # 选中第一个
                    Service.get_tier_ele(query_result_count, By.XPATH,
                                         "//table[@id='transmit-table']/tbody/tr[1]/td[1]/input").click()

            # 选择提交人、或地域（选择之前，先统计，本有个数）
            time.sleep(3)
            Transferee.submit_commit(self.driver,transferee_info)
            # 确定提交
            Service.get_ele(self.driver,By.CSS_SELECTOR,"button.btn-primary:nth-child(2)").click()
            #刷新页面
            self.driver.refresh()

            # 二次验证判断，提交到的人或区域的学生人数
            Transferee.query_commit(self.driver, transferee_submit_info)
            submit_two_result = self.verification_submit_result(self.driver)
            print(int(submit_one_result))
            print(int(submit_two_result))
            if int(submit_one_result) <= int(submit_two_result):
                actual = "query-pass"
            else:
                actual = "query-fail"
            self.assertEqual(actual, expect)

        else:
            print("当前条件下，数据查询为空")

        self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)



