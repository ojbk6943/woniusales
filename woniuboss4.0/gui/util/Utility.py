import json
import pymysql
from selenium.webdriver.support.select import Select


class Utility:

    # 连接数据库
    @classmethod
    def get_connect(cls,path):
        # 读取配置文件
        con_data = Utility.read_json(path)
        return pymysql.connect(
            con_data["HOST"],con_data["USER"],con_data["PASSWORD"],con_data["DATABASE"],charset="utf8")
    # 单条查询
    @classmethod
    def get_connect_one(cls,sql,path):
        con = Utility.get_connect(path)
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchone()

    # 多条查询
    @classmethod
    def get_connect_all(cls, sql,path):
        con = Utility.get_connect(path)
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()

    # 增删改
    @classmethod
    def increases_deletion(cls,sql,path):
        con = Utility.get_connect(path)
        cur = con.cursor()
        cur.execute(sql)
        # 更新数据库
        con.commit()
        return True

    # 读取json类型数据
    @classmethod
    def read_json(cls,path):
        with open(path,encoding='utf-8') as file:
            return json.load(file)

    # 读取excell表中的用例数据
    @classmethod
    def read_excell(cls,path):
        import xlrd
        with open(path) as file:
            return xlrd.open_workbook(path)

    # select选择框的随机输入
    @classmethod
    def get_select(cls, ele, data):
        select_count = ele.options
        return Select(ele).select_by_index(Utility.get_random(0, select_count - 1))

    # 随机数获取
    @classmethod
    def get_random(cls, start, end):
        from random import randint
        return randint(start, end)


if __name__ == '__main__':
    pass