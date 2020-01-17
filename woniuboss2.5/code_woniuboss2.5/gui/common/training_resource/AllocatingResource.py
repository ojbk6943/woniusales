from selenium.webdriver.common.by import By
from gui.util.Service import Service


class AllocatingResource:

    # 用户信息输入框
    @classmethod
    def allocating_resource_query(cls,driver,data):
        input_ele = Service.get_ele(driver, By.CSS_SELECTOR,
                        "#content > div.row.con-margin.con-body-header > "
                        "div.col-lg-3.col-md-3.col-xs-3.con-body-padding > input[type=text]")
        Service.input_value_ele(input_ele,data)



    # 渠道下拉框
    @classmethod
    def allocating_resource_source(cls,driver,data):
        source_select_ele = Service.get_ele(driver, By.CSS_SELECTOR,
                        " #content > div.row.con-margin.con-body-header > "
                        "div.col-lg-2.col-md-2.col-xs-2.con-body-padding > select")
        Service.get_select_result(source_select_ele,data)

    # 分配简历下拉框、提交
    @classmethod
    def allocating_resource_resume(cls,driver,data):
        resume_select_ele = Service.get_ele(driver,By.ID,"empNameSelect")
        Service.get_select_result(resume_select_ele, data)

        Service.get_ele(driver, By.ID, "Submit").click()

    # 按比例分配
    @classmethod
    def allocating_resource_ratio_resume(cls,driver,data):
        Service.get_ele(driver, By.CSS_SELECTOR,
                        "#content > div.row.con-margin.con-body-header > "
                        "div.col-lg-7.col-md-7.col-xs-7.con-body-padding.text-right > button:nth-child(3)").click()
        ratio_resume_count = Service.get_eles(driver,By.CSS_SELECTOR,"#proportion_num tr")

        # 层级关系找下级元素个数
        if len(ratio_resume_count) > 0:

            # 大于1个咨询师
            if len(ratio_resume_count) > 1:
                # 选则第一个,输入指定比例
                first_ratio_resume = Service.get_tier_ele(ratio_resume_count,By.XPATH,
                                                        "//table[@id='proportion-table']/tbody/tr[1]/td[3]/input")
                Service.input_value_ele(first_ratio_resume,data["firstcounselor"])

                # 选择最后一个，输入指定比例
                css_select_path = "#proportion_num > tr:nth-of-type(%d) > td:nth-child(3) > " \
                                  "input[type=text]"%len(ratio_resume_count)
                last_ratio_resume = Service.get_tier_ele(ratio_resume_count, By.CSS_SELECTOR,css_select_path)
                Service.input_value_ele(last_ratio_resume, data["lastcounselor"])
            # 只有一个咨询师
            else:
                # 选则第一个,输入指定比例
                first_ratio_resume = Service.get_tier_ele(ratio_resume_count, By.XPATH,
                                                          "//table[@id='proportion-table']/tbody/tr[1]/td[3]/input")
                Service.input_value_ele(first_ratio_resume, data["firstcounselor"])

            # 完成比例分配，点击提交,再点击确定
            Service.get_ele(driver,By.ID,"proportion_submit").click()
            Service.get_ele(driver,By.CSS_SELECTOR,
                            "body > div.bootbox.modal.fade.mydialog.in > div > div > "
                            "div.modal-footer > button.btn.btn-primary").click()
        else:
            print("系统分配人员出错")

    # 查询操作
    @classmethod
    def allocating_resource_query_operation(cls,driver,query_operation_info):
        AllocatingResource.allocating_resource_source(driver,query_operation_info["source"])
        AllocatingResource.allocating_resource_query(driver, query_operation_info["userinfo"])
        # 点击查询
        Service.get_ele(driver, By.CSS_SELECTOR, ".col-lg-3 > button:nth-child(2)").click()
    # 提交 操作
    @classmethod
    def allocating_resource_submit_operation(cls,driver,submit_operation_info):

        # 手动提交
        if submit_operation_info["submitway"] == "0":
            AllocatingResource.allocating_resource_resume(driver, submit_operation_info["empNameSelect"])
        # 按比例提交
        else:
            AllocatingResource.allocating_resource_ratio_resume(driver,submit_operation_info)