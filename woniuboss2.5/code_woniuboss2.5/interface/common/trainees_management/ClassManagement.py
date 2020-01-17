
from selenium.webdriver.common.by import By

from gui.util.Service import Service



'''学员管理 子模块 班级管理'''
class ClassManagement:

    # 姓名 元素
    @classmethod
    def input_name(cls, driver, data):
        input_name_ele = Service.get_ele(
            driver, By.CSS_SELECTOR, "#cmDiv > div.col-lg-8.col-md-8.col-sm-12.col-xs-12.con-body-padding.text-left"
                                     " > input[type=text]")
        # 值
        Service.input_value_ele(input_name_ele, data)

    # 查询 按钮 元素
    @classmethod
    def button_query(cls,driver):
        Service.get_ele(
            driver, By.CSS_SELECTOR, "#cmDiv > div.col-lg-8.col-md-8.col-sm-12.col-xs-12.con-body-padding.text-left"
                                     " > button:nth-child(2)").click()
    # 分班班级 下拉框 元素
    @classmethod
    def class_name_select(cls,driver,data):
        class_name_select_ele = Service.get_ele(
            driver, By.CSS_SELECTOR, "#cmDiv > div.col-lg-8.col-md-8.col-sm-12.col-xs-12.con-body-padding.text-left"
                                     " > select.sel-text.stu-class")
        Service.get_select_result(class_name_select_ele,data)

    # 班级的方向 下拉框 元素
    @classmethod
    def class_direction_select(cls, driver, data):
        class_direction_select_ele = Service.get_ele(
            driver, By.CSS_SELECTOR, "#cmDiv > div.col-lg-8.col-md-8.col-sm-12.col-xs-12.con-body-padding.text-left"
                                     " > select.sel-text.stu-orientation")
        Service.get_select_result(class_direction_select_ele, data)

    # 确认 按钮 元素
    @classmethod
    def button_confirmation(cls, driver):
        Service.get_ele(
            driver, By.CSS_SELECTOR, "#cmDiv > div.col-lg-8.col-md-8.col-sm-12.col-xs-12.con-body-padding.text-left"
                                     " > button:nth-child(5)").click()

    # 查询学生 操作
    @classmethod
    def class_management_query(cls,driver,query_info):
        ClassManagement.input_name(driver,query_info["name"])
        ClassManagement.button_query(driver)

    # 分班确定 操作
    @classmethod
    def class_management_commit(cls, driver, commit_info):
        ClassManagement.class_name_select(driver, commit_info["classname"])
        ClassManagement.class_direction_select(driver, commit_info["classdirection"])
        # 确定
        ClassManagement.button_confirmation(driver)