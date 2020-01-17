from selenium.webdriver.common.by import By

from gui.util.Service import Service


class Login:

    # 首页
    @classmethod
    def open_page(cls,driver,url):
        driver.get(url)

    # 登录，元素有：用户框、密码框、验证码框、登录按钮
    @classmethod
    def login(cls,driver,url,login_info):
        driver.get(url)
        # 数据
        uname_ele = Service.get_ele(driver,By.CSS_SELECTOR,"div.row:nth-child(1) > input:nth-child(1)")
        Service.input_value_ele(uname_ele,login_info["uname"])
        upass_ele = Service.get_ele(driver,By.CSS_SELECTOR,"div.row:nth-child(2) > input:nth-child(1)")
        Service.input_value_ele(upass_ele, login_info["upass"])
        verify_code_ele = Service.get_ele(driver,By.CSS_SELECTOR,"input.col-md-6")
        Service.input_value_ele(verify_code_ele, login_info["verifycode"])
        # 点击登录
        login_ele = Service.get_ele(driver, By.CSS_SELECTOR, ".btn")
        login_ele.click()
        # print(driver.get_cookies())
