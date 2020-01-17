from gui.util.Service import Service


class Marketing:

    # 查询功能 area,status,starttime,endtime
    @classmethod
    def marketing_query(cls,driver,marketing_query_info):
        # 找到select元素:区域、状态、来源
        # 区域
        select_area_ele = Service.get_ele_location_method(
            driver, "css", "#queryDiv > div:nth-child(1) > span:nth-child(1) > select")
        Service.get_select_result(select_area_ele, marketing_query_info['area'])

        # 状态
        select_status_ele = Service.get_ele_location_method(
            driver, "css", "#queryDiv > div:nth-child(1) > span:nth-child(2) > select")
        Service.get_select_result(select_status_ele, marketing_query_info['status'])

        # 来源
        select_source_ele = Service.get_ele_location_method(
            driver, "css", "#queryDiv > div:nth-child(1) > span:nth-child(3) > select")
        Service.get_select_result(select_source_ele, marketing_query_info['source'])

        # 开始时间
        starttime_ele = Service.get_ele_location_method(
            driver, "css", "#queryDiv > div:nth-child(2) > input:nth-child(2)")
        Service.input_value_ele(starttime_ele, marketing_query_info['starttime'])

        # 结束时间
        endtime_ele = Service.get_ele_location_method(
            driver, "css", "#queryDiv > div:nth-child(2) > input:nth-child(4)")
        Service.input_value_ele(endtime_ele, marketing_query_info['endtime'])

        # 姓名
        name_ele = Service.get_ele_location_method(
            driver, "css", "#queryDiv > div:nth-child(2) > input[type=text]:nth-child(5)")
        Service.get_input(name_ele, marketing_query_info['name'])

        # 点击查询
        marketing_query_ele = Service.get_ele_location_method(
            driver, "css", "#queryDiv > div:nth-child(2) > button.btn.btn-padding.btn-info.btn-search")
        marketing_query_ele.click()

    # 新增功能
    @classmethod
    def marketing_add(cls, driver, marketing_add_info):
        # 区域
        select_area_ele = Service.get_ele_location_method(
            driver, "css", "#addResource-form > div > div > div:nth-child(1) > select")
        Service.get_select_result(select_area_ele, marketing_add_info['area'])

        # 部门
        select_department_ele = Service.get_ele_location_method(
            driver, "css", "#addResource-form > div > div > div:nth-child(2) > select")
        Service.get_select_result(select_department_ele, marketing_add_info['department'])

        # 电话
        phone_ele = Service.get_ele_location_method(
            driver, "css", "#addResource-form > div > div > div:nth-child(3) > input")
        Service.input_value_ele(phone_ele, marketing_add_info['phone'])

        # 姓名
        name_ele = Service.get_ele_location_method(
            driver, "css", "#addResource-form > div > div > div:nth-child(4) > input")
        Service.input_value_ele(name_ele, marketing_add_info['name'])

        # QQ
        qq_ele = Service.get_ele_location_method(
            driver, "css", "#addResource-form > div > div > div:nth-child(8) > input")
        Service.input_value_ele(qq_ele, marketing_add_info['qq'])

        # 学历
        select_education_ele = Service.get_ele_location_method(
            driver, "css", "#addResource-form > div > div > div:nth-child(10) > select")
        Service.get_select_result(select_education_ele, marketing_add_info['education'])

        # 最后跟踪
        tracking_ele = Service.get_ele_location_method(
            driver, "css", "#addResource-form > div > div > div.col-md-12.col-sm-12.form-group > textarea")
        Service.input_value_ele(tracking_ele, marketing_add_info['tracking'])

        # 点击保存
        Service.get_ele_location_method(driver, "id", "addCusBtn").click()

