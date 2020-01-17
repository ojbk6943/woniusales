import re
import unittest
import requests
from parameterized import parameterized
from interface.common.training_resource.TrainingResource import TrainingResource
from interface.config.try_to_encode_and_decode_woniu import WoniuBoss
from interface.util.Service import Service
from interface.util.Utility import Utility


open_training_resource_data = Utility.read_json(
    "../../test_data/training_resource/training_resource_module/open_transferee_data")

training_resource_data = Utility.read_json(
    "../../test_data/training_resource/training_resource_module/training_resource_data")

add_training_resource_data = Utility.read_json(
    "../../test_data/training_resource/training_resource_module/add_training_resource_data")

abandon_training_resource_data = Utility.read_json(
    "../../test_data/training_resource/training_resource_module/abandon_training_resource_data")

show_resume_resource_data = Utility.read_json(
    "../../test_data/training_resource/training_resource_module/show_resume_training_resource_data")

tracking_resource_data = Utility.read_json(
    "../../test_data/training_resource/training_resource_module/tracking_resource_data")

Modify_resource_data = Utility.read_json(
    "../../test_data/training_resource/training_resource_module/Modify_resource_data")

# 培训资源 子模块 培训资源
class TrainingResourceTest(unittest.TestCase):

    # 自定义，设定登录
    def setUp(self):
        self.session = requests.session()
        self.base_url = Utility.read_json("../../config/data_base")["BASEURL"]
        # 登录
        login_data = Utility.read_json("../../test_data/login_data/login_data")
        login_url = self.base_url + login_data[0][0]["login_url"]
        Service.login(self.session, login_url, login_data[0][1])
        # 解密
        decode_data = Utility.read_json("../../test_data/login_data/decode_data")
        decode_url = self.base_url + decode_data[0][0]["decode_url"]
        Service.decode(self.session, decode_url, decode_data[0][1])


    # 测试 打开培训资源页面
    @parameterized.expand(open_training_resource_data)
    def test_open_training_resource(self, url, expect):
        open_training_resource_url = self.base_url + url["open_training_resource_url"]
        open_training_resource_resp = \
            TrainingResource.open_training_resource(self.session, open_training_resource_url)
        if "培训资源" in open_training_resource_resp.text:
            actual = "open-training-resource-pass"
        else:
            actual = "open-training-resource-fail"
        self.assertEqual(actual, expect)

    # 测试 培训资源子模块 ： 培训资源, 查询功能
    @parameterized.expand(training_resource_data)
    def test_query_training_resource(self, url, query_training_resource_info, decode_info, expect):
        # 数据准备
        query_training_resource_url = self.base_url + url["query_training_resource_url"]
        query_training_resource_resp = TrainingResource.query_training_resource(
            self.session, query_training_resource_url, query_training_resource_info)
        query_result = query_training_resource_resp.json()

        # 拼接sql
        sql = Service.sql_query_training_resource(decode_info, "../../config/base_sql")

        # 调用数据库
        sql_result = Utility.get_connect_one(sql, "../../config/data_base")

        # 断言
        if sql_result[0] == query_result["totalRow"] and WoniuBoss.decode(
                decode_info["cusInfo"]) == query_result["list"][0]["name"]:

            actual = "query-training-resource-pass"
        else:
            actual = "query-training-resource-fail"

        self.assertEqual(actual, expect)

    # 测试 新增
    @parameterized.expand(add_training_resource_data)
    def test_training_resource_add(self, url, add_training_resource_info, expect):
        # 数据准备
        add_training_resource_url = self.base_url + url["add_training_resource_url"]
        add_training_resource_resp = TrainingResource.add_training_resource(
            self.session, add_training_resource_url, add_training_resource_info
        )
        # 响应文本
        add_result = add_training_resource_resp.text
        # 断言
        if "新增成功" in add_result:
            actual = "add-training-resource-pass"
        else:
            actual = "add-training-resource-fail"
        self.assertEqual(actual, expect)

    # 测试 废弃  /WoniuBoss2.5/resource/abandonResource
    @parameterized.expand(abandon_training_resource_data)
    def test_raining_resource_query_abandon(self, url, abandon_training_resource_info, expect):
        # 数据准备
        abandon_training_resource_url = self.base_url + url["abandon_training_resource_url"]
        abandon_training_resource_resp = TrainingResource.abandon_training_resource(
            self.session, abandon_training_resource_url, abandon_training_resource_info
        )
        # 响应文本
        abandon_result = abandon_training_resource_resp.text
        # 断言
        if "废弃资源完成" in abandon_result:
            actual = "abandon-training-resource-pass"
        else:
            actual = "abandon-training-resource-fail"
        self.assertEqual(actual, expect)

    # 测试 跟踪 (查看简历) /WoniuBoss2.5/resource/showResumeById
    @parameterized.expand(show_resume_resource_data)
    def test_raining_resource_show_resume(self, url, show_resume_training_resource_info, expect):
        # 数据准备
        show_resume_training_resource_url = self.base_url + url["show_resume_training_resource_url"]
        show_resume_training_resource_resp = TrainingResource.query_abandon_resource(
            self.session, show_resume_training_resource_url, show_resume_training_resource_info
        )
        # 响应json
        show_resume_result = show_resume_training_resource_resp.json()
        # 电话断言
        if re.match('^1[3456789]\d{9}$', show_resume_result["tel"]):
            actual = "show-resume-training-resource-pass"
        else:
            actual = "show-resume-training-resource-fail"
        self.assertEqual(actual, expect)

    # 测试  跟踪资源 /WoniuBoss2.5/resource/saveTrackingRecord
    @parameterized.expand(tracking_resource_data)
    def test_tracking_resource(self, url, tracking_resource_info, tracking_resource_sql, expect):
        # 调用之前，先查看数据库的记录数
        recode_count = Utility.get_connect_one(tracking_resource_sql["sql"], "../../config/data_base")
        # 数据准备
        tracking_resource_url = self.base_url + url["tracking_resource_url"]
        tracking_resource_url_resp = TrainingResource.tracking_resource(
            self.session, tracking_resource_url, tracking_resource_info
        )
        print(tracking_resource_url_resp.text)
        # 响应无内容，在数据库添加记录判断
        recode_count_again = Utility.get_connect_one(tracking_resource_sql["sql"], "../../config/data_base")
        # 电话断言
        if recode_count_again[0] > recode_count[0]:
            actual = "tracking-resource-pass"
        else:
            actual = "tracking-resource-fail"
        self.assertEqual(actual, expect)

    # 测试  修改  /WoniuBoss2.5/resource/modifyCusInfo  Modify_resource
    @parameterized.expand(Modify_resource_data)
    def test_modify_resource(self, url, modify_resource_info, expect):
        # 数据准备
        modify_resource_url = self.base_url + url["Modify_resource_url"]
        modify_resource_resp = TrainingResource.Modify_resource(
            self.session, modify_resource_url, modify_resource_info
        )
        # 响应文本
        modify_result = modify_resource_resp.text
        # 断言
        if "修改成功" in modify_result:
            actual = "modify-resource-pass"
        else:
            actual = "modify-resource-fail"
        self.assertEqual(actual, expect)



if __name__ == '__main__':
    unittest.main(verbosity=2)