import re
import unittest

from parameterized import parameterized
from selenium import webdriver
from selenium.webdriver.common.by import By

from gui.common.trainees_management.TodayMorningExam import TodayMorningExam
from gui.util.Service import Service
from gui.util.Utility import Utility

today_morning_test_data = Utility.read_json("../test_data/trainees_management_data/today_morning_exam_data")


class TodayMorningExamTest(unittest.TestCase):
    # 自定义，初始化driver，窗口最大化，隐式等待
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.config_info = Utility.read_json("../config/data_base")
        self.url = self.config_info["BASEURL"]
        self.driver.get(self.url)

    # 添加cookie
    def today_morning_exam_init(self):
        # 添加cookie信息，跳转到登陆后首页
        Service.add_cookie(self.driver, self.url, "../config/director_study_data_cookie")
        # 点击市场营销，分配资源
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "学员管理").click()
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "今日晨考").click()

        # 解密
        Service.get_ele(self.driver, By.ID, "btn-decrypt").click()
        decode_input_ele = Service.get_ele(self.driver,
                                           By.CSS_SELECTOR, "#secondPass-modal > div > div > "
                                                            "div.modal-body.text-center > input[type=password]")
        Service.input_value_ele(decode_input_ele, self.config_info["DECODE"])
        # 点击确定
        Service.get_ele(self.driver, By.CSS_SELECTOR,
                        "#secondPass-modal > div > div > div.modal-footer > button").click()

    # 判断当前页面（今日晨考）是否有数据
    def verification_morning_exam_result(self, driver):
        # 判断自身、区域有无数据
        query_result_morning = Service.get_ele(driver, By.CSS_SELECTOR, "#mornExam-table > tbody").text
        if query_result_morning != "无符合条件的记录":
            # 前端页面显示数据数，根据状态（不同状态数量不同）
            query_count_result = Service.get_ele(
                driver, By.CSS_SELECTOR,
                "#mornExam > div.bootstrap-table > div.fixed-table-container > "
                "div.fixed-table-pagination > div.pull-left.pagination-detail > span.pagination-info").text
            result = re.match('^显示.*，总.*?(\d+)', query_count_result).group(1)
        else:
            result = 0
        return result

    # 有无评过晨考
    def grade_today_morning_exam(self, query_select, exam_info):
        # 判断是否晨考
        if query_select.text == '-':
            # 弹窗
            today_morning_way = Service.get_ele(self.driver, By.CSS_SELECTOR,
                                                "#mornExam-form > div > div:nth-child(1) > select")
            Service.get_select_result(today_morning_way, exam_info["way"])
            today_morning_score = Service.get_ele(self.driver,
                                                  By.CSS_SELECTOR, "#mornExam-form > div > div:nth-child(2) > input")
            Service.input_value_ele(today_morning_score, exam_info["score"])
            today_morning_describe = Service.get_ele(self.driver, By.CSS_SELECTOR,
                                                     "#mornExam-form > div > div.col-md-12.col-sm-12.col-xs-12.form-group > "
                                                     "textarea")
            Service.input_value_ele(today_morning_describe, exam_info["describe"])

            # 保存
            Service.get_ele(self.driver,
                            By.CSS_SELECTOR, "#mornExam-modal > div > div > div.modal-footer > button"
                            ).click()

            # 用于判断是否是这里添加的评分
            return True
            # 判断当前元素，分数，一致，则通过

        # 评过分的略过
        else:
            return False
    # 晨考，先判断有无分数，有分数，不可晨考，略过
    def verification_today_morning_exam(self, exam_data, expect):

        # 判断当前条件下，有无数据  判断有无元素，以及有多少个
        today_morning_query_result = self.verification_morning_exam_result(self.driver)

        # 学生数量不为 0
        if int(today_morning_query_result) != 0:

            # 判断学生数量 一页数据大于10，分页
            if int(today_morning_query_result) > 10:

                # 翻页功能
                page_count_ele = Service.get_eles(self.driver, By.CSS_SELECTOR,
                                                  "#mornExam > div.bootstrap-table > div.fixed-table-container > "
                                                  "div.fixed-table-pagination > div.pull-right.pagination > ul li")
                # 选择最后一页
                Service.get_tier_ele(page_count_ele[len(page_count_ele) - 1 - 1], By.TAG_NAME, "a").click()

                # 校验显示是否正确
                query_count_result_again = Service.get_ele(self.driver, By.XPATH,
                                                           "//span[@class='pagination-info']").text
                result_again = re.match('^显示.*到.*?(\d+)', query_count_result_again).group(1)

                if int(result_again) == int(today_morning_query_result):
                    pass
                else:
                    print("翻页功能异常")
                    self.driver.close()

                # 当前页展示信息个数
                query_result_count = Service.get_eles(self.driver, By.CSS_SELECTOR,
                                                      "#mornExam-table > tbody > tr")
                if len(query_result_count) > 1:

                    # 挨个晨考
                    for count_exam in range(len(query_result_count)):
                        query_select = Service.get_tier_ele(
                            query_result_count[count_exam], By.CSS_SELECTOR,
                            "#mornExam-table > tbody > tr:nth-child(%d) > td:nth-child(6)"%(count_exam+1))
                        # 晨考 按钮
                        Service.get_ele(self.driver, By.CSS_SELECTOR,
                                        "#mornExam-table > tbody > tr:nth-child(%d) > td:nth-child(7) > button"%(count_exam+1)
                                        ).click()
                        condtion = self.grade_today_morning_exam(query_select, exam_data)

                        if condtion:
                            if exam_data["score"] == Service.get_ele(
                                self.driver, By.CSS_SELECTOR,
                                "#mornExam-table > tbody > tr:nth-child(%d) > td:nth-child(6)"%(count_exam+1)).text:
                                actual = "today-attendance-pass"
                            else:
                                actual = "today-attendance-pass"
                        else:
                            actual = "exam-null"

                    if actual == "exam-null":
                        self.assertEqual(actual, "exam-null")
                    else:
                        self.assertEqual(actual, expect)
                else:

                    query_select = Service.get_ele(self.driver, By.CSS_SELECTOR,
                        "#mornExam-table > tbody > tr:nth-child(1) > td:nth-child(6)")
                    # 晨考 按钮
                    Service.get_ele(self.driver, By.CSS_SELECTOR,
                                    "#mornExam-table > tbody > tr:nth-child(1) > td:nth-child(7) > button"
                                    ).click()
                    # 调用判断晨考是否评分
                    condtion = self.grade_today_morning_exam(query_select, exam_data)

                    if condtion:
                        if exam_data["score"] == Service.get_ele(
                            self.driver, By.CSS_SELECTOR,
                            "#mornExam-table > tbody > tr:nth-child(1) > td:nth-child(6)").text:
                            actual = "today-attendance-pass"
                        else:
                            actual = "today-attendance-pass"
                    else:
                        actual = "exam-null"

                    if actual == "exam-null":
                        self.assertEqual(actual, "exam-null")
                    else:
                        self.assertEqual(actual, expect)

            # 不分页
            elif int(today_morning_query_result) > 1:
                # 当前页展示信息个数
                query_result_count = Service.get_eles(self.driver, By.CSS_SELECTOR,
                                                      "#mornExam-table > tbody > tr")
                # 挨个晨考
                for count_exam in range(len(query_result_count)):
                    query_select = Service.get_ele(self.driver, By.CSS_SELECTOR,
                        "#mornExam-table > tbody > tr:nth-child(%d) > td:nth-child(6)" % (count_exam + 1))
                    # 晨考 按钮
                    Service.get_ele(self.driver, By.CSS_SELECTOR,
                                    "#mornExam-table > tbody > tr:nth-child(%d) > td:nth-child(7) > button"% (count_exam + 1)
                                    ).click()
                    condtion = self.grade_today_morning_exam(query_select, exam_data)

                    if condtion:
                        if exam_data["score"] == Service.get_ele(
                            self.driver, By.CSS_SELECTOR,
                            "#mornExam-table > tbody > tr:nth-child(%d) > td:nth-child(6)"%(count_exam+1)).text:
                            actual = "today-attendance-pass"
                        else:
                            actual = "today-attendance-pass"
                    else:
                        actual = "exam-null"
                if actual == "exam-null":
                    self.assertEqual(actual,"exam-null")
                else:
                    self.assertEqual(actual,expect)

            # 一条数据，用全选，选中元素，然后分班
            else:
                query_select = Service.get_ele(self.driver, By.CSS_SELECTOR,
                                               "#mornExam-table > tbody > tr:nth-child(1) > td:nth-child(6)")
                # 晨考 按钮
                Service.get_ele(self.driver, By.CSS_SELECTOR,
                                "#mornExam-table > tbody > tr:nth-child(1) > td:nth-child(7) > button"
                                ).click()
                condtion = self.grade_today_morning_exam(query_select, exam_data)

                if condtion:
                    if exam_data["score"] == Service.get_ele(
                            self.driver, By.CSS_SELECTOR,
                            "#mornExam-table > tbody > tr:nth-child(1) > td:nth-child(6)").text:
                        actual = "today-attendance-pass"
                    else:
                        actual = "today-attendance-pass"
                else:
                    actual = "exam-null"

                if actual == "exam-null":
                    self.assertEqual(actual, "exam-null")
                else:
                    self.assertEqual(actual, expect)

        else:
            print("当前条件下，查询数据为空")
            self.driver.quit()

    # 测试用例
    @parameterized.expand(today_morning_test_data)
    def test_today_morning_exam(self,today_morning_query, today_morning_exam, expect):
        # cookie
        self.today_morning_exam_init()
        # 调用 查询 操作
        TodayMorningExam.today_attendance_query(self.driver,today_morning_query["name"])

        # 调用晨考 操作（本页面）
        self.verification_today_morning_exam(today_morning_exam, expect)

        self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)