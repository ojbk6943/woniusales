import requests
import unittest
from parameterized import parameterized
from interface.util.Service import Service
from interface.util.Utility import Utility

open_allocating_resource_data = Utility.read_json(
    "../../test_data/training_resource/allocating_resource_module/open_allocating_resource_data")

allocating_resource_data = Utility.read_json(
    "../../test_data/training_resource/allocating_resource_module/query_allocating_resource_data")

commit_allocating_resource_data = Utility.read_json(
    "../../test_data/training_resource/allocating_resource_module/commit_allocating_resource_data")


'''培训资源子模块，分配资源'''

class AllocatingResourceTest(unittest.TestCase):
    # 自定义，初始化driver，窗口最大化，隐式等待
    def setUp(self):
        self.session = requests.session()
        self.base_url = Utility.read_json("../../config/data_base")["BASEURL"]
        # 登陆（咨询主管：郑雪姣）、解密
        counselor_login_path = "../../test_data/login_data/counselor_login_data"
        decode_path = "../../test_data/login_data/decode_data"
        Service.get_login_decode(self.base_url, self.session, counselor_login_path, decode_path)

    # 用例，打开分配资源页面
    @parameterized.expand(open_allocating_resource_data)
    def test_open_allocating_resource(self, url, expect):
        open_allocating_resource_url = self.base_url + url["open_allocating_resource_url"]
        open_allocating_resource_resp = Service.get_no_arguments(self.session, open_allocating_resource_url)
        if "分配资源" in open_allocating_resource_resp.text:
            actual = "open-allocating-resource-pass"
        else:
            actual = "open-allocating-resource-fail"
        self.assertEqual(actual, expect)

    # 查询
    # 测试 培训资源子模块 ： 培训资源, 查询功能
    @parameterized.expand(allocating_resource_data)
    def test_query_allocating_resource(self, url, allocating_resource_info, expect):
        # 数据准备
        query_allocating_resource_url = self.base_url + url["query_allocating_resource_url"]

        query_allocating_resource_resp = Service.post_arguments(
            self.session, query_allocating_resource_url, allocating_resource_info)

        query_result = query_allocating_resource_resp.json()

        # 拼接sql
        sql = Service.sql_query_trans_feree(allocating_resource_info, "../../config/transferee_query_sql")

        # 调用数据库
        sql_result = Utility.get_connect_one(sql, "../../config/data_base")
        # print(sql_result)
        # 断言
        if sql_result[0] == query_result["totalRow"]:

            actual = "query-trans-feree-pass"
        else:
            actual = "query-trans-feree-pass"

        self.assertEqual(actual, expect)

    # 分配
    @parameterized.expand(commit_allocating_resource_data)
    def test_commit_allocating_resource(self, url, commit_allocating_resource_info, expect):
        open_allocating_resource_url = self.base_url + url["commit_allocating_resource_info"]

        # 提交前，看数量
        sql = "select count(work_id) from customer where work_id='%s'" % (commit_allocating_resource_info["work_id"])
        count_work_id = Utility.get_connect_one(sql, '../../config/data_base')
        # 响应为空
        Service.post_arguments(self.session, open_allocating_resource_url, commit_allocating_resource_info)
        # 提交后
        count_work_id_commit = Utility.get_connect_one(sql, '../../config/data_base')
        # 无响应，数据库查询
        if count_work_id_commit[0] >= count_work_id[0]:
            actual = "commit-allocating-resource-pass"
        else:
            actual = "commit-allocating-resource-fail"

        self.assertEqual(actual, expect)



if __name__ == '__main__':
    unittest.main(verbosity=2)