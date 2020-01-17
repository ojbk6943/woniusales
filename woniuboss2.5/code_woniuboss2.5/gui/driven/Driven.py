
import unittest

from gui.case.login_test.LoginTest import LoginTest
from gui.case.marketing_test.MarketingTest import MarketingTest
from gui.case.trainees_management_test.ClassManagementTest import ClassManagementTest
from gui.case.trainees_management_test.CourseArrangementTest import CourseArrangementTest
from gui.case.trainees_management_test.EvaluationRecordsTest import Evaluation_Records_Test
from gui.case.trainees_management_test.StagedEvaluationTest import StagedEvaluationTest
from gui.case.trainees_management_test.StudentsVacateTest import StudentsVacateTest
from gui.case.trainees_management_test.TodayAttendanceTest import TodayAttendanceTest
from gui.case.trainees_management_test.TodayMorningExamTest import TodayMorningExamTest
from gui.case.trainees_management_test.TraineesManagementTest import TraineesManagementTest
from gui.case.training_resource_test.AllocatingResourceTest import AllocatingResourceTest
from gui.case.training_resource_test.CommonResourcePoolTest import CommonResourcePoolTest
from gui.case.training_resource_test.TrainingResourceTest import TrainingResourceTest
from gui.case.training_resource_test.TransfereeTest import TransfereeTest
from gui.config.HTMLTestRunnerCN import HTMLTestRunner


class Driven:
    def run_case(self):
        # 测试套
        suite = unittest.TestSuite()
        # 加载器
        loader = unittest.TestLoader()

        suite.addTests(loader.loadTestsFromTestCase(LoginTest))
        suite.addTests(loader.loadTestsFromTestCase(MarketingTest))

        # 培训资源
        suite.addTests(loader.loadTestsFromTestCase(AllocatingResourceTest))
        suite.addTests(loader.loadTestsFromTestCase(CommonResourcePoolTest))
        suite.addTests(loader.loadTestsFromTestCase(TrainingResourceTest))
        suite.addTests(loader.loadTestsFromTestCase(TransfereeTest))


        # 学员管理
        suite.addTests(loader.loadTestsFromTestCase(TraineesManagementTest))
        suite.addTests(loader.loadTestsFromTestCase(CourseArrangementTest))
        suite.addTests(loader.loadTestsFromTestCase(ClassManagementTest))
        suite.addTests(loader.loadTestsFromTestCase(TodayAttendanceTest))
        suite.addTests(loader.loadTestsFromTestCase(TodayMorningExamTest))
        suite.addTests(loader.loadTestsFromTestCase(StudentsVacateTest))
        suite.addTests(loader.loadTestsFromTestCase(StagedEvaluationTest))
        suite.addTests(loader.loadTestsFromTestCase(Evaluation_Records_Test))


        # 加载运行器
        with open('result.html','w',encoding='utf-8') as file:

            runner = HTMLTestRunner(stream=file,verbosity=2,title='flag')
            runner.run(suite)
        # runner = unittest.TextTestRunner(verbosity=2)
        # runner.run(suite)


if __name__ == '__main__':
    Driven().run_case()









