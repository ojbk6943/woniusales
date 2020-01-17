import unittest
import re
from parameterized import parameterized
from selenium import webdriver
from selenium.webdriver.common.by import By

from gui.common.training_resource.TrainingResource import TrainingResource
from gui.util.Service import Service
from gui.util.Utility import Utility

training_resource_data = Utility.read_json("../test_data/training_resource/training_resource_data")

class TrainingResourceTest(unittest.TestCase):

    # 自定义，初始化driver，窗口最大化，隐式等待
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.url = Utility.read_json("../config/data_base")["BASEURL"]
        self.driver.get(self.url)

    # 添加cookie
    def training_resource_init(self):
        # 添加cookie信息，跳转到登陆后首页
        Service.add_cookie(self.driver, self.url, "../config/data_cookie")
        # 培训资源
        Service.get_ele(self.driver, By.PARTIAL_LINK_TEXT, "培训资源").click()


    @parameterized.expand(training_resource_data)
    def test_training_resource(self,training_resource_info,expect):

        # 获取sql
        def joint_sql():
            time_base_sql = ' and create_time between "%s" and "%s" and type="下载"' % (
                training_resource_info['date1'], training_resource_info['date2'])
            if training_resource_info['poolSelect']=="全部" and training_resource_info['empNameSelect']=="全部" and\
                training_resource_info['statusSelect']=="全部" and training_resource_info['sourceSelect']=="全部" and\
                    training_resource_info['date1']=="" and training_resource_info['date2']!="":
                sql = 'select count(customer_id) from customer where pool_type != "public"' + time_base_sql
                return sql

            if training_resource_info['poolSelect']=="全部" and training_resource_info['empNameSelect']=="全部" and\
                training_resource_info['statusSelect']=="全部" and training_resource_info['sourceSelect']!="全部":

                sql = 'select count(customer_id) from customer where source = "%s" and pool_type != "public"'\
                      %training_resource_info['sourceSelect']+time_base_sql
                return sql

            elif training_resource_info['poolSelect']!="全部" and training_resource_info['empNameSelect']=="全部" and\
                training_resource_info['statusSelect']=="全部" and training_resource_info['sourceSelect']!="全部":

                sql = 'select count(customer_id) from customer where source = "%s" and pool_type = "%s"' \
                      % (training_resource_info['sourceSelect'],training_resource_info['poolSelect'])+time_base_sql
                return sql

            elif training_resource_info['poolSelect']!="全部" and training_resource_info['empNameSelect']=="全部" and\
                training_resource_info['statusSelect']!="全部" and training_resource_info['sourceSelect']!="全部":

                sql = 'select count(customer_id) from customer where source = "%s" and pool_type = "%s" and last_status="%s"' \
                      % (training_resource_info['sourceSelect'],training_resource_info['poolSelect'],
                         training_resource_info['statusSelect'])+time_base_sql
                return sql
        # 获取cookie
        self.training_resource_init()
        # 选择加载资源模块
        Service.get_ele(self.driver,By.CSS_SELECTOR,
                        "#content > div.row.con-margin.con-body-header > div:nth-child(1) > ul > li.active > a").click()
        TrainingResource.training_resource(self.driver,training_resource_info)

        # 系统提示搜索条件
        if Service.is_Element_present(
                self.driver, By.CSS_SELECTOR, "body > div.bootbox.modal.fade.mydialog.in > div > div > "
                                              "div.modal-footer > button"):
            actual = "query-fail"
            self.assertEqual(actual, expect)
            # 关闭
            self.driver.quit()
        else:
            # 判断是否查询出数据
            training_resource_query_result = Service.get_ele(self.driver, By.CSS_SELECTOR, "table#personal-table tbody").text
            # 市场营销有上传过数据
            if training_resource_query_result != "无符合条件的记录":
                # 前端页面显示数据数，根据状态（不同状态数量不同）
                query_count_result = Service.get_ele(self.driver, By.CSS_SELECTOR, "span.pagination-info").text
                result = re.match('^显示.*，总.*?(\d+)', query_count_result)
                print(result.group(1))
                sql = joint_sql()
                print(sql)
                if sql:
                    query_connect_count = Utility.get_connect_one(sql, "../config/data_base")
                    print(query_connect_count)
                    if int(result.group(1)) == int(query_connect_count[0]):
                        actual = 'query-pass'
                    else:
                        actual = 'query-fail'
                    self.assertEqual(actual, expect)

            else:
                print("查询结果为空")
            self.driver.close()
if __name__ == '__main__':
    unittest.main(verbosity=2)