import re
import time
import unittest

from parameterized import parameterized
from selenium import webdriver
from selenium.webdriver.common.by import By

from gui.common.trainees_management.TodayAttendance import TodayAttendance
from gui.util.Service import Service
from gui.util.Utility import Utility


today_attendance_test_data = Utility.read_json("../test_data/trainees_management_data/today_attendance_data")


class TodayAttendanceTest(unittest.TestCase):

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
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "今日考勤").click()

        # 解密
        Service.get_ele(self.driver, By.ID, "btn-decrypt").click()
        decode_input_ele = Service.get_ele(self.driver,
                                           By.CSS_SELECTOR, "#secondPass-modal > div > div > "
                                                            "div.modal-body.text-center > input[type=password]")
        Service.input_value_ele(decode_input_ele, self.config_info["DECODE"])
        # 点击确定
        Service.get_ele(self.driver, By.CSS_SELECTOR,
                        "#secondPass-modal > div > div > div.modal-footer > button").click()

    # 判断当前页面（课程安排）是否有数据
    def verification_today_attendance_result(self, driver):
        # 判断自身、区域有无数据
        query_result_class = Service.get_ele(driver, By.CSS_SELECTOR, "table#attendance_table tbody").text
        if query_result_class != "无符合条件的记录":
            # 前端页面显示数据数，根据状态（不同状态数量不同）
            query_count_result = Service.get_ele(
                driver, By.CSS_SELECTOR,
                "#atten > div.bootstrap-table > div.fixed-table-container > div.fixed-table-pagination > "
                "div.pull-left.pagination-detail > span.pagination-info").text
            result = re.match('^显示.*，总.*?(\d+)', query_count_result).group(1)
        else:
            result = 0
        return result

    # 单个用户考勤
    def single_today_attendance(self,status,expect):
        # 选中，确定，判断
        select_one_ele = Service.get_ele(self.driver, By.CSS_SELECTOR,
                                         "#attendance_table > tbody > tr:nth-child(1) > td:nth-child(7) > select")

        Service.get_select_result(select_one_ele, status)
        Service.get_ele(self.driver, By.CSS_SELECTOR,
                        "#attendance_table > tbody > tr:nth-child(1) > td:nth-child(7) > button").click()
        # 验证
        select_two_ele = Service.get_ele(self.driver, By.CSS_SELECTOR,
                                         "#attendance_table > tbody > tr > td:nth-child(6)").text
        if select_two_ele == status:
            actual = "today-attendance-pass"
        else:
            actual = "today-attendance-fail"
            print("单个学生考勤错误")
        self.assertEqual(actual,expect)

    # 测试用例，先执行单个学生考勤，在执行批量考勤
    @parameterized.expand(today_attendance_test_data)
    def test_today_attendance(self, today_name, today_status,expect):
        # cookie
        self.course_arrangement_init()

        # 批量考勤
        # 判断当前条件下，有无数据  判断有无元素，以及有多少个
        class_query_result = self.verification_today_attendance_result(self.driver)

        # 学生数量不为 0
        if int(class_query_result) != 0:

            # 判断学生数量 一页数据大于10，分页
            if int(class_query_result) > 10:

                # 翻页功能
                page_count_ele = Service.get_eles(self.driver, By.CSS_SELECTOR,
                                                  "#atten > div.bootstrap-table > div.fixed-table-container > "
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
                                                      "#attendance_table > tbody > tr")
                if len(query_result_count) > 1:
                    # 选中第一个
                    one_query_select = Service.get_tier_ele(query_result_count[0], By.XPATH,
                                         "//*[@id='attendance_table']/tbody/tr[1]/td[7]/select")
                    Service.get_select_result(one_query_select, today_status["status"])
                    # 本页最后一个
                    css_count = "#attendance_table > tbody > tr:nth-child(%d) > td:nth-child(7) > " \
                                "select" % (len(query_result_count))

                    # # 得到姓名，验证一下
                    # css_count_name = Service.get_ele(self.driver,By.CSS_SELECTOR,
                    #                             "#attendance_table > tbody > tr:nth-child(%d) > "
                    #                             "td:nth-child(1)"%(len(query_result_count))).text
                    time.sleep(2)
                    two_query_select = Service.get_tier_ele(query_result_count[len(query_result_count) - 1],
                                                            By.CSS_SELECTOR, css_count)

                    Service.get_select_result(two_query_select, today_status["status"])

                    # 批量 操作
                    TodayAttendance.today_attendance_check(self.driver)

                else:
                    # 选中第一个
                    one_query_select = Service.get_tier_ele(query_result_count[0], By.XPATH,
                                                            "//*[@id='attendance_table']/tbody/tr[1]/td[7]/select")
                    Service.get_select_result(one_query_select, today_status["status"])

                    # 批量 操作
                    TodayAttendance.today_attendance_check(self.driver)

            # 不分页
            elif int(class_query_result) > 1:
                # 当前页展示信息个数
                query_result_count = Service.get_eles(self.driver, By.CSS_SELECTOR,
                                                      "#attendance_table > tbody > tr")
                # 选中第一个
                one_query_select = Service.get_tier_ele(query_result_count[0], By.XPATH,
                                                        "//*[@id='attendance_table']/tbody/tr[1]/td[7]/select")
                Service.get_select_result(one_query_select, today_status["status"])
                # 本页最后一个
                css_count = "#attendance_table > tbody > tr:nth-child(%d) > td:nth-child(7) > " \
                            "select" % (len(query_result_count))

                # # 得到姓名，验证一下
                # css_count_name = Service.get_ele(self.driver,By.CSS_SELECTOR,
                #                             "#attendance_table > tbody > tr:nth-child(%d) > "
                #                             "td:nth-child(1)"%(len(query_result_count))).text
                time.sleep(2)
                two_query_select = Service.get_tier_ele(query_result_count[len(query_result_count) - 1],
                                                        By.CSS_SELECTOR, css_count)

                Service.get_select_result(two_query_select, today_status["status"])

                # 批量 操作
                TodayAttendance.today_attendance_check(self.driver)

            # 一条数据，用全选，选中元素，然后分班
            else:
                self.single_today_attendance(today_status["status"],expect)

        else:
            print("当前条件下，查询数据为空")
            self.driver.quit()

        # 单个学生
        TodayAttendance.today_attendance_query(self.driver, today_name["name"])
        # 验证学生考勤
        self.single_today_attendance(today_status["status"],expect)

        self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)