import re
import requests
import unittest
from parameterized import parameterized
from interface.util.Service import Service
from interface.util.Utility import Utility

open_common_resource_pool_data = Utility.read_json(
    "../../test_data/training_resource/common_resource_pool_module/open_common_resource_pool_data")

query_common_resource_pool_data = Utility.read_json(
    "../../test_data/training_resource/common_resource_pool_module/query_common_resource_pool_data")

claim_data = Utility.read_json(
    "../../test_data/training_resource/common_resource_pool_module/claim_data")

class CommonResourcePoolTest(unittest.TestCase):

    # 开始
    def setUp(self):
        self.session = requests.session()
        self.base_url = Utility.read_json("../../config/data_base")["BASEURL"]
        # 登陆（咨询主管：郑雪姣）、解密
        counselor_login_path = "../../test_data/login_data/counselor_login_data"
        decode_path = "../../test_data/login_data/decode_data"
        Service.get_login_decode(self.base_url, self.session, counselor_login_path, decode_path)

    # 打开页面，公共资源池
    @parameterized.expand(open_common_resource_pool_data)
    def test_open_common_resource_pool(self, url, expect):
        open_common_resource_pool_url = self.base_url + url["open_common_resource_pool_url"]
        open_common_resource_pool_resp = Service.get_no_arguments(self.session, open_common_resource_pool_url)
        if "公共资源池" in open_common_resource_pool_resp.text:
            actual = "open-common-resource-pool-pass"
        else:
            actual = "open-common-resource-pool-fail"
        self.assertEqual(actual, expect)

    # 查询
    @parameterized.expand(query_common_resource_pool_data)
    def test_query_common_resource_pool(self, url, query_common_resource_pool_info, expect):
        # 数据准备，调用
        query_common_resource_pool_url = self.base_url + url["query_common_resource_pool_url"]
        query_common_resource_pool_resp = Service.post_arguments(
            self.session, query_common_resource_pool_url, query_common_resource_pool_info)
        query_common_resp_result = query_common_resource_pool_resp.json()
        # 查询数据库
        sql = Service.sql_query_common_resource_pool(
            query_common_resource_pool_info, "../../config/query_common_resource_pool_sql")

        sql_result = Utility.get_connect_one(sql, "../../config/data_base")

        # 响应数据数量
        if sql_result[0] == query_common_resp_result["totalRow"]:
            actual = "query-common-resource-pass"
        else:
            actual = "query-common-resource-fail"
        self.assertEqual(actual, expect)

    # 认领 /WoniuBoss2.5/public/ownResource
    @parameterized.expand(claim_data)
    def test_claim(self, url, claim_info, expect):
        claim_url = self.base_url + url["claim_url"]
        # 提交前，看数量
        sql = "select count(work_id) from customer where pool_type='public'"
        count_sql = Utility.get_connect_one(sql, '../../config/data_base')
        # 无响应
        Service.post_arguments(self.session, claim_url, claim_info)
        # 提交后
        count_sql_again = Utility.get_connect_one(sql, '../../config/data_base')
        # 无响应，数据库查询
        if count_sql_again[0] <= count_sql[0]:
            # 响应断言
            actual = "claim-pass"
        else:
            actual = "claim-pass"
        self.assertEqual(actual, expect)
if __name__ == '__main__':
    unittest.main(verbosity=2)