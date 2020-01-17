import requests
from parameterized import parameterized
from interface.util.Service import Service
import unittest


 # 打开首页
roles = Service.get_role_info(
    "C:/Users/wang/Desktop/woniuboss4.0/interface/config/roles.xlsx", "讲师")

# 首页
open_page_data = Service.get_excell_data("C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/testCase.xlsx",
    "open_page", "open", 2, 4, 7)

# 登录页
login_data = Service.get_excell_data("C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/testCase.xlsx",
    "login", "login", 2, 4, 7)


# 解密
decode_data = Service.get_excell_data("C:/Users/wang/Desktop/woniuboss4.0/interface/test_data/testCase.xlsx",
    "decode", "decode", 2, 4, 7)

# 登陆账户
login_info = Service.get_role_info(
    "C:/Users/wang/Desktop/woniuboss4.0/interface/config/roles.xlsx", "咨询主管")



class LoginTest(unittest.TestCase):

    # 初始化
    def setUp(self):
        self.session = requests.session()

    # 测试首页
    @parameterized.expand(open_page_data)
    def test_open_page(self, param):
        open_page_resp = Service.get_no_arguments(self.session, param["url"])
        if "BOSS系统" in open_page_resp.text :
            actual = "open-page-pass"
        else:
            actual = "open-page-fail"
        self.assertEqual(actual, param["expect"])

    # 验证登录
    @parameterized.expand(login_data)
    def test_login(self, param):

        login_resp = Service.post_arguments(self.session, param["url"], param["step"])
        if login_resp.text == "success":
            actual = "login-success"
        else:
            actual = "login-fail"
        self.assertEqual(actual, param["expect"])

    # 解密
    @parameterized.expand(decode_data)
    def test_login_decode(self, param):
        Service.post_arguments(self.session, login_info[0], login_info[1])
        decode_resp = Service.post_arguments(self.session, param["url"], param["step"])
        if decode_resp.text == "yes":
            actual = "decode-success"
        else:
            actual = "decode-fail"
        self.assertEqual(actual, param["expect"])

if __name__ == '__main__':
    pass
    # unittest.main(verbosity=2)