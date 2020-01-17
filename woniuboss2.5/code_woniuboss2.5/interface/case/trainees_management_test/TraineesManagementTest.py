import requests
import unittest
from parameterized import parameterized
from interface.util.Service import Service
from interface.util.Utility import Utility


# 数据
basic_info_modify_data = Utility.read_json(
    "../../test_data/trainees_management_data/trainees_management_module/basic_info_modify_data")


class TraineesManagementTest(unittest.TestCase):

    # 自定义，初始化driver，窗口最大化，隐式等待
    def setUp(self):
        self.session = requests.session()
        self.base_url = self.base_url = Utility.read_json("../../config/data_base")["BASEURL"]
        # 登陆（咨询主管：李毅）、解密
        teacher_login_path = "../../test_data/login_data/teacher_manage_login_data"
        decode_path = "../../test_data/login_data/decode_data"
        Service.get_login_decode(self.base_url, self.session, teacher_login_path, decode_path)

    # 修改
    @parameterized.expand(basic_info_modify_data)
    def test_basic_info_modify(self, url, expect):
        basic_info_modify_url = self.base_url + url["basic_info_modify_url"]
        print(basic_info_modify_url)
        files = {'fileToUpload':
                     ('basic_info_modify_info.txt', open('C:/Users/wang/Desktop/woniuboss_automation/interface/test_data/trainees_management_data/trainees_management_module/basic_info_modify_info.txt', 'rb'))}
        basic_resp = requests.post(basic_info_modify_url, files=files)
        print(basic_resp.text)
if __name__ == '__main__':

    unittest.main(verbosity=2)