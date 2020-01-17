import re
import requests
import unittest
from parameterized import parameterized
from interface.util.Service import Service


# 登录页
open_public_resource_data = Service.get_excell_data("C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/testCase.xlsx",
    "public_resource", "open", 2, 4, 7)

claim_public_resource_data = Service.get_excell_data("C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/testCase.xlsx",
    "public_resource", "claim", 2, 4, 7)

query_public_resource_data = Service.get_excell_data("C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/testCase.xlsx",
    "public_resource", "query", 2, 4, 7)



class PublicResourceTest(unittest.TestCase):

    # 自定义, 咨询主管账户
    def setUp(self):
        self.session = requests.session()
        # 登陆、解密
        Service.get_login(
            self.session, "C:/Users/wang/Desktop/woniuboss4.0/interface/config/roles.xlsx", "咨询主管")
        Service.get_decode(
            self.session, "C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/decode.xlsx",
                          "decode", 2, 4, 7)

    # 打开公共资源
    @parameterized.expand(open_public_resource_data)
    def test_claim_public_resource(self, param):
            resp = Service.get_no_arguments(self.session, param["url"])

            if "公共资源" in resp.text:
                actual = "claim-public-success"
            else:
                actual = "open-public-source-fail"
            # 断言
            self.assertEqual(actual, param["expect"])

    # 认领资源
    @parameterized.expand(claim_public_resource_data)
    def test_claim_public_resource(self, param):
        resp = Service.post_arguments(self.session, param["url"], param["step"])

        if re.match('\d+', resp.text):
            actual = "claim-public-success"
        else:
            actual = "claim-public-fail"
        # 断言
        self.assertEqual(actual, param["expect"])

    # 查询资源
    @parameterized.expand(query_public_resource_data)
    def test_query_public_resource(self, param):
        resp = Service.post_arguments(self.session, param["url"], param["step"])
        sql_count = Service.query_public_resource_query_sql(param["step"], "../config/data_base")

        if int(resp.json()["totalRow"]) == sql_count:
            actual = "query-public-success"
        else:
            actual = "query-public-fail"
        # 断言
        self.assertEqual(actual, param["expect"])

if __name__ == '__main__':
    pass
    # unittest.main(verbosity=2)