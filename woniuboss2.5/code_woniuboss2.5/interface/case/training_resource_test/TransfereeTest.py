import unittest
from parameterized import parameterized
from interface.common.training_resource.Transferee import Transferee
from interface.util.Service import Service
from interface.util.Utility import Utility
import re
import requests


# 数据
open_transferee_data = Utility.read_json(
    "../../test_data/training_resource/transferee_module/open_transferee_data")

trans_feree_data = Utility.read_json(
    "../../test_data/training_resource/transferee_module/trans_feree_data")

show_resume_data = Utility.read_json(
    "../../test_data/training_resource/transferee_module/show_resume_data")

switch_page_data = Utility.read_json(
    "../../test_data/training_resource/transferee_module/switch_page_data")

submit_data = Utility.read_json(
    "../../test_data/training_resource/transferee_module/submit_data")

'''培训资源模块  子模块 转让责任人'''
class TransfereeTest(unittest.TestCase):

    # 自定义，登录、解密
    def setUp(self):
        self.session = requests.session()
        self.base_url = Utility.read_json("../../config/data_base")["BASEURL"]
        # 登录、解密
        login_path = "../../test_data/login_data/login_data"
        decode_path = "../../test_data/login_data/decode_data"
        Service.get_login_decode(self.base_url, self.session, login_path, decode_path)

    # 测试打开 转让责任人
    @parameterized.expand(open_transferee_data)
    def test_open_trans_feree(self, url, expect):
        open_trans_feree_url = self.base_url + url["open_transferee_url"]
        open_trans_feree_resp = Transferee.open_trans_feree(self.session, open_trans_feree_url)
        if "转交责任人" in open_trans_feree_resp.text:
            actual = "open-trans-feree-pass"
        else:
            actual = "open-trans-feree-fail"
        self.assertEqual(actual, expect)

    # 测试 培训资源子模块 ： 培训资源, 查询功能
    @parameterized.expand(trans_feree_data)
    def test_query_trans_feree(self, url, query_trans_feree_info,  expect):
        # 数据准备
        query_trans_feree_url = self.base_url + url["query_trans_feree_url"]
        query_trans_feree_resp = Transferee.query_trans_feree(
            self.session, query_trans_feree_url, query_trans_feree_info)
        query_result = query_trans_feree_resp.json()

        # 拼接sql
        sql = Service.sql_query_trans_feree(query_trans_feree_info, "../../config/transferee_query_sql")

        # 调用数据库
        sql_result = Utility.get_connect_one(sql, "../../config/data_base")
        # print(sql_result)
        # 断言
        if sql_result[0] == query_result["totalRow"]:

            actual = "query-trans-feree-pass"
        else:
            actual = "query-trans-feree-pass"

        self.assertEqual(actual, expect)

    # 查询后的 查看
    @parameterized.expand(show_resume_data)
    def test_query_show_resume(self, url, show_resume_info,  expect):
        show_resume_url = self.base_url + url["show_resume_url"]
        show_resume_resp = Transferee.show_resume(self.session, show_resume_url, show_resume_info)
        show_resume_result = show_resume_resp.json()

        if re.match('^1[3456789]\d{9}$', show_resume_result["tel"]):
            actual = "show-resume-pass"
        else:
            actual = "show-resume-pass"
        self.assertEqual(actual, expect)

    # 切换页数  /WoniuBoss2.5/transmit/queryResourcesByInfo
    @parameterized.expand(switch_page_data)
    def test_query_switch_page(self, url, switch_page_info, expect):
        switch_page_url = self.base_url + url["switch_page_url"]
        switch_page_resp = Transferee.switch_page(self.session, switch_page_url, switch_page_info)

        switch_page_result = switch_page_resp.json()
        # 断言
        if switch_page_info["pageIndex"] == switch_page_result["pageNumber"]:

            actual = "switch-page-pass"
        else:
            actual = "switch-page-pass"

        self.assertEqual(actual, expect)


    # 提交  /WoniuBoss2.5/transmit/updateTransmit
    @parameterized.expand(submit_data)
    def test_submit(self, url, submit_info, expect):
        submit_url = self.base_url + url["submit_url"]
        # 提交前，看数量
        sql = "select count(work_id) from customer where work_id='%s'" % (submit_info["workId"])
        count_work_id = Utility.get_connect_one(sql, '../../config/data_base')
        submit_resp = Transferee.submit_trans(self.session, submit_url, submit_info)
        # 提交后
        count_work_id_submit = Utility.get_connect_one(sql, '../../config/data_base')
        # 无响应，数据库查询
        if count_work_id_submit[0] >= count_work_id[0]:
            actual = "submit-pass"
        else:
            actual = "submit-fail"

        self.assertEqual(actual, expect)
if __name__ == '__main__':
    unittest.main(verbosity=2)




