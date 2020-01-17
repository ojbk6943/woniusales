import requests
import unittest
from parameterized import parameterized
from interface.util.Service import Service


# 登录页
open_deliver_resource_data = Service.get_excell_data("C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/testCase.xlsx",
    "deliver_resource", "open", 2, 4, 7)

query_deliver_resource_data = Service.get_excell_data("C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/testCase.xlsx",
    "deliver_resource", "query", 2, 4, 7)

update_deliver_resource_data = Service.get_excell_data("C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/testCase.xlsx",
    "deliver_resource", "update", 2, 4, 7)


class DeliverResourceTest(unittest.TestCase):

    # 自定义, 咨询主管账户
    def setUp(self):
        self.session = requests.session()
        # 登陆、解密
        Service.get_login(
            self.session, "C:/Users/wang/Desktop/woniuboss4.0/interface/config/roles.xlsx", "管理员")
        Service.get_decode(
            self.session, "C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/decode.xlsx",
                          "admin_decode", 2, 4, 7)

    # 打开 转交资源
    @parameterized.expand(open_deliver_resource_data)
    def test_open_deliver_resource(self, param):
        resp = Service.get_no_arguments(self.session, param["url"])

        if "转交资源" in resp.text:
            actual = "open-success"
        else:
            actual = "open-fail"
        # 断言
        self.assertEqual(actual, param["expect"])

    # 查询  转交资源
    @parameterized.expand(query_deliver_resource_data)
    def test_query_deliver_resource(self, param):
        resp = Service.post_arguments(self.session, param["url"], param["step"])
        sql_count = Service.query_deliver_resource_query_sql(param["step"], "../config/data_base")
        if int(resp.json()["totalRow"]) == sql_count:
            actual = "query-success"
        else:
            actual = "query-fail"
        # 断言
        self.assertEqual(actual, param["expect"])

    # 转交资源(转交后，判断数量)[无响应，只能从数据库中查询，前后变化]
    @parameterized.expand(update_deliver_resource_data)
    def test_update_deliver_resource(self, param):
        sql_count_one = Service.update_deliver_resource_query_sql(param["step"], "../config/data_base")
        Service.post_arguments(self.session, param["url"], param["step"])
        sql_count_two = Service.update_deliver_resource_query_sql(param["step"], "../config/data_base")
        # 断言
        if sql_count_two > sql_count_one:
            actual = "update-success"
        else:
            actual = "update-fail"
        # 断言
        self.assertEqual(actual, param["expect"])

if __name__ == '__main__':
    pass
    # unittest.main(verbosity=2)