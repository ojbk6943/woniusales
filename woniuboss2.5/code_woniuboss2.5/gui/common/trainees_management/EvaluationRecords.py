from selenium.webdriver.common.by import By

from gui.util.Service import Service


'''学员管理 子模块 测评记录'''
class EvaluationRecords:

    # 班级下拉框 元素
    @classmethod
    def records_class_ele(cls, driver, data):
        class_select_ele = Service.get_ele(
            driver, By.CSS_SELECTOR, "#stagetest > "
                                     "div.col-lg-12.col-md-12.col-sm-12.col-xs-12.con-body-padding.text-left > "
                                     "select.sel-text.stu-class")
        Service.get_select_result(class_select_ele, data)

    # 方向下拉框 元素
    @classmethod
    def records_direction_ele(cls, driver, data):
        direction_select_ele = Service.get_ele(
            driver, By.CSS_SELECTOR, "#stagetest > "
                                     "div.col-lg-12.col-md-12.col-sm-12.col-xs-12.con-body-padding.text-left > "
                                     "select.sel-text.stu-orientation")
        Service.get_select_result(direction_select_ele, data)

    # 阶段下拉框 元素
    @classmethod
    def records_stage_ele(cls, driver, data):
        stage_select_ele = Service.get_ele(
            driver, By.CSS_SELECTOR, "#stagetest > "
                                     "div.col-lg-12.col-md-12.col-sm-12.col-xs-12.con-body-padding.text-left > "
                                     "select.sel-text.stu-phase")
        Service.get_select_result(stage_select_ele, data)

    # 姓名输入框 元素
    @classmethod
    def records_name_input(cls, driver, data):
        name_input_query_ele = Service.get_ele(
            driver, By.CSS_SELECTOR, "#stagetest > "
                                     "div.col-lg-12.col-md-12.col-sm-12.col-xs-12.con-body-padding.text-left > "
                                     "input[type=text]")
        Service.input_value_ele(name_input_query_ele, data)

    # 查询操作
    @classmethod
    def staged_evaluation_query(cls, driver, query_info):
        EvaluationRecords.records_class_ele(driver, query_info["class"])
        EvaluationRecords.records_direction_ele(driver, query_info["direction"])
        EvaluationRecords.records_stage_ele(driver, query_info["stage"])
        EvaluationRecords.records_name_input(driver, query_info["name"])

        # 查询按钮 元素
        Service.get_ele(
            driver, By.CSS_SELECTOR,
            "#stagetest > div.col-lg-12.col-md-12.col-sm-12.col-xs-12.con-body-padding.text-left > button"
        ).click()
