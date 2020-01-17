import re
import requests
import unittest
from parameterized import parameterized
from interface.util.Service import Service
from interface.util.Utility import Utility


# 登录页
open_training_resource_data = Service.get_excell_data("C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/testCase.xlsx",
    "training-resource", "open", 2, 4, 7)

add_training_resource_data = Service.get_excell_data("C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/testCase.xlsx",
    "training-resource", "add", 2, 4, 7)

query_training_resource_data = Service.get_excell_data("C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/testCase.xlsx",
    "training-resource", "query", 2, 4, 7)

page_training_resource_data = Service.get_excell_data("C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/testCase.xlsx",
    "training-resource", "paging", 2, 4, 7)

open_tracking_training_resource_data = Service.get_excell_data("C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/testCase.xlsx",
    "training-resource", "oTracking", 2, 4, 7)

tracking_training_resource_data = Service.get_excell_data("C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/testCase.xlsx",
    "training-resource", "save", 2, 4, 7)

target_tracking_training_resource_data = Service.get_excell_data("C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/testCase.xlsx",
    "training-resource", "target", 2, 4, 7)

modify_training_resource_data = Service.get_excell_data("C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/testCase.xlsx",
    "training-resource", "modify", 2, 4, 7)

abandon_training_resource_data = Service.get_excell_data("C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/testCase.xlsx",
    "training-resource", "abandon", 2, 4, 7)



class TraineesManagementTest(unittest.TestCase):

    # 自定义, 咨询主管账户
    def setUp(self):
        self.session = requests.session()
        # 登陆、解密
        Service.get_login(
            self.session, "C:/Users/wang/Desktop/woniuboss4.0/interface/config/roles.xlsx", "咨询主管")
        Service.get_decode(
            self.session, "C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/decode.xlsx",
                          "decode", 2, 4, 7)

    # 打开分配资源
    @parameterized.expand(open_training_resource_data)
    def test_open_training_resource(self, param):
            resp = Service.get_no_arguments(self.session, param["url"])

            if "培训资源" in resp.text:
                actual = "open-training-success"
            else:
                actual = "open-training-fail"
            # 断言
            self.assertEqual(actual, param["expect"])

    # 新增
    @parameterized.expand(add_training_resource_data)
    def test_add_training_resource(self, param):
        resp = Service.post_arguments(self.session, param["url"], param["step"])

        if "新增成功" in resp.text:
            actual = "add-training-success"
        else:
            actual = "add-training-fail"
        # 断言
        self.assertEqual(actual, param["expect"])

    # 查询
    @parameterized.expand(query_training_resource_data)
    def test_query_training_resource(self, param):
        resp = Service.post_arguments(self.session, param["url"], param["step"])
        sql_count = Service.training_resource_query_sql(param["step"], "../config/data_base")
        if int(resp.json()["totalRow"]) == sql_count:

            actual = "query-training-success"
        else:
            actual = "query-training-fail"

        self.assertEqual(actual, param["expect"])

    # 翻页
    @parameterized.expand(page_training_resource_data)
    def test_page_training_resource(self, param):
        resp = Service.post_arguments(self.session, param["url"], param["step"])
        if int(resp.json()["pageNumber"]) == int(param["step"]["pageIndex"]):
            actual = "page-success"
        else:
            actual = "page-fail"

        self.assertEqual(actual, param["expect"])

    # 跟踪（正常打开）
    @parameterized.expand(open_tracking_training_resource_data)
    def test_open_tracking_training_resource(self, param):
        resp = Service.post_arguments(self.session, param["url"], param["step"])
        # 解密、日期格式（创建日期）
        result = Utility.get_secret(resp.text).split("&")[1]
        if re.match('20\d{2}-\d{2}-\d{2} \d{2}:\d{2}', result):
            actual = "open-tracking-success"
        else:
            actual = "open-tracking-fail"

        self.assertEqual(actual, param["expect"])

    # 打开跟踪资源 选项
    @parameterized.expand(target_tracking_training_resource_data)
    def test_target_tracking_training_resource(self, param):

        resp = Service.post_arguments(self.session, param["url"], param["step"])
        sql = "select tracking_times from customer where customer_id = '%s'"%(param["step"]["id"])
        count_one = Utility.get_connect_one(sql, "../config/data_base")[0]
        if count_one == len(resp.json()):
            actual = "target-tracking-success"
        else:
            actual = "target-tracking-fail"
        self.assertEqual(actual, param["expect"])

    # 跟踪资源
    @parameterized.expand(tracking_training_resource_data)
    def test_tracking_training_resource(self, param):

        sql = "select count(tracking_record_id) from tracking_record"
        count_one = Utility.get_connect_one(sql, "../config/data_base")[0]
        resp = Service.post_arguments(self.session, param["url"], param["step"])
        # 解密、日期格式（创建日期）
        count_two = Utility.get_connect_one(sql, "../config/data_base")[0]
        if resp.text == "newStudent" or count_two > count_one:
            actual = "tracking-success"
        else:
            actual = "tracking-fail"

        self.assertEqual(actual, param["expect"])

    # 修改资源
    @parameterized.expand(modify_training_resource_data)
    def test_tracking_training_resource(self, param):

        resp = Service.post_arguments(self.session, param["url"], param["step"])
        # 响应文本

        if "修改成功" in resp.text:
            actual = "modify-success"
        else:
            actual = "modify-fail"

        self.assertEqual(actual, param["expect"])

    # 废弃资源
    @parameterized.expand(abandon_training_resource_data)
    def test_abandon_training_resource(self, param):

        resp = Service.post_arguments(self.session, param["url"], param["step"])
        # 响应文本
        if "废弃资源完成" in resp.text:
            actual = "abandon-success"
        else:
            actual = "abandon-fail"

        self.assertEqual(actual, param["expect"])

if __name__ == '__main__':
    pass
    # unittest.main(verbosity=2)