import unittest
from interface.case.login_test.LoginTest import LoginTest
from interface.case.resource_management_test.AllotResourceTest import AllotResourceTest
from interface.case.resource_management_test.DeliverResourceTest import DeliverResourceTest
from interface.case.resource_management_test.PublicResourceTest import PublicResourceTest
from interface.case.resource_management_test.TrainResourceTest import TraineesManagementTest
from interface.config.HTMLTestRunnerCN import HTMLTestRunner


class Driven:
    def run_case(self):
        # 测试套
        suite = unittest.TestSuite()
        # 加载器
        loader = unittest.TestLoader()

        # 登录
        suite.addTests(loader.loadTestsFromTestCase(LoginTest))

        # 资源管理
        suite.addTests(loader.loadTestsFromTestCase(PublicResourceTest))
        suite.addTests(loader.loadTestsFromTestCase(TraineesManagementTest))
        suite.addTests(loader.loadTestsFromTestCase(DeliverResourceTest))
        suite.addTests(loader.loadTestsFromTestCase(AllotResourceTest))

        # 加载运行器
        with open('C:/Users/wang/Desktop/woniuboss4.0/interface/log/result.html',
                  'w',encoding='utf-8') as file:

            runner = HTMLTestRunner(stream=file, verbosity=2, title='log')
            runner.run(suite)
            # runner = unittest.TextTestRunner(verbosity=2)
            # runner.run(suite)


if __name__ == '__main__':
    Driven().run_case()









