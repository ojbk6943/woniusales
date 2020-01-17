


from selenium.webdriver.common.by import By

from gui.util.Service import Service


'''学员管理 子模块 阶段测评'''
class StagedEvaluation:

    # 班级 元素
    @classmethod
    def staged_class_ele(cls, driver, data):
        class_select_ele = Service.get_ele(
            driver, By.CSS_SELECTOR, "#examination > "
                                     "div.col-lg-8.col-md-8.col-sm-12.col-xs-12.con-body-padding.text-left > "
                                     "select.sel-text.stu-class")
        Service.get_select_result(class_select_ele, data)

    # 方向 元素
    @classmethod
    def staged_direction_ele(cls, driver, data):
        direction_select_ele = Service.get_ele(
            driver, By.CSS_SELECTOR, "#examination > "
                                     "div.col-lg-8.col-md-8.col-sm-12.col-xs-12.con-body-padding.text-left > "
                                     "select.sel-text.stu-orientation")
        Service.get_select_result(direction_select_ele, data)

    # 姓名输入框 元素
    @classmethod
    def staged_name_input(cls, driver, data):
        name_input_query_ele = Service.get_ele(
            driver, By.CSS_SELECTOR, "#examination > "
                                     "div.col-lg-8.col-md-8.col-sm-12.col-xs-12.con-body-padding.text-left > "
                                     "input[type=text]")
        Service.input_value_ele(name_input_query_ele, data)

    # 查询操作
    @classmethod
    def staged_evaluation_query(cls, driver, query_info):
        StagedEvaluation.staged_class_ele(driver, query_info["class"])
        StagedEvaluation.staged_direction_ele(driver, query_info["direction"])
        StagedEvaluation.staged_name_input(driver, query_info["name"])

        # 查询按钮 元素
        Service.get_ele(
            driver, By.CSS_SELECTOR, "#examination > "
                                     "div.col-lg-8.col-md-8.col-sm-12.col-xs-12.con-body-padding.text-left > button"
        ).click()

    # 测评操作
    @classmethod
    def staged_evaluation_staged(cls, driver, staged_ifo):
        # 点击测评按钮
        Service.get_ele(
            driver, By.CSS_SELECTOR, "#exam-table > tbody > tr > td:nth-child(6) > button:nth-child(1)").click()
        # 阶段下拉框 元素
        stage_ele = Service.get_ele(
            driver, By.CSS_SELECTOR, "#score-form > div > div:nth-child(2) > div:nth-child(1) > select")
        Service.get_select_result(stage_ele, staged_ifo["stage"])
        # 成绩输入框 元素
        score_ele = Service.get_ele(
            driver, By.CSS_SELECTOR, "#score-form > div > div:nth-child(2) > div:nth-child(2) > input")
        Service.input_value_ele(score_ele, staged_ifo["score"])

        # 评语输入框 元素
        comment_ele = Service.get_ele(
            driver, By.CSS_SELECTOR, "#score-form > div > div.col-md-12.col-sm-12.col-xs-12.form-group > textarea")
        Service.input_value_ele(comment_ele, staged_ifo["comment"])

        # 保存
        Service.get_ele(driver, By.ID, "saveStageBtn").click()

