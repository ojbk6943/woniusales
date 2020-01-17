from selenium.webdriver.common.by import By

from gui.util.Service import Service


class CommonResourcePool:

    # 最后废弃人 元素
    @classmethod
    def finally_abandoned_people(cls,driver,data):
        finally_abandoned_people_select_ele = \
            Service.get_ele(driver, By.CSS_SELECTOR,"#content > div.row.con-margin.con-body-header > "
                                                    "div.col-lg-6.col-md-6.col-xs-12.con-body-padding > "
                                                    "select:nth-child(1)")
        Service.get_select_result(finally_abandoned_people_select_ele, data)

    # 状态  元素
    @classmethod
    def common_resource_pool_status(cls, driver, data):
        pool_status_select_ele = Service.get_ele(driver,
                                            By.CSS_SELECTOR, "#content > div.row.con-margin.con-body-header > "
                                                             "div.col-lg-6.col-md-6.col-xs-12.con-body-padding > "
                                                             "select:nth-child(2)")
        Service.get_select_result(pool_status_select_ele, data)

    # 来源  元素
    @classmethod
    def common_resource_pool_source(cls, driver, data):
        pool_source_select_ele = Service.get_ele(driver,
                                                 By.CSS_SELECTOR, "#content > div.row.con-margin.con-body-header > "
                                                                  "div.col-lg-6.col-md-6.col-xs-12.con-body-padding > "
                                                                  "select:nth-child(3)")
        Service.get_select_result(pool_source_select_ele, data)

    # 查询输入框 元素
    @classmethod
    def common_resource_pool_input_query(cls, driver, data):
        input_query_ele = Service.get_ele(driver, By.CSS_SELECTOR,
                                    "#content > div.row.con-margin.con-body-header > "
                                    "div:nth-child(3) > input[type=text]")
        Service.input_value_ele(input_query_ele, data)


    # 查询操作 包括：最后废弃人、状态、来源、查询输入框
    @classmethod
    def common_resource_pool_query(cls,driver,query_info):
        # 元素
        CommonResourcePool.finally_abandoned_people(driver,query_info["people"])
        CommonResourcePool.common_resource_pool_status(driver,query_info["status"])
        CommonResourcePool.common_resource_pool_source(driver,query_info["source"])
        CommonResourcePool.common_resource_pool_input_query(driver,query_info["userinfo"])

        # 点击查询
        Service.get_ele(driver,By.CSS_SELECTOR,"button.btn:nth-child(2)").click()

    # 认领 操作 包括：找到认领元素，点击
    @classmethod
    def common_resource_pool_claim(cls,driver):
        # 点击认领
        Service.get_ele(driver, By.ID, "ownCusBtn").click()
