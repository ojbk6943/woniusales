import requests
import unittest
from parameterized import parameterized
from interface.util.Service import Service
from interface.util.Utility import Utility

open_advisory_department = Utility.read_json(
    "../../test_data/training_resource/report_center_data/open_advisory_department_data")


'''报表中心子模块，咨询部'''

class AdvisoryDepartmentTest(unittest.TestCase):
    # 自定义，初始化driver，窗口最大化，隐式等待
    def setUp(self):
        self.session = requests.session()
        self.base_url = Utility.read_json("../../config/data_base")["BASEURL"]
        # 登陆（admin）、解密
        login_path = "../../test_data/login_data/login_data"
        decode_path = "../../test_data/login_data/decode_data"
        Service.get_login_decode(self.base_url, self.session, login_path, decode_path)

    # 用例，打开分配资源页面
    @parameterized.expand(open_advisory_department)
    def test_open_advisory_department(self, url, expect):
        open_advisory_department_url = self.base_url + url["open_allocating_resource_url"]
        open_advisory_department_resp = Service.get_no_arguments(self.session, open_advisory_department_url)
        if "分配资源" in open_allocating_resource_resp.text:
            actual = "open-allocating-resource-pass"
        else:
            actual = "open-allocating-resource-fail"
        self.assertEqual(actual, expect)


if __name__ == '__main__':
    unittest.main(verbosity=2)