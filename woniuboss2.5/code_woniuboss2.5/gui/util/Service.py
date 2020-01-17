import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from random import randint
from gui.util.Utility import Utility
from selenium import webdriver

class Service:

    # 判断元素是否存在
    @classmethod
    def is_Element_present(cls,driver,how,what):
        from selenium.common.exceptions import NoSuchElementException
        try:
            driver.find_element(by=how,value=what)
            return True
        except NoSuchElementException as e:
            return False

    # 寻找元素
    @classmethod
    def get_ele(cls,driver,how,what):
        try:
            return driver.find_element(by=how,value=what)
        except:
            return None

    # 寻找复数元素
    @classmethod
    def get_eles(cls, driver, how, what):
        try:
            return driver.find_elements(by=how, value=what)
        except:
            return None

    # 层级关系寻找下级元素
    @classmethod
    def get_tier_ele(cls,current_ele,how,what):
        try:
            return current_ele.find_element(by=how, value=what)
        except:
            return None

    # 格式化日期
    @classmethod
    def format_date(cls):
        return time.strftime('%Y-%m-%d',time.localtime())

    # 输入类型元素，三步骤：点击、清空、输入值
    @classmethod
    def input_value_ele(cls,ele,data_info):
        ele.click()
        ele.clear()
        ele.send_keys(data_info)

    # 输入框文本内容+日期
    @classmethod
    def input_value_date_ele(cls,ele,date):
        content = ele.get_attribute("value") + date
        ele.click()
        ele.clear()
        ele.send_keys(content)
        return content

    # 输入日期，先删除10个日期位置
    @classmethod
    def get_input(cls, ele, data_info):
        import time
        for i in range(10):
            ele.send_keys(Keys.BACKSPACE)
        ele.send_keys(data_info)
        ele.send_keys(Keys.ENTER)
        time.sleep(1)

    #读写输入框的value值
    @classmethod
    def input_value(cls,driver):
        driver.execute_script("document.getElementById('selectStuLeave').style.display='block';")
    # 添加cookie信息
    @classmethod
    def add_cookie(cls,driver,url,path):
        # cookie信息
        cookie_data = Utility.read_json(path)
        for cookie_info in cookie_data:
            driver.add_cookie(cookie_info)
        driver.get(url)

    # select框指定输入
    @classmethod
    def get_select_result(cls,ele,data):
        Select(ele).select_by_visible_text(data)


    # 用select元素定位下级option
    @classmethod
    def get_select_option(cls,ele,ele_num):
        ele.find_element_by_xpath("//select[@name='cus.last_status']/option[%s]"%ele_num).click()

    # 一定范围随机取出一个下拉框元素
    @classmethod
    def get_select_random(cls, ele):
        content_options = Select(ele).options
        # 随机数
        Select(ele).select_by_index(randint(0, len(content_options) - 1))

if __name__ == '__main__':
    pass
