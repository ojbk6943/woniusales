import re
import time
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

    # 登录
    @classmethod
    def get_login(cls, session, path, role_data):
        roles = Service.get_role_info(path, role_data)
        # 登录
        Service.post_arguments(session, roles[0], roles[1])

    # 解密
    @classmethod
    def get_decode(cls, session, *param):
        decode_info = Service.get_excell_info(*param)[0]
        # 解密
        return Service.post_arguments(session, decode_info["url"], decode_info["step"])

    # 读取表格的用例信息([{},{}])
    @classmethod
    def get_excell_info(cls, path, sheet_name, *clos):
        # 读取表格
        book = Utility.read_excell(path)
        # 得到具体工作表
        sheet_target_name = book.sheet_by_name(sheet_name)
        # 定义 返回的列表
        test_case_list_directory = []

        # 遍历读取
        for i in range(1, sheet_target_name.nrows):
            # 空字典
            clos_dict = {}
            # 具体列
            url_clos = sheet_target_name.cell(i, clos[0]).value
            param_clos = sheet_target_name.cell(i, clos[1]).value
            value_clos_expect = sheet_target_name.cell(i, clos[2]).value.strip()

            # 添加网址
            clos_dict["url"] = url_clos

            if param_clos != "无参数":
                value_clos_datas = param_clos.splitlines()
                step_dict = {}
                for clos_data in value_clos_datas:
                    # 排除空行
                    if clos_data:
                        # 切割，用"="
                        data_split = clos_data.split("=")
                        # = 左边为键，右边为值
                        step_dict[data_split[0].strip()] = data_split[1].strip()

                # 添加参数
                clos_dict["step"] = step_dict

            # 添加预期
            clos_dict["expect"] = value_clos_expect

            # 添加列表
            test_case_list_directory.append(clos_dict)
        return test_case_list_directory


    # 读取表格的用例信息(parameterized)
    @classmethod
    def get_excell_data(cls, path, sheet_name, type_name,  *clos):
        # 读取表格
        book = Utility.read_excell(path)
        # 得到具体工作表
        sheet_target_name = book.sheet_by_name(sheet_name)
        # 定义 返回的列表
        test_case_list_directory = []

        # 遍历读取
        for i in range(1, sheet_target_name.nrows):
            type_clos = sheet_target_name.cell(i, 0).value
            if type_name in type_clos:
                # 空字典
                test_case_list = []
                clos_dict = {}
                # 具体列
                url_clos = sheet_target_name.cell(i, clos[0]).value
                param_clos = sheet_target_name.cell(i, clos[1]).value
                value_clos_expect = sheet_target_name.cell(i, clos[2]).value.strip()

                # 添加网址
                clos_dict["url"] = url_clos

                if param_clos != "无参数":
                    value_clos_datas = param_clos.splitlines()
                    step_dict = {}
                    for clos_data in value_clos_datas:
                        # 排除空行
                        if clos_data:
                            # 切割，用"="
                            data_split = clos_data.split("=")
                            # = 左边为键，右边为值
                            step_dict[data_split[0].strip()] = data_split[1].strip()

                    # 添加参数
                    clos_dict["step"] = step_dict

                # 添加预期
                clos_dict["expect"] = value_clos_expect

                # 添加列表
                test_case_list.append(clos_dict)
                test_case_list_directory.append(test_case_list)

        return test_case_list_directory

    # 读取角色表信息
    @classmethod
    def get_role_info(cls, path, role_data):
        # 读表格
        book = Utility.read_excell(path)
        role_sheet = book.sheet_by_name("roles")
        user_info = {}
        user_list = []
        # 遍历每一行
        for i in range(1, role_sheet.nrows):
            # 读取 角色   判断账号
            role_info = role_sheet.cell(i, 1).value.strip()
            # 找到要找的角色
            if role_data in role_info:
                # 读取账号、密码
                url = role_sheet.cell(i, 3).value
                user_datas = role_sheet.cell(i, 4).value.splitlines()
                for data in user_datas:
                    # “=”切割
                    param = data.split("=")
                    user_info[param[0].strip()] = param[1].strip()

                user_list.append(url)
                user_list.append(user_info)

                return user_list
        else:
            return None

    # sql查询  培训资源  allot_resource
    @classmethod
    def training_resource_query_sql(cls, query_info, path):

        base_sql = "select count(customer_id) from customer where pool_type!='public'"

        if query_info["poolType"] != "全部" and query_info["poolType"] != "":
            base_sql = "select count(customer_id) from customer where pool_type='%s'"%(query_info["poolType"])

        if query_info["lastStatus"] != "全部" and query_info["lastStatus"] != "":
            status_sql = "select dict_key from dictionary_data where dict_type_id=1 and dict_value='%s'" % (
                query_info["lastStatus"])
            last_status = Utility.get_connect_one(status_sql, path)[0]

            base_sql = base_sql + " and last_status='%s'" % (last_status)

        if query_info["source"] != "全部" and query_info["source"] != "":
            source_sql = "select dict_key from dictionary_data where dict_type_id=4 and dict_value='%s'" % (
                query_info["source"])
            source = Utility.get_connect_one(source_sql, path)[0]
            base_sql = base_sql + " and source='%s'" % (source)

        if query_info["s_time"] != "" and query_info["e_time"] != "":
            base_sql = base_sql + \
                       " and create_time between '%s' and '%s'" % (
                       query_info["s_time"], query_info["e_time"])

        elif query_info["s_time"] == "" and query_info["e_time"] != "":

            base_sql = base_sql + \
                       " and create_time before '%s'" % (query_info["e_time"])


        elif query_info["s_time"] != "" and query_info["e_time"] == "":

            base_sql = base_sql + \
                       " and create_time after '%s'" % (query_info["s_time"])
        # 咨询师
        if query_info["workId"] != "全部" and  query_info["workId"] != "":

            consult_sql = "select work_id from employee where employee_name='%s';"%(query_info["workId"])
            consult = Utility.get_connect_one(consult_sql, path)[0]
            base_sql = base_sql + " and work_id='%s'" % (consult)

        if query_info["cusInfo"] != "" and query_info["cusInfo"] == "一瓢":
            info = "1A5EF59031E0FDEB"

            base_sql = base_sql + " and name='%s'" % (info)

        return Utility.get_connect_one(base_sql + ";", path)[0]

    # sql查询  分配资源  allot_resource
    @classmethod
    def allot_resource_query_sql(cls, query_info, path):

        base_sql = "select count(customer_id) from customer where work_id='0' and allot_time =''"

        if query_info["source"] != "全部" and query_info["source"] != "":
            source_sql = "select dict_key from dictionary_data where dict_type_id=4 and dict_value='%s'" % (
                query_info["source"])
            source = Utility.get_connect_one(source_sql, path)[0]
            base_sql = base_sql + " and source='%s'" % (source)

        if query_info["info"] != "" and query_info["info"] == "软件小达人":
            info = "BF4051071EFC93BE29B8A46D5F3C97CD"
            base_sql = base_sql + " and name='%s'" % (info)

        return Utility.get_connect_one(base_sql + ";", path)[0]

    # sql查询 公共资源 public_resource
    @classmethod
    def query_public_resource_query_sql(cls, query_info, path):
        base_sql = "select count(customer_id) from customer where pool_type='public'"

        # 地区
        if query_info["regionId"] != "全部" and query_info["regionId"] != "":
            base_sql = base_sql + " and region_id='%s'" %(query_info["regionId"])

        # 部门
        if query_info["deptId"] != "全部" and query_info["deptId"] != "":
            base_sql = base_sql + " and department_id=%d"%(query_info["deptId"])

        # 最后废弃人(从老师到废弃表中查询，自己废弃的记录，再来匹配，public状态的)
        if query_info["workId"] != "全部" and query_info["workId"] != "":
            customer_sql = "select customer_id from abandon_record where work_id='%s';" %(query_info["workId"])
            customer_id = Utility.get_connect_one(customer_sql, path)[0]
            base_sql = base_sql + " and work_id in '%s'" % (customer_id)

        # 状态 lastStatus
        if query_info["lastStatus"] != "全部" and query_info["lastStatus"] != "":
            base_sql = base_sql + " and last_status='%s'" % (query_info["lastStatus"])
        # 来源
        if query_info["source"] != "全部" and query_info["source"] != "":
            base_sql = base_sql + " and source='%s'" %(query_info["source"])

        # 学历
        if query_info["education"] != "全部" and query_info["education"] != "":
            base_sql = base_sql + " and education='%s'" % (query_info["education"])
        # 姓名
        if query_info["cusInfo"] != "" and query_info["cusInfo"] == "小红旗":
            info = "30DEFFB90BC0E5B38AF9118A5E8B2309"
            base_sql = base_sql + " and name='%s'" % (info)

        return Utility.get_connect_one(base_sql + ";", path)[0]

    # sql查询 （转交资源 ）query_deliver_resource_query_sql
    @classmethod
    def query_deliver_resource_query_sql(cls, query_info, path):

        base_sql = "select count(customer_id) from customer where true"

        # 地区
        if query_info["region"] != "全部" and query_info["region"] != "":
            base_sql = base_sql + " and region_id='%s'" % (query_info["region"])

        # 部门
        if query_info["deptId"] != "全部" and query_info["deptId"] != "":
            base_sql = base_sql + " and department_id='%s'" % (query_info["deptId"])

        # 最后废弃人(从老师到废弃表中查询，自己废弃的记录，再来匹配，public状态的)
        if query_info["workId"] != "全部" and query_info["workId"] != "":
            customer_sql = "select customer_id from abandon_record where work_id='%s';" % (query_info["workId"])
            customer_id = Utility.get_connect_one(customer_sql, path)[0]
            base_sql = base_sql + " and work_id in '%s'" % (customer_id)

        # 状态 lastStatus
        if query_info["status"] != "全部" and query_info["status"] != "":
            base_sql = base_sql + " and last_status='%s'" % (query_info["status"])
        # 来源
        if query_info["source"] != "全部" and query_info["source"] != "":
            base_sql = base_sql + " and source='%s'" % (query_info["source"])

        # 姓名
        if query_info["cusInfo"] != "" and query_info["cusInfo"] == "小红旗":
            info = "30DEFFB90BC0E5B38AF9118A5E8B2309"
            base_sql = base_sql + " and name='%s'" % (info)

        return Utility.get_connect_one(base_sql + ";", path)[0]

    # sql查询 提交 转交资源 update_deliver_resource_query_sql
    @classmethod
    def update_deliver_resource_query_sql(cls, query_info, path):

        base_sql = "select count(customer_id) from customer where true"

        # 地区
        if query_info["regionId"] != "全部" and query_info["regionId"] != "":
            base_sql = base_sql + " and region_id='%s'" % (query_info["regionId"])

        # 部门
        if query_info["deptId"] != "全部" and query_info["deptId"] != "":
            base_sql = base_sql + " and department_id='%s'" % (query_info["deptId"])
        # 咨询师
        if query_info["workId"] != "全部" and query_info["workId"] != "":
            base_sql = base_sql + " and work_id='%s'" %(query_info["workId"])

        return Utility.get_connect_one(base_sql + ";", path)[0]

if __name__ == '__main__':
    pass
