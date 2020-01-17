from selenium.webdriver.common.by import By
from gui.util.Service import Service


class PersonnelManagement:

    '''员工信息'''
    @classmethod
    def Person_second_directory_employee_info(cls, driver):
        Service.get_ele(driver, By.LINK_TEXT, "员工信息").click()

    # 地区  region
    @classmethod
    def Person_region(cls, driver, data):
        region_selector_ele = Service.get_ele(driver, By.ID, "regionSel")
        Service.get_select_result(region_selector_ele, data)

    # 部门  department
    @classmethod
    def Person_department(cls, driver, data):
        department_selector_ele = Service.get_ele_location_method(
            driver, "css", "#content > div.row.con-margin.con-body-con > "
                                     "div.col-lg-12.col-md-12.col-xs-12.con-body-padding.text-left > "
                                     "select.sel-text.dept")
        Service.get_select_result(department_selector_ele, data)

    # 状态  status
    @classmethod
    def Person_status(cls, driver, data):
        status_selector_ele = Service.get_ele(
            driver, By.CSS_SELECTOR, "#content > div.row.con-margin.con-body-con > "
                                     "div.col-lg-12.col-md-12.col-xs-12.con-body-padding.text-left > "
                                     "select.emp_status.sel-text")
        Service.get_select_result(status_selector_ele, data)

    # 姓名输入框
    @classmethod
    def Person_name(cls, driver, data):
        name_input_ele = Service.get_ele(
            driver, By.CSS_SELECTOR, "#content > div.row.con-margin.con-body-con > "
                                     "div.col-lg-12.col-md-12.col-xs-12.con-body-padding.text-left > "
                                     "input[type=text]")
        Service.input_value_ele(name_input_ele, data)

    # 查询按钮
    @classmethod
    def Person_query_button(cls, driver):
        Service.get_ele(
            driver, By.CSS_SELECTOR, "#content > div.row.con-margin.con-body-con > "
                                     "div.col-lg-12.col-md-12.col-xs-12.con-body-padding.text-left > "
                                     "button.btn.btn-info.btn-padding").click()
    # 查询操作
    @classmethod
    def query_employee(cls, driver, query_info):
        PersonnelManagement.Person_second_directory_employee_info(driver)
        PersonnelManagement.Person_region(driver, query_info["region"])
        PersonnelManagement.Person_department(driver, query_info["department"])
        PersonnelManagement.Person_status(driver, query_info["status"])
        PersonnelManagement.Person_name(driver, query_info["name"])
        # 按钮
        PersonnelManagement.Person_query_button(driver)

    # 新增操作
    @classmethod
    def add_employee(cls, driver, add_info):
        PersonnelManagement.Person_second_directory_employee_info(driver)
        # 新增按钮
        Service.get_ele_location_method(
            driver, "xpath", "//*[@id='content']/div[2]/div[1]/div/button").click()
        # 区域 region
        add_region_select_ele = Service.get_ele_location_method(
            driver, "css", "#addEmp-form > div > div:nth-child(1) > div:nth-child(1) > select")

        Service.get_select_result(add_region_select_ele, add_info["region"])

        # 部门 department
        add_department_select_ele = Service.get_ele_location_method(
            driver, "css", "#addEmp-form > div > div:nth-child(1) > div:nth-child(2) > select")
        Service.get_select_result(add_department_select_ele, add_info["department"])

        # 职位 job
        add_job_input_ele = Service.get_ele_location_method(
            driver, "css", "#addEmp-form > div > div:nth-child(1) > div:nth-child(3) > input")
        Service.input_value_ele(add_job_input_ele, add_info["job"])

        # 姓名 name
        add_name_input_ele = Service.get_ele_location_method(
            driver, "css", "#addEmp-form > div > div:nth-child(2) > div:nth-child(1) > input")
        Service.input_value_ele(add_name_input_ele, add_info["name"])

        # 性别 sex
        add_sex_input_ele = Service.get_ele_location_method(
            driver, "css", "#addEmp-form > div > div:nth-child(2) > div:nth-child(2) > select")
        Service.get_select_result(add_sex_input_ele, add_info["sex"])

        # 入职日期 date
        Service.get_ele_location_method(
            driver, "css", "#addEmp-form > div > div:nth-child(2) > div:nth-child(3) > input").click()

        Service.get_ele_location_method(
            driver, "css",
            "body > div:nth-child(22) > div.datetimepicker-days > table > tbody > tr:nth-child(2) > td:nth-child(1)").click()
        # Service.input_value_ele(add_date_input_ele, add_info["date"])

        # 电话 phone
        add_phone_input_ele = Service.get_ele_location_method(
            driver, "css", "#addEmp-form > div > div:nth-child(3) > div:nth-child(1) > input")

        Service.input_value_ele(add_phone_input_ele, add_info["phone"])

        # 工号 job_number
        add_job_number_input_ele = Service.get_ele_location_method(
            driver, "css", "#addEmp-form > div > div:nth-child(8) > div > input")
        Service.input_value_ele(add_job_number_input_ele, add_info["job_number"])

        # 点击保存
        Service.get_ele_location_method(driver, "css", "#addEmpBtn").click()

        # 确定
        Service.get_ele_location_method(
            driver, "css", "body > div.bootbox.modal.fade.mydialog.in > div > div > div.modal-footer > button").click()


    # 修改员工信息
    @classmethod
    def modify_employee(cls, driver):
        name_ele = Service.get_ele_location_method(
            driver, "css", "#modifyEmp-form > div > div:nth-child(2) > div:nth-child(1) > input")
        Service.input_value_date_ele(name_ele, Service.format_date())
        # 保存
        Service.get_ele_location_method(driver, "css", "#modifyEmpBtn").click()