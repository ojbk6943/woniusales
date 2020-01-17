import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from random import randint
from gui.util.Utility import Utility
from selenium import webdriver

class Service:

    # different broswer
    @classmethod
    def open_browser(cls, browser):
        if browser == "Firefox":
            return webdriver.Firefox()
        elif browser == "Chrome":
            return webdriver.Chrome()
        elif browser == "Ie":
            return webdriver.Ie()
        else:
            return None

    # different location method
    @classmethod
    def get_ele_location_method(cls,driver, locate_mode, msg):
        if locate_mode == "id":
            return driver.find_element(by=By.ID, value=msg)
        elif locate_mode == "name":
            return driver.find_element(by=By.NAME, value=msg)
        elif locate_mode == "tag_name":
            return driver.find_element(by=By.TAG_NAME, value=msg)
        elif locate_mode == "class_name":
            return driver.find_element(by=By.CLASS_NAME, value=msg)
        elif locate_mode == "css":
            return driver.find_element(by=By.CSS_SELECTOR, value=msg)
        elif locate_mode == "xpath":
            return driver.find_element(by=By.XPATH, value=msg)
        elif locate_mode == "link":
            return driver.find_element(by=By.LINK_TEXT, value=msg)
        elif locate_mode == "partial_link":
            return driver.find_element(by=By.PARTIAL_LINK_TEXT, value=msg)
        else:
            return None

    # different location method
    @classmethod
    def get_eles_location_method(cls, driver, locate_mode, msg):
        if locate_mode == "id":
            return driver.find_elements(by=By.ID, value=msg)
        elif locate_mode == "name":
            return driver.find_elements(by=By.NAME, value=msg)
        elif locate_mode == "tag_name":
            return driver.find_elements(by=By.TAG_NAME, value=msg)
        elif locate_mode == "class_name":
            return driver.find_elements(by=By.CLASS_NAME, value=msg)
        elif locate_mode == "css":
            return driver.find_elements(by=By.CSS_SELECTOR, value=msg)
        elif locate_mode == "xpath":
            return driver.find_elements(by=By.XPATH, value=msg)
        elif locate_mode == "link":
            return driver.find_elements(by=By.LINK_TEXT, value=msg)
        elif locate_mode == "partial_link":
            return driver.find_elements(by=By.PARTIAL_LINK_TEXT, value=msg)
        else:
            return None

    # 实例化driver    instantiation driver
    @classmethod
    def get_driver(cls, broswer="Firefox"):
        driver = Service.open_browser(broswer)
        driver.maximize_window()
        driver.implicitly_wait(10)
        return driver

    # Jump targets module
    @classmethod
    def jump_target_module(cls, driver, url_path, cookie_path, locate_mode, msg):
        url = Utility.read_json(url_path)["BASEURL"]
        driver.get(url)
        # add cookie info , jump target login page
        Service.add_cookie(driver, url, cookie_path)
        # click "msg" module
        Service.get_ele_location_method(driver, locate_mode, msg).click()

    # 解密 decode
    @classmethod
    def page_decode(cls, driver, config_path):

        # 得到decode信息
        config_info = Utility.read_json(config_path)

        # 解密
        Service.get_ele(driver, By.ID, "btn-decrypt").click()
        decode_input_ele = Service.get_ele(driver,
                                           By.CSS_SELECTOR, "#secondPass-modal > div > div > "
                                                            "div.modal-body.text-center > input[type=password]")
        Service.input_value_ele(decode_input_ele, config_info["DECODE"])
        # 点击确定
        Service.get_ele(driver, By.CSS_SELECTOR,
                        "#secondPass-modal > div > div > div.modal-footer > button").click()

    # search recode is not null
    @classmethod
    def search_recode_result(cls, driver, locate_mode, msg, result_locate_mode, result_msg):
        if Service.get_ele_location_method(driver, locate_mode, msg).text != "无符合条件的记录":
            # judge count 判断数量
            result_recode = Service.get_ele_location_method(driver, result_locate_mode, result_msg).text
            return re.match('.*，.*(\d+)',result_recode).group(1)
        else:
            return 0

    # 当前页员工信息条数
    @classmethod
    def current_page_person(cls, driver, locate_method, msg, body_id_msg):
        current_page_count = Service.get_eles_location_method(driver, locate_method, msg)
        if len(current_page_count) > 1:
            # 随机一个
            random_number = Utility.get_random(1, len(current_page_count))
            Service.get_ele_location_method(
                driver, 'css', "%s > tbody "
                               "> tr:nth-child(%d) > td:nth-child(9) > button"%(body_id_msg, random_number)).click()
        else:
            Service.get_ele_location_method(
                driver, 'css', "%s > tbody "
                               "> tr:nth-child(1) > td:nth-child(9) > button"%(body_id_msg)).click()
    # 修改  modify_person
    @classmethod
    def modify_person(cls, driver, query_count, page_id_msg, body_id_msg):
        # 翻页(有无页数)
        if int(query_count) > 10:
            page_count = Service.get_eles_location_method(
                driver, 'css', "%s > div.row.con-margin.con-body-con > div.bootstrap-table > "
                               "div.fixed-table-container > div.fixed-table-pagination > "
                               "div.pull-right.pagination > ul > li"%(page_id_msg))

            # 几页, 翻页到最后一页
            (Service.get_ele_location_method(
                driver, 'link', '%s')%(len(page_count)-2)).click()

            # 当前页员工信息个数
            Service.current_page_person(driver, 'css', "%s > tbody > tr"%(body_id_msg), body_id_msg)


        elif int(query_count) > 1:
            Service.current_page_person(driver, 'css', "%s > tbody > tr"%(body_id_msg), body_id_msg)
        elif int(query_count) > 0:
            Service.current_page_person(driver, 'css', "%s > tbody > tr"%(body_id_msg), body_id_msg)

    # element is(not) exist
    @classmethod
    def is_Element_present(cls,driver,how,what):
        from selenium.common.exceptions import NoSuchElementException
        try:
            return driver.find_element(by=how,value=what)
        except NoSuchElementException as e:
            return None

    # 寻找元素   find element
    @classmethod
    def get_ele(cls,driver,how,what):
        try:
            return driver.find_element(by=how,value=what)
        except:
            return None

    # 寻找复数元素  find elements
    @classmethod
    def get_eles(cls, driver, how, what):
        try:
            return driver.find_elements(by=how, value=what)
        except:
            return None

    # 层级关系寻找下级元素   tier find lower element
    @classmethod
    def get_tier_ele(cls,current_ele,how,what):
        try:
            return current_ele.find_element(by=how, value=what)
        except:
            return None

    # 格式化日期  format data
    @classmethod
    def format_date(cls):
        return time.strftime('%Y-%m-%d %H-%M-%S',time.localtime())

    # 输入类型元素，三步骤：点击、清空、输入值    input: click、clear、input_info
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
        if data:
            Select(ele).select_by_visible_text(data)
        else:
            pass
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

    # 读取角色表信息
    @classmethod
    def get_role_info(cls, path, role_data):
        # 读表格
        book = Utility.read_excell(path)
        role_sheet = book.sheet_by_name("roles")

        # 遍历每一行
        for i in range(1, role_sheet.nrows):
            # 读取 角色   判断账号
            role_info = role_sheet.cell(i, 1).value.strip()
            # 找到要找的角色
            if role_data in role_info:
                # 读取账号、密码
                role_user = role_sheet.cell(i, 3).value.strip()
                role_upass = role_sheet.cell(i, 4).value.strip()
                return role_user, role_upass
        else:
            return None

    # 读取表格的用例信息
    @classmethod
    def get_excell_data(cls, path, sheet_name, *clos):
        # 读取表格
        book = Utility.read_excell(path)
        # 得到具体工作表
        sheet_target_name = book.sheet_by_name(sheet_name)
        # 定义 返回的列表
        test_case_list_directory = []

        # 遍历读取
        for i in range(1, sheet_target_name.nrows):
            # 空字典
            test_case_list = []
            clos_dict = {}
            # 具体列
            value_clos_datas = sheet_target_name.cell(i, clos[0]).value.splitlines()
            value_clos_expect = sheet_target_name.cell(i, clos[1]).value.strip()
            for clos_data in value_clos_datas:
                # 切割，用"="
                data_split = clos_data.split("=")
                # = 左边为键，右边为值
                clos_dict[data_split[0].strip()] = data_split[1].strip()

            # 添加预期
            clos_dict["expect"] = value_clos_expect
            # 添加列表
            test_case_list.append(clos_dict)
            test_case_list_directory.append(test_case_list)
        return test_case_list_directory

    # 预期和实际不符合，截图
    @classmethod
    def get_screen(cls, driver, actual, expect, save_name, save_path):
        if actual != expect:
            file_name = save_name + Service.format_date() + '.png'
            driver.get_screenshot_as_file(save_path + file_name)

    # sql查询  市场营销  marketing
    @classmethod
    def marketing_query_sql(cls, query_info, path):

        base_sql = "select count(customer_id) from customer"
        flag = 0

        if query_info["area"] != "全部" and query_info["area"] != "":
            area_sql = "select region_id from region where region_name='%s'" % query_info["area"]
            area_id = Utility.get_connect_one(area_sql, path)[0]
            if flag:
                base_sql = base_sql + " and region_id=%d" % area_id
            else:
                base_sql = base_sql + " where region_id=%d" % area_id
                flag = 1

        if query_info["status"] != "全部" and query_info["status"] != "":
            status_sql = "select dict_key from dictionary_data where dict_type_id=1 and dict_value='%s'" % (
            query_info["status"])
            last_status = Utility.get_connect_one(status_sql, path)[0]
            if flag:
                base_sql = base_sql + " and last_status='%s'"%(last_status)
            else:
                base_sql = base_sql + " where last_status='%s'"%(last_status)
                flag = 1

        if query_info["source"] != "全部" and query_info["source"] != "":
            source_sql = "select dict_key from dictionary_data where dict_type_id=4 and dict_value='%s'"%(
                query_info["source"])
            source = Utility.get_connect_one(source_sql, path)[0]
            if flag:
                base_sql = base_sql + " and source='%s'"%(source)
            else:
                base_sql = base_sql + " where source='%s'"%(source)
                flag = 1
        if query_info["starttime"] != "" and query_info["endtime"] != "":
            if flag:
                base_sql = base_sql + \
                           " and create_time between '%s' and '%s'"%(query_info["starttime"], query_info["endtime"])
            else:
                base_sql = base_sql + \
                           " where create_time between '%s' and '%s'"%(query_info["starttime"], query_info["endtime"])
                flag = 1
        elif query_info["starttime"] == "" and query_info["endtime"] != "":
            if flag:
                base_sql = base_sql + \
                           " and create_time before '%s'"%(query_info["endtime"])
            else:
                base_sql = base_sql + \
                           " where create_time before '%s'"%(query_info["endtime"])
                flag = 1

        elif query_info["starttime"] != "" and query_info["endtime"] == "":
            if flag:
                base_sql = base_sql + \
                           " and create_time after '%s'"%(query_info["starttime"])
            else:
                base_sql = base_sql + \
                           " where create_time after '%s'"%(query_info["starttime"])
                flag = 1

        if query_info["name"] != "" and query_info["name"] == "一瓢":
            query_info["name"] = "1A5EF59031E0FDEB"
            if flag:
                base_sql = base_sql + " and name='%s'" % (query_info["name"] + "%")
            else:
                base_sql = base_sql + " where name='%s'" % (query_info["name"] + "%")
        return Utility.get_connect_one(base_sql + ";", path)[0]

    # sql 查询  人事管理   department
    @classmethod
    def person_query_sql(cls, query_info, path):

        base_sql = "select count(employee_id) from employee"
        flag = 0

        if query_info["region"] != "全部" and query_info["region"] != "":
            region_sql = "select region_id from region where region_name='%s'" %query_info["region"]
            region_id = Utility.get_connect_one(region_sql, path)[0]
            if flag:
                base_sql = base_sql + " and region_id=%d"%region_id
            else:
                base_sql = base_sql + " where region_id=%d"%region_id
                flag = 1

        if query_info["department"] != "全部" and query_info["department"] != "":
            department_sql = "select department_id from department where department_name='%s' and region_id=%d" %(query_info["department"],region_id)
            department_id = Utility.get_connect_one(department_sql, path)[0]
            if flag:
                base_sql = base_sql + " and department_id=%d"%department_id
            else:
                base_sql = base_sql + " where department_id=%d"%department_id
                flag = 1

        if query_info["status"] != "全部" and query_info["status"] != "":
            status_sql = "select dict_key from dictionary_data where dict_type_id=2 and dict_value='%s'" % (
            query_info["status"])
            status_id = Utility.get_connect_one(status_sql, path)[0]
            if flag:

                base_sql = base_sql + " and emp_status='%s'"%status_id
            else:
                base_sql = base_sql + " where emp_status='%s'"%status_id
                flag = 1
        if query_info["name"] != "":
            if flag:
                base_sql = base_sql + " and employee_name like '%s'"%(query_info["name"]+"%")
            else:
                base_sql = base_sql + " where employee_name like '%s'"%(query_info["name"]+"%")
        return Utility.get_connect_one(base_sql+";", path)[0]

    # sql查询  班级管理  class_manager
    @classmethod
    def class_manager_query_sql(cls, query_info, path):
        base_sql = "select count(class_id) from class"
        flag = 0
        if query_info["region"] != "全部" and query_info["region"] != "":
            region_sql = "select region_id from region where region_name='%s'" % query_info["region"]
            region_id = Utility.get_connect_one(region_sql, path)[0]
            if flag:
                base_sql = base_sql + " and region_id=%d" % region_id
            else:
                base_sql = base_sql + " where region_id=%d" % region_id
                flag = 1

        if query_info["class_status"] != "全部" and query_info["class_status"] != "":
            status_sql = "select dict_key from dictionary_data where dict_type_id=37 and dict_value='%s'" % (
                query_info["class_status"])
            status_id = Utility.get_connect_one(status_sql, path)[0]
            if flag:

                base_sql = base_sql + " and opening_status='%s'" % status_id
            else:
                base_sql = base_sql + " where opening_status='%s'" % status_id
                flag = 1

        return Utility.get_connect_one(base_sql + ";", path)[0]


    # sql查询  请假 students_leave
    @classmethod
    def students_vacate_query_sql(cls, query_info, path):
        base_sql = "select count(student_id) from student_leave"
        flag = 0
        if query_info["region"] != "全部" and query_info["region"] != "":
            region_table = "select count(s.student_id) from student_leave s " \
                         "inner join class c on s.class_id=c.class_id where " \
                         "c.region_id in (select region_id from region where region_name='%s')" \
                         % query_info["region"]
            base_sql = region_table
            flag = 1
        if query_info["status"] != "全部" and query_info["status"] != "":
            if flag:
                base_sql = base_sql + " and leave_status='%s'" %query_info["status"]
            else:
                base_sql = base_sql + " where leave_status='%s'" %query_info["status"]
                flag = 1

        if query_info["name"] != "":
            status_sql = "select student_id from student where student_name='%s'" % (
                query_info["name"])
            status_id = Utility.get_connect_one(status_sql, path)[0]

            if flag:
                base_sql = base_sql + " and student_id=%d" % (status_id)
            else:
                base_sql = base_sql + " where student_id=%d" % (status_id)
        return Utility.get_connect_one(base_sql + ";", path)[0]


if __name__ == '__main__':

    pass
