import re
import time
import unittest
from parameterized import parameterized
from selenium import webdriver
from selenium.webdriver.common.by import By
from gui.common.trainees_management.TraineesManagement import TraineesManagement
from gui.util.Service import Service
from gui.util.Utility import Utility


# 数据
trainees_management_data = Utility.read_json("../test_data/trainees_management_data/trainees_management_data")


class TraineesManagementTest(unittest.TestCase):

    # 自定义，初始化driver，窗口最大化，隐式等待
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.config_info = Utility.read_json("../config/data_base")
        self.url = self.config_info["BASEURL"]
        self.driver.get(self.url)

    # 添加cookie   #content > div.row.con-margin.con-body-header > ul > li.active > a
    def common_resource_pool_init(self):
        # 添加cookie信息，跳转到登陆后首页
        Service.add_cookie(self.driver, self.url, "../config/director_study_data_cookie")
        # 点击市场营销，分配资源
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "学员管理").click()
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "基本信息").click()

        # 解密
        Service.get_ele(self.driver,By.ID,"btn-decrypt").click()
        decode_input_ele = Service.get_ele(self.driver,By.CSS_SELECTOR,"#secondPass-modal > div > "
                                                    "div > div.modal-body.text-center > input[type=password]")
        Service.input_value_ele(decode_input_ele, self.config_info["DECODE"])
        # 点击确定
        Service.get_ele(self.driver,By.CSS_SELECTOR,
                        "#secondPass-modal > div > div > div.modal-footer > button").click()

    # 判断当前页面（基本信息）是否有元素
    @classmethod
    def verification_trainees_management_result(cls, driver):
        # 判断自身、区域有无数据
        query_result_basic = Service.get_ele(driver, By.CSS_SELECTOR, "table#stuInfo_table tbody").text
        if query_result_basic != "无符合条件的记录":
            # 前端页面显示数据数，根据状态（不同状态数量不同）
            query_count_result = Service.get_ele(driver, By.XPATH, "//span[@class='pagination-info']").text
            result = re.match('^显示.*，总.*?(\d+)', query_count_result).group(1)
        else:
            result = 0
        return result

    # 修改功能是否正确
    def verification_modify_result(self,modify_ele,modif_path,expect):
        Service.get_tier_ele(modify_ele, By.XPATH, modif_path).click()
        # 姓名框
        modify_name_ele = Service.get_ele(self.driver,By.CSS_SELECTOR,
                        "#modifyForm > div > div:nth-child(2) > div.col-md-8.col-sm-6.col-xs-6 > "
                        "div.col-md-6.col-sm-8.col-xs-8.form-group > input")
        # 在姓名后输入日期
        current_time = Service.format_date()
        current_content = Service.input_value_date_ele(modify_name_ele,current_time)
        # 点击 保存
        Service.get_ele(self.driver,By.CSS_SELECTOR,"#form-modify > div > div > div.modal-footer > button").click()
        # 修改完成，用修改后的姓名，查询一次
        TraineesManagement.name_input_query(self.driver,current_content)
        TraineesManagement.basic_information_query_ele(self.driver)

        if Service.get_ele(self.driver,
                           By.CSS_SELECTOR,"#stuInfo_table > tbody > tr > td:nth-child(1)").text == current_content:
            actual = "basic-pass"
        else:
            actual = "basic-fail"

        self.assertEqual(actual, expect)

    # 验证查看功能正确性
    def verification_check_result(self,check_ele,check_path):

        Service.get_tier_ele(check_ele, By.CSS_SELECTOR,check_path).click()
        # 判断 查看功能
        if Service.is_Element_present(self.driver, By.CSS_SELECTOR, "#seeStuInfo-modal > div > div"):
            # 关闭页面
            Service.get_ele(self.driver,By.CSS_SELECTOR,
                            "#seeStuInfo-modal > div > div > div.modal-header > button > span:nth-child(1)").click()
        else:
            print("查看功能出错")
            self.driver.quit()


    # 测试用例
    @parameterized.expand(trainees_management_data)
    def test_trainees_management(self,trainees_management_info,expect):

        # cookie
        self.common_resource_pool_init()

        # 调用查询操作
        TraineesManagement.basic_information_query(self.driver,trainees_management_info)

        # 判断当前条件下，有无数据
        basic_query_result = self.verification_trainees_management_result(self.driver)

        # 学生数量不为 0
        if int(basic_query_result) != 0:

            # 判断学生数量 一页数据大于10，分页
            if int(basic_query_result) > 10:

                # 翻页功能
                page_count_ele = Service.get_eles(self.driver, By.CSS_SELECTOR,
                                                  "#stuInfo > div.bootstrap-table > div.fixed-table-container > "
                                                  "div.fixed-table-pagination > div.pull-right.pagination > ul li")
                # 选择最后一页
                Service.get_tier_ele(page_count_ele[len(page_count_ele) - 1 - 1], By.TAG_NAME, "a").click()

                # 校验显示是否正确
                query_count_result_again = Service.get_ele(self.driver, By.XPATH,
                                                           "//span[@class='pagination-info']").text
                result_again = re.match('^显示.*到.*?(\d+)', query_count_result_again).group(1)

                if int(result_again) == int(basic_query_result):
                    pass
                else:
                    print("翻页功能异常")
                    self.driver.close()

                # 当前页展示信息个数
                query_result_count = Service.get_eles(self.driver, By.CSS_SELECTOR,
                                                     "#stuInfo_table > tbody > tr")
                if len(query_result_count) > 1:
                    # 选中第一个 查看功能
                    self.verification_check_result(query_result_count[0],
                                                   "//table[@id='stuInfo_table']/tbody/tr[1]/td[12]/input/button[1]")
                    # 本页最后一个
                    css_count = "#stuInfo_table > tbody > tr:nth-child(%d) > td:nth-child(12) > button:nth-child(1)" % (
                        len(query_result_count))
                    time.sleep(2)
                    self.verification_check_result(query_result_count[len(query_result_count) - 1],css_count)

                    # 调用修改功能  第一个
                    self.verification_modify_result(query_result_count[0],
                                                    "//table[@id='stuInfo_table']/tbody/tr/td[12]/button[2]", expect)
                else:
                    query_result_count_one = Service.get_ele(self.driver, By.CSS_SELECTOR,
                                                     "#stuInfo_table > tbody > tr")
                    # 选中唯一个 查看功能#stuInfo_table > tbody > tr > td:nth-child(12) > button:nth-child(1)
                    self.verification_check_result(query_result_count_one,
                                                   "#stuInfo_table > tbody > tr > td:nth-child(12) > "
                                                   "button:nth-child(1)")

                    # 调用修改功能#stuInfo_table > tbody > tr > td:nth-child(12) > button:nth-child(1)
                    self.verification_modify_result(query_result_count_one,
                                                    "//table[@id='stuInfo_table']/tbody/tr/td[12]/button[2]", expect)

            # 不分页
            elif int(basic_query_result) > 1:
                # 当前页展示信息个数
                query_result_count = Service.get_eles(self.driver, By.CSS_SELECTOR,
                                                     "#stuInfo_table > tbody > tr")
                # 选中第一个 查看功能
                self.verification_check_result(query_result_count[0],
                                               "//table[@id='stuInfo_table']/tbody/tr[1]/td[12]/input/button[1]")
                # 本页最后一个
                css_count = "#stuInfo_table > tbody > tr:nth-child(%d) > td:nth-child(12) > button:nth-child(1)" % (
                    len(query_result_count))
                time.sleep(2)
                self.verification_check_result(query_result_count[len(query_result_count) - 1], css_count)

                # 调用修改功能 最后一个
                self.verification_modify_result(query_result_count[len(query_result_count) - 1],
                                                "//table[@id='stuInfo_table']/tbody/tr/td[12]/button[2]", expect)

            # 一条数据
            else:
                # 当前页展示信息个数
                query_result_count = Service.get_ele(self.driver, By.CSS_SELECTOR,
                                                     "#stuInfo_table > tbody > tr")
                # 选中一个 查看功能
                self.verification_check_result(query_result_count,
                                               "#stuInfo_table > tbody > tr > td:nth-child(12) > button:nth-child(1)")
                # 调用修改功能
                self.verification_modify_result(query_result_count,
                                                "//table[@id='stuInfo_table']/tbody/tr/td[12]/button[2]",expect)

        else:
            print("当前条件下，查询数据为空")
            self.driver.quit()

        # 退出
        self.driver.quit()

if __name__ == '__main__':

    unittest.main(verbosity=2)