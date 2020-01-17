import re
import time
import unittest
from parameterized import parameterized
from selenium import webdriver
from selenium.webdriver.common.by import By
from gui.common.trainees_management.ClassManagement import ClassManagement
from gui.util.Service import Service
from gui.util.Utility import Utility


class_management_test_data = Utility.read_json("../test_data/trainees_management_data/class_management_data")


class ClassManagementTest(unittest.TestCase):

    # 自定义，初始化driver，窗口最大化，隐式等待
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.config_info = Utility.read_json("../config/data_base")
        self.url = self.config_info["BASEURL"]
        self.driver.get(self.url)

    # 添加cookie
    def course_arrangement_init(self):
        # 添加cookie信息，跳转到登陆后首页
        Service.add_cookie(self.driver, self.url, "../config/director_study_data_cookie")
        # 点击市场营销，分配资源
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "学员管理").click()
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "班级管理").click()

        # 解密
        Service.get_ele(self.driver, By.ID, "btn-decrypt").click()
        decode_input_ele = Service.get_ele(self.driver,
                                           By.CSS_SELECTOR, "#secondPass-modal > div > div > "
                                                            "div.modal-body.text-center > input[type=password]")
        Service.input_value_ele(decode_input_ele, self.config_info["DECODE"])
        # 点击确定
        Service.get_ele(self.driver, By.CSS_SELECTOR,
                        "#secondPass-modal > div > div > div.modal-footer > button").click()

    # 校验是否分班成功
    def verification_class_correct(self,data,expect):
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "今日考勤").click()
        class_manage_name_ele = Service.get_ele(self.driver,By.CSS_SELECTOR,
                        "#atten > div.col-lg-12.col-md-12.col-xs-12.con-body-padding.text-left > "
                        "input[type=text]")
        Service.input_value_ele(class_manage_name_ele,data)
        # 点击搜索
        Service.get_ele(self.driver, By.CSS_SELECTOR,
                        "#atten > div.col-lg-12.col-md-12.col-xs-12.con-body-padding.text-left > "
                        "button:nth-child(2)").click()
        if Service.get_ele(self.driver,
                           By.CSS_SELECTOR, "table#attendance_table tbody").text != "无符合条件的记录":
            actual = "class-manage-pass"
        else:
            actual = "class-manage-fail"
        # 断言
        self.assertEqual(actual,expect)

    # 判断当前页面（课程安排）是否有数据
    def verification_class_management_result(self, driver):
        # 判断自身、区域有无数据
        query_result_class = Service.get_ele(driver, By.CSS_SELECTOR, "table#class-table tbody").text
        if query_result_class != "无符合条件的记录":
            # 前端页面显示数据数，根据状态（不同状态数量不同）
            query_count_result = Service.get_ele(
                driver, By.CSS_SELECTOR,
                "#cmDiv > div.bootstrap-table > div.fixed-table-container > div.fixed-table-pagination > "
                "div.pull-left.pagination-detail > span.pagination-info").text
            result = re.match('^显示.*，总.*?(\d+)', query_count_result).group(1)
        else:
            result = 0
        return result

    # 测试用例
    @parameterized.expand(class_management_test_data)
    def test_class_management(self,class_management_query_info,class_management_commit_info,expect):

        # cookie
        self.course_arrangement_init()

        # 调用 查询操作
        ClassManagement.class_management_query(self.driver,class_management_query_info)

        # 判断当前条件下，有无数据  判断有无元素，以及有多少个
        class_query_result = self.verification_class_management_result(self.driver)

        # 学生数量不为 0
        if int(class_query_result) != 0:

            # 判断学生数量 一页数据大于10，分页
            if int(class_query_result) > 10:

                # 翻页功能
                page_count_ele = Service.get_eles(self.driver, By.CSS_SELECTOR,
                                                  "#class-table > div.bootstrap-table > div.fixed-table-container > "
                                                  "div.fixed-table-pagination > div.pull-right.pagination > ul li")
                # 选择最后一页
                Service.get_tier_ele(page_count_ele[len(page_count_ele) - 1 - 1], By.TAG_NAME, "a").click()

                # 校验显示是否正确
                query_count_result_again = Service.get_ele(self.driver, By.XPATH,
                                                           "//span[@class='pagination-info']").text
                result_again = re.match('^显示.*到.*?(\d+)', query_count_result_again).group(1)

                if int(result_again) == int(class_query_result):
                    pass
                else:
                    print("翻页功能异常")
                    self.driver.close()

                # 当前页展示信息个数
                query_result_count = Service.get_eles(self.driver, By.CSS_SELECTOR,
                                                      "#class-table > tbody > tr")
                if len(query_result_count) > 1:
                    # 选中第一个
                    Service.get_tier_ele(query_result_count[0], By.XPATH,
                                         "#class-table > tbody > tr:nth-child(1) > "
                                         "td.bs-checkbox > input[type=checkbox]").click()
                    # 本页最后一个
                    css_count = "#class-table > tbody > tr:nth-child(%d) > " \
                                "td.bs-checkbox > input[type=checkbox]" % (len(query_result_count))
                    time.sleep(2)
                    Service.get_tier_ele(query_result_count[len(query_result_count) - 1], By.CSS_SELECTOR,
                                         css_count).click()
                    # 调用分班 操作
                    ClassManagement.class_management_commit(self.driver, class_management_commit_info)
                    self.driver.refresh()

                    # 去班级管理模块， 验证信息是否正确添加
                    self.verification_class_correct(class_management_query_info["name"],expect)

                else:
                    # 选中第一个
                    Service.get_tier_ele(query_result_count[0], By.XPATH,
                                         "#class-table > tbody > tr:nth-child(1) > "
                                         "td.bs-checkbox > input[type=checkbox]").click()

                    # 调用分班 操作
                    ClassManagement.class_management_commit(self.driver, class_management_commit_info)
                    self.driver.refresh()

                    # 去班级管理模块， 验证信息是否正确添加
                    self.verification_class_correct(class_management_query_info["name"], expect)

            # 不分页
            elif int(class_query_result) > 1:
                # 当前页展示信息个数
                query_result_count = Service.get_eles(self.driver, By.CSS_SELECTOR,
                                                      "#class-table > tbody > tr")
                # 选中第一个
                Service.get_tier_ele(query_result_count[0], By.XPATH,
                                     "#class-table > tbody > tr:nth-child(1) > "
                                     "td.bs-checkbox > input[type=checkbox]").click()
                # 本页最后一个
                css_count = "#class-table > tbody > tr:nth-child(%d) > " \
                            "td.bs-checkbox > input[type=checkbox]" % (len(query_result_count))
                time.sleep(2)
                Service.get_tier_ele(query_result_count[len(query_result_count) - 1], By.CSS_SELECTOR,
                                     css_count).click()
                # 调用分班 操作
                ClassManagement.class_management_commit(self.driver, class_management_commit_info)
                self.driver.refresh()

                # 去班级管理模块， 验证信息是否正确添加
                self.verification_class_correct(class_management_query_info["name"], expect)

            # 一条数据，用全选，选中元素，然后分班
            else:

                Service.get_ele(self.driver,By.CSS_SELECTOR,
                                "#class-table > thead > tr > th.bs-checkbox > "
                                "div.th-inner > input[type=checkbox]").click()
                # 调用分班 操作
                ClassManagement.class_management_commit(self.driver,class_management_commit_info)
                self.driver.refresh()

                # 去班级管理模块， 验证信息是否正确添加
                self.verification_class_correct(class_management_query_info["name"], expect)

        else:
            print("当前条件下，查询数据为空")
            self.driver.quit()

        self.driver.quit()


if __name__ == '__main__':
    unittest.main(verbosity=2)