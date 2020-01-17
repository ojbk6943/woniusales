import re

import requests
import unittest
from parameterized import parameterized
from interface.util.Service import Service


# 登录页
allot_allocation_resource_data = Service.get_excell_data("C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/testCase.xlsx",
    "allot-resource", "allot", 2, 4, 7)

query_allocation_resource_data = Service.get_excell_data("C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/testCase.xlsx",
    "allot-resource", "query", 2, 4, 7)

scale_allocation_resource_data = Service.get_excell_data("C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/testCase.xlsx",
    "allot-resource", "scale", 2, 4, 7)

class AllotResourceTest(unittest.TestCase):

    # 自定义, 咨询主管账户
    def setUp(self):
        self.session = requests.session()
        # 登陆、解密
        Service.get_login(
            self.session, "C:/Users/wang/Desktop/woniuboss4.0/interface/config/roles.xlsx", "咨询主管")
        Service.get_decode(
            self.session, "C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/decode.xlsx",
                          "decode", 2, 4, 7)

    # 分配资源
    @parameterized.expand(allot_allocation_resource_data)
    def test_allot_allocation_resource(self, param):
            resp = Service.post_arguments(self.session, param["url"], param["step"])

            if re.match('\d+', resp.text):
                actual = "allot-success"
            else:
                actual = "allot-fail"
            # 断言
            self.assertEqual(actual, param["expect"])

    # 查询资源
    @parameterized.expand(query_allocation_resource_data)
    def test_query_allocation_resource(self, param):
        resp = Service.post_arguments(self.session, param["url"], param["step"])
        sql_count = Service.allot_resource_query_sql(param["step"], "../config/data_base")
        if int(resp.json()["totalRow"]) == sql_count:
            actual = "query-success"
        else:
            actual = "query-fail"
        # 断言
        self.assertEqual(actual, param["expect"])

    # 按比例分配资源
    @parameterized.expand(scale_allocation_resource_data)
    def test_scale_allocation_resource(self, param):
        resp = Service.post_arguments(self.session, param["url"], param["step"])
        if "success" == resp.text:
            actual = "scale-allot-success"
        else:
            actual = "scale-allot-fail"
        # 断言
        self.assertEqual(actual, param["expect"])


if __name__ == '__main__':
    pass
    # unittest.main(verbosity=2)