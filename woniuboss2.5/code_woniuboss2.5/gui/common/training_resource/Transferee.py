from selenium.webdriver.common.by import By
from gui.util.Service import Service


class Transferee:

    # 电话、姓名、qq
    @classmethod
    def cusInfo(cls,driver,data):
        cusInfo_ele = Service.get_ele(driver,By.NAME,"cusInfo")
        Service.input_value_ele(cusInfo_ele,data)

    # 查询 按钮
    @classmethod
    def query(cls,driver):
        Service.get_ele(driver,
                        By.CSS_SELECTOR,"#content > div.row.con-margin.con-body-header > "
                                        "div.col-lg-12.col-md-12.col-xs-12.con-body-padding > button").click()

    # 咨询师 下拉框
    @classmethod
    def empname_select1(cls, driver, data):
        empname_select1_ele = Service.get_ele(driver, By.ID, "empNameSelect1")
        Service.get_select_result(empname_select1_ele, data)

    # 区域
    @classmethod
    def region_select1(cls,driver, data):
        region_select1_ele = Service.get_ele(driver, By.ID, "regionSelect1")
        Service.get_select_result(region_select1_ele, data)

    # 状态
    @classmethod
    def status_select1(cls, driver, data):
        status_select1_ele = Service.get_ele(driver, By.NAME, "last_status")
        Service.get_select_result(status_select1_ele, data)

    # 来源
    @classmethod
    def source_select1(cls, driver, data):
        source_select1_ele = Service.get_ele(driver, By.XPATH, '//select[@name="source"]')
        Service.get_select_result(source_select1_ele, data)

    # 提交人
    @classmethod
    def empname_select2(cls,driver,data):
        region_select2_ele = Service.get_ele(driver, By.ID, "empNameSelect2")
        Service.get_select_result(region_select2_ele, data)

    # 区域
    @classmethod
    def region_select2(cls,driver,data):
        region_select2_ele = Service.get_ele(driver, By.ID, "regionSelect2")
        Service.get_select_result(region_select2_ele, data)

    # 提交
    @classmethod
    def submit(cls,driver):
        Service.get_ele(driver, By.ID, "Submit").click()

    # 按条件查询
    @classmethod
    def query_commit(cls,driver,query_commit_info):

        # 应填信息
        Transferee.cusInfo(driver,query_commit_info['cusInfo'])
        Transferee.empname_select1(driver,query_commit_info['empname'])
        Transferee.region_select1(driver,query_commit_info['region'])
        Transferee.status_select1(driver,query_commit_info['status'])
        Transferee.source_select1(driver,query_commit_info['source'])

        # 确定查询
        Transferee.query(driver)

    # 提交指定资源（单人，或全部）
    @classmethod
    def submit_commit(cls,driver,submit_commit_info):

        # 提交信息
        Transferee.empname_select2(driver,submit_commit_info["empnamesubmit"])
        Transferee.region_select2(driver,submit_commit_info["regionsubmit"])

        # 点击提交
        Transferee.submit(driver)





