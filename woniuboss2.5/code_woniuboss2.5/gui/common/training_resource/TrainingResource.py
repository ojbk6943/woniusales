from selenium.webdriver.common.by import By
from gui.util.Service import Service



class TrainingResource:

    # 资源库 下拉框
    @classmethod
    def resource_library_select(cls,driver,data):
        resource_library_select_ele = Service.get_ele(driver,By.ID,"poolSelect")
        Service.get_select_result(resource_library_select_ele,data)

    # 咨询师 下拉框
    @classmethod
    def counselo_selectr(cls, driver, data):
        counselo_selectr_ele = Service.get_ele(driver, By.ID, "empNameSelect")
        Service.get_select_result(counselo_selectr_ele, data)

    # 状态
    @classmethod
    def status_select(cls, driver, data):
        status_select_ele = Service.get_ele(driver, By.ID, "statusSelect")
        Service.get_select_result(status_select_ele, data)

    # 来源
    @classmethod
    def source_select(cls, driver, data):
        source_select_ele = Service.get_ele(driver, By.ID, "sourceSelect")
        Service.get_select_result(source_select_ele, data)

    # 分配时间（开始，结束） date1  date2
    @classmethod
    def data_input(cls,driver,start_data,end_data):

        start_data_input_ele = Service.get_ele(driver, By.ID, "date1")
        Service.input_value_ele(start_data_input_ele,start_data)

        end_data_input_ele = Service.get_ele(driver, By.ID, "date2")
        Service.input_value_ele(end_data_input_ele, end_data)

    # 电话
    @classmethod
    def phone_input(cls, driver, phone_data):
        phone_input_ele = Service.get_ele(driver, By.NAME, "cusInfo")
        Service.input_value_ele(phone_input_ele, phone_data)

    # 搜索
    @classmethod
    def query_button(cls, driver):
        Service.get_ele(driver, By.XPATH, '//button[@class="btn btn-padding"]').click()

    # 培训资源
    @classmethod
    def training_resource(cls,driver,training_resource_info):
        # 查询条件
        TrainingResource.resource_library_select(driver,training_resource_info['poolSelect'])
        TrainingResource.counselo_selectr(driver, training_resource_info['empNameSelect'])
        TrainingResource.status_select(driver, training_resource_info['statusSelect'])
        TrainingResource.source_select(driver, training_resource_info['sourceSelect'])
        TrainingResource.data_input(driver, training_resource_info['date1'],training_resource_info['date2'])
        TrainingResource.phone_input(driver, training_resource_info['cusInfo'])
        # 点击搜索
        TrainingResource.query_button(driver)
