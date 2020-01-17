import requests
from parameterized import parameterized
from interface.common.login.Login import Login
import unittest
from interface.util.Utility import Utility



 # 打开首页
open_page_data = Utility.read_json("../../test_data/login_data/open_page_data")

# 登陆数据
login_data = Utility.read_json("../../test_data/login_data/login_data")

# 解密数据
decode_data = Utility.read_json("../../test_data/login_data/decode_data")


class LoginTest(unittest.TestCase):
    # 初始化
    def setUp(self):
        self.session = requests.session()
        self.base_url = Utility.read_json("../../config/data_base")["BASEURL"]

    # 测试首页
    @parameterized.expand(open_page_data)
    def test_open_page(self, open_page_url, expect):

        open_page_url = self.base_url + open_page_url["open_page_url"]
        open_page_resp = Login.open_page(self.session,open_page_url)

        if "Boss系统" in open_page_resp.text :
            actual = "open-page-pass"
        else:
            actual = "open_page-fail"
        self.assertEqual(actual, expect)

    # 验证登录
    @parameterized.expand(login_data)
    def test_login(self, login_url, login_info, expect):
        login_url = self.base_url + login_url["login_url"]
        login_resp = Login.login(self.session,login_url,login_info)
        if login_resp.text == "success":
            actual = "login-pass"
        else:
            actual = "login-fail"
        self.assertEqual(actual,expect)
    # 解密
    @parameterized.expand(decode_data)
    def test_decode(self, decode_url, decode_info, expect):
        decode_url = self.base_url + decode_url["decode_url"]
        decode_resp = Login.decode(self.session, decode_url, decode_info)
        if decode_resp.text == "yes":
            actual = "decode-pass"
        else:
            actual = "decode-fail"
        self.assertEqual(actual, expect)

if __name__ == '__main__':
    unittest.main(verbosity=2)