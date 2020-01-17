import re
import time
from random import randint
from interface.util.Utility import Utility


class Service:

    # 格式化日期
    @classmethod
    def format_date(cls):
        return time.strftime('%Y-%m-%d',time.localtime())

    # 登录
    @classmethod
    def login(cls,session, login_url, login_info):
        session.post(login_url, login_info)
    # 解密
    @classmethod
    def decode(cls, session, decode_url, decode_info):
        session.post(decode_url, decode_info)

    # 培训资源，判断输入用户信息，为：电话号码、qq、名字
    @classmethod
    def judge_cusInfo(cls, cusInfo):
        # 数字一组
        if cusInfo.isdigit():
            # 手机号
            if re.match('^1[3456789]\d{9}$', cusInfo):
                return 1
            # qq号
            else:
                return 2
        # 名字
        else:
            return 3

    # 响应方法对应传参数与否

    # 无参get请求
    @classmethod
    def get_no_arguments(cls, session, url):
        return session.get(url)

    # 有参get请求
    @classmethod
    def get_arguments(cls, session, url, info):
        return session.get(url, info)

    # 无参POST请求
    @classmethod
    def post_no_arguments(cls, session, url):
        return session.post(url)

    # 有参get请求
    @classmethod
    def post_arguments(cls, session, url, info):
        return session.post(url, info)

    # 登录、解密
    @classmethod
    def get_login_decode(cls, base_url, session, login_path, decode_path):
        # 登录
        login_data = Utility.read_json(login_path)
        login_url = base_url + login_data[0][0]["login_url"]
        Service.login(session, login_url, login_data[0][1])
        # 解密
        decode_data = Utility.read_json(decode_path)
        decode_url = base_url + decode_data[0][0]["decode_url"]
        Service.decode(session, decode_url, decode_data[0][1])

    # 培训资源 查询培训资源 sql
    # poolType empName lastStatus source  s_time e_time  cusInfo
    # 正交实验
    # 1111111  1112222  1221122     1222211     2121212   2122121   2211221   2212112

    # 对应操作，返回对应sql
    @classmethod
    def sql_query_training_resource(cls, query_info, path):
        base_sql = Utility.read_json(path)
        # 1111111
        if query_info["poolType"] == "" and query_info["empName"] == "" and query_info["lastStatus"] == "" and \
                        query_info["source"] == "" and query_info["s_time"] == "" and query_info["e_time"] == "" and \
                query_info["cusInfo"] == "" :
            return base_sql["1"]
        # 1112222
        elif query_info["poolType"] == "" and query_info["empName"] == "" and query_info["lastStatus"] == "" and \
            query_info["source"] != "" and query_info["s_time"] != "" and query_info["e_time"] != "" and \
                query_info["cusInfo"] != "" :
            return base_sql["2"]%(query_info["source"], query_info["cusInfo"], query_info["s_time"], query_info["e_time"])

        # 1221122
        elif query_info["poolType"] == "" and query_info["empName"] != "" and query_info["lastStatus"] != "" and \
            query_info["source"] == "" and query_info["s_time"] == "" and query_info["e_time"] != "" and \
                query_info["cusInfo"] != "" :

            # 判断用户信息 类别
            condition = Service.judge_cusInfo(query_info["cusInfo"])
            empName_work_id = Utility.get_connect_one(
                "select work_id from employee where employee_name='%s'" % (query_info["empName"]),
                '../../config/data_base')

            if condition == 1:
                return base_sql["3"][0]%(empName_work_id, query_info["lastStatus"], empName_work_id, query_info["e_time"])
            elif condition == 2:
                return base_sql["3"][1]%(empName_work_id, query_info["lastStatus"], empName_work_id, query_info["e_time"])
            elif condition == 3:
                return base_sql["3"][2]%(empName_work_id, query_info["lastStatus"], empName_work_id, query_info["e_time"])
        # 1222211
        elif query_info["poolType"] == "" and query_info["empName"] != "" and query_info["lastStatus"] != "" and \
            query_info["source"] != "" and query_info["s_time"] != "" and query_info["e_time"] == "" and \
                query_info["cusInfo"] == "" :
            empName_work_id = Utility.get_connect_one(
                "select work_id from employee where employee_name='%s'" % (query_info["empName"]),
                '../../config/data_base')
            return base_sql["4"]%(empName_work_id, query_info["lastStatus"], query_info["source"], query_info["s_time"])

        # 2121212
        elif query_info["poolType"] != "" and query_info["empName"] == "" and query_info["lastStatus"] != "" and \
                query_info["source"] == "" and query_info["s_time"] != "" and query_info["e_time"] == "" and \
                query_info["cusInfo"] != "":
            condition = Service.judge_cusInfo(query_info["cusInfo"])
            if condition == 1:
                return base_sql["5"][0]%(query_info["poolType"], query_info["lastStatus"], query_info["cusInfo"], query_info["s_time"])
            elif condition == 2:
                return base_sql["5"][1]%(query_info["poolType"], query_info["lastStatus"], query_info["cusInfo"], query_info["s_time"])
            elif condition == 3:
                return base_sql["5"][2]%(query_info["poolType"], query_info["lastStatus"], query_info["cusInfo"], query_info["s_time"])

        # 2122121
        elif query_info["poolType"] != "" and query_info["empName"] == "" and query_info["lastStatus"] != "" and \
                query_info["source"] != "" and query_info["s_time"] == "" and query_info["e_time"] != "" and \
                query_info["cusInfo"] == "":
            return  base_sql["6"]% (query_info["poolType"], query_info["lastStatus"], query_info["source"], query_info["e_time"])

        # 2211221
        elif query_info["poolType"] != "" and query_info["empName"] != "" and query_info["lastStatus"] == "" and \
                query_info["source"] == "" and query_info["s_time"] != "" and query_info["e_time"] != "" and \
                query_info["cusInfo"] == "":
            empName_work_id = Utility.get_connect_one(
                "select work_id from employee where employee_name='%s'" % (query_info["empName"]),
                '../../config/data_base')
            return base_sql["7"]% (query_info["poolType"], empName_work_id, query_info["s_time"], query_info["e_time"])

        # 2212112
        elif query_info["poolType"] != "" and query_info["empName"] != "" and query_info["lastStatus"] == "" and \
                query_info["source"] != "" and query_info["s_time"] == "" and query_info["e_time"] == "" and \
                query_info["cusInfo"] != "":
            condition = Service.judge_cusInfo(query_info["cusInfo"])
            empName_work_id = Utility.get_connect_one(
                "select work_id from employee where employee_name='%s'" % (query_info["empName"]),
                '../../config/data_base')
            if condition == 1:
                return base_sql["8"][0]% (query_info["poolType"], empName_work_id, query_info["source"], query_info["cusInfo"])
            elif condition == 2:
                return base_sql["8"][1]% (query_info["poolType"], empName_work_id, query_info["source"], query_info["cusInfo"])
            elif condition == 3:
                return base_sql["8"][2]% (query_info["poolType"], empName_work_id, query_info["source"], query_info["cusInfo"])

    # 培训资源 查询培训资源 sql
    # poolType empName lastStatus source  s_time e_time  cusInfo
    # 正交实验
    # 0000  0011 0101 0110  1001  1010  1100  1111

    # 对应操作，返回对应sql      "workId":"WNCD011","region":"成都","source":"网络","status":"新入库"
    @classmethod
    def sql_query_trans_feree(cls, query_info, path):
        base_sql = Utility.read_json(path)
        # 0000
        if query_info["workId"] == "" and query_info["region"] == "" and query_info["source"] == "" and \
                query_info["status"] == "" :
            return base_sql["1"]
            #   "select count(customer_id) from customer;"
        # 0011
        elif query_info["workId"] == "" and query_info["region"] == "" and query_info["source"] != "" and \
                query_info["status"] != "" :
            return base_sql["2"]%(query_info["source"], query_info["status"])
            # "select count(customer_id) from customer where source='%s' and last_status='%s';"%(query_info["source"], query_info["status"])
        # 0101
        elif query_info["workId"] == "" and query_info["region"] != "" and query_info["source"] == "" and \
                query_info["status"] != "" :
            return base_sql["3"]%(query_info["region"], query_info["status"])
            # "select count(customer_id) from customer where region='%s' and last_status='%s';"%(query_info["region"], query_info["status"])

        # 0110
        elif query_info["workId"] == "" and query_info["region"] != "" and query_info["source"] != "" and \
             query_info["status"] == "":
            return base_sql["4"]%(query_info["region"], query_info["source"])
            # "select count(customer_id) from customer where region='%s' and source='%s';"%(query_info["region"], query_info["source"])

        # 1001
        elif query_info["workId"] != "" and query_info["region"] == "" and query_info["source"] == "" and \
             query_info["status"] != "":
            return base_sql["5"]%(query_info["workId"], query_info["status"])
            # "select count(customer_id) from customer where work_id='%s' and status='%s';"%(empName_work_id, query_info["status"])

        # 1010
        elif query_info["workId"] != "" and query_info["region"] == "" and query_info["source"] != "" and \
             query_info["status"] == "":
            return base_sql["6"]%(query_info["workId"], query_info["source"])
            # "select count(customer_id) from customer where work_id='%s' and source='%s';"%(empName_work_id, query_info["source"])

        # 1100
        elif query_info["workId"] != "" and query_info["region"] != "" and query_info["source"] == "" and \
             query_info["status"] == "":
            return base_sql["7"]%(query_info["workId"], query_info["region"])
        # "select count(customer_id) from customer where work_id='%s' and region='%s';"%(empName_work_id, query_info["region"])

        # 1111
        elif query_info["workId"] != "" and query_info["region"] != "" and query_info["source"] != "" and \
             query_info["status"] != "":
            return base_sql["8"]%(query_info["workId"], query_info["region"], query_info["source"], query_info["status"])
            # "select count(customer_id) from customer where work_id='%s' and region='%s' and source='%s' and last_status='%s';"%(empName_work_id, query_info["region"], query_info["source"], query_info["status"])


    # 培训资源 分配资源 sql
    @classmethod
    def sql_query_allocating_resource(cls, query_info, path):
        base_sql = Utility.read_json(path)
        # "source": "专属", "info": ""
        # 00
        if query_info["source"] == "" and query_info["region"] == "":
            return base_sql["1"]
        # 01
        elif query_info["source"] == "" and query_info["region"] != "":
            condition = Service.judge_cusInfo(query_info["info"])
            if condition == 1:
                return base_sql["201"][0] % (query_info["info"])
            elif condition == 2:
                return base_sql["202"][0] % (query_info["info"])
            elif condition == 3:
                return base_sql["203"][0] % (query_info["info"])
        # 10
        elif query_info["source"] != "" and query_info["region"] == "":
            return base_sql["3"]

        # 11
        elif query_info["source"] != "" and query_info["region"] != "":
            condition = Service.judge_cusInfo(query_info["info"])
            if condition == 1:
                return base_sql["401"][0] % (query_info["source"], query_info["info"])
            elif condition == 2:
                return base_sql["402"][0] % (query_info["source"], query_info["info"])
            elif condition == 3:
                return base_sql["403"][0] % (query_info["source"], query_info["info"])

    # 000 011 101 110

    # 公共资源池  sql
    @classmethod
    def sql_query_common_resource_pool(cls, query_info, path):
        base_sql = Utility.read_json(path)
        # 000
        if query_info["workId"] == "全部" and query_info["lastStatus"] == "全部" and query_info["source"] == "全部":
            return base_sql["1"]
        # 011
        elif query_info["workId"] == "全部" and query_info["lastStatus"] != "" and query_info["source"] != "":
            return base_sql["2"]%(query_info["lastStatus"], query_info["source"])
        # 101
        elif query_info["workId"] != "全部" and query_info["lastStatus"] == "" and query_info["source"] != "全部":
            return base_sql["3"]%(query_info["workId"], query_info["source"])
        # 110
        elif query_info["workId"] != "全部" and query_info["lastStatus"] != "全部" and query_info["source"] == "":
            return base_sql["4"]%(query_info["workId"], query_info["lastStatus"])


    # @classmethod
    # def sql_query(cls, query_info, path):
    #
    #     # 1111111
    #     if query_info["poolType"] == "" and query_info["empName"] == "" and query_info["lastStatus"] == "" and \
    #         query_info["source"] == "" and query_info["s_time"] == "" and query_info["e_time"] == "" and \
    #             query_info["cusInfo"] == "" :
    #         return None
    #     # 1112222
    #     elif query_info["poolType"] == "" and query_info["empName"] == "" and query_info["lastStatus"] == "" and \
    #         query_info["source"] != "" and query_info["s_time"] != "" and query_info["e_time"] != "" and \
    #             query_info["cusInfo"] != "" :
    #         return "select count(customer_id),tel from customer where pool_type != 'public' and source='%s' and name='%s'" \
    #                "and allot_time between '%s' and '%s' "%(query_info["source"], query_info["cusInfo"], query_info["s_time"], query_info["e_time"])
    #     # 1221122
    #     elif query_info["poolType"] == "" and query_info["empName"] != "" and query_info["lastStatus"] != "" and \
    #         query_info["source"] == "" and query_info["s_time"] == "" and query_info["e_time"] != "" and \
    #             query_info["cusInfo"] != "" :
    #
    #         # 判断用户信息 类别
    #         condition = Service.judge_cusInfo(query_info["cusInfo"])
    #         empName_work_id = Utility.get_connect_one(
    #             "select work_id from employee where employee_name='%s'" % (query_info["empName"]),
    #             '../../config/data_base')
    #
    #         if condition == 1:
    #             return "select count(customer_id),tel from customer where pool_type != 'public' and work_id = '%s' and last_status='%s' and tel='%s'" \
    #                    "and allot_time before '%s' "%(empName_work_id, query_info["lastStatus"], empName_work_id, query_info["e_time"])
    #         elif condition == 2:
    #             return "select count(customer_id),tel from customer where pool_type != 'public' and work_id = '%s' and last_status='%s' and qq='%s'" \
    #                    "and allot_time before '%s' "%(empName_work_id, query_info["lastStatus"], empName_work_id, query_info["e_time"])
    #         elif condition == 3:
    #             return "select count(customer_id),tel from customer where pool_type != 'public' and work_id = '%s' and last_status='%s' and name='%s'" \
    #                    "and allot_time before '%s' "%(empName_work_id, query_info["lastStatus"], empName_work_id, query_info["e_time"])
    #     # 1222211
    #     elif query_info["poolType"] == "" and query_info["empName"] != "" and query_info["lastStatus"] != "" and \
    #         query_info["source"] != "" and query_info["s_time"] != "" and query_info["e_time"] == "" and \
    #             query_info["cusInfo"] == "" :
    #         empName_work_id = Utility.get_connect_one(
    #             "select work_id from employee where employee_name='%s'" % (query_info["empName"]),
    #             '../../config/data_base')
    #         return "select count(customer_id),tel from customer where pool_type != 'public' and work_id = '%s' and lastStatus='%s' and source = '%s'" \
    #                "and allot_time after '%s'  "%(empName_work_id, query_info["lastStatus"], query_info["source"], query_info["s_time"])
    #     # 2121212
    #     elif query_info["poolType"] != "" and query_info["empName"] == "" and query_info["lastStatus"] != "" and \
    #             query_info["source"] == "" and query_info["s_time"] != "" and query_info["e_time"] == "" and \
    #             query_info["cusInfo"] != "":
    #         condition = Service.judge_cusInfo(query_info["cusInfo"])
    #         if condition == 1:
    #             return "select count(customer_id),tel from customer where poolType = '%s' and last_status='%s' and tel='%s'" \
    #                    "and allot_time before '%s' "%(query_info["poolType"], query_info["lastStatus"], query_info["cusInfo"], query_info["s_time"])
    #         elif condition == 2:
    #             return "select count(customer_id),tel from customer where poolType = '%s' and last_status='%s' and qq='%s'" \
    #                    "and allot_time before '%s' "%(query_info["poolType"], query_info["lastStatus"], query_info["cusInfo"], query_info["s_time"])
    #         elif condition == 3:
    #             return "select count(customer_id),tel from customer where poolType = '%s' and last_status='%s' and name='%s'" \
    #                    "and allot_time before '%s' "%(query_info["poolType"], query_info["lastStatus"], query_info["cusInfo"], query_info["s_time"])
    #     # 2122121
    #     elif query_info["poolType"] != "" and query_info["empName"] == "" and query_info["lastStatus"] != "" and \
    #             query_info["source"] != "" and query_info["s_time"] == "" and query_info["e_time"] != "" and \
    #             query_info["cusInfo"] == "":
    #         return "select count(customer_id),tel from customer where poolType = '%s' and lastStatus='%s' and source = '%s'" \
    #                "and allot_time before '%s'  " % (query_info["poolType"], query_info["lastStatus"], query_info["source"], query_info["e_time"])
    #
    #     # 2211221
    #     elif query_info["poolType"] != "" and query_info["empName"] != "" and query_info["lastStatus"] == "" and \
    #             query_info["source"] == "" and query_info["s_time"] != "" and query_info["e_time"] != "" and \
    #             query_info["cusInfo"] == "":
    #         empName_work_id = Utility.get_connect_one(
    #             "select work_id from employee where employee_name='%s'" % (query_info["empName"]),
    #             '../../config/data_base')
    #         return "select count(customer_id),tel from customer where poolType = '%s' and work_id='%s'" \
    #                "and allot_time between '%s' and '%s'  " % (query_info["poolType"], empName_work_id, query_info["s_time"], query_info["e_time"])
    #
    #     # 2212112
    #     elif query_info["poolType"] != "" and query_info["empName"] != "" and query_info["lastStatus"] == "" and \
    #             query_info["source"] != "" and query_info["s_time"] == "" and query_info["e_time"] == "" and \
    #             query_info["cusInfo"] != "":
    #         condition = Service.judge_cusInfo(query_info["cusInfo"])
    #         empName_work_id = Utility.get_connect_one(
    #             "select work_id from employee where employee_name='%s'" % (query_info["empName"]),
    #             '../../config/data_base')
    #         if condition == 1:
    #             return "select count(customer_id),tel from customer where poolType = '%s' and work_id='%s' and source='%s'" \
    #                    "and tel='%s' " % (
    #                    query_info["poolType"], empName_work_id, query_info["source"], query_info["cusInfo"])
    #         elif condition == 2:
    #             return "select count(customer_id),tel from customer where poolType = '%s' and work_id='%s' and source='%s'" \
    #                    "and qq='%s' " % (
    #                    query_info["poolType"], empName_work_id, query_info["source"], query_info["cusInfo"])
    #         elif condition == 3:
    #             return "select count(customer_id),tel from customer where poolType = '%s' and work_id='%s' and source='%s'" \
    #                    "and name='%s' " % (
    #                    query_info["poolType"], empName_work_id, query_info["source"], query_info["cusInfo"])

if __name__ == '__main__':
    pass
