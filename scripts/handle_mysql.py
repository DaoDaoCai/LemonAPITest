# -*- coding: UTF-8 -*-
# file: handle_mysql_1.py
# author:Administrator
# Time: 2019/11/18 17:16
# software: PyCharm


import random
import pymysql

from scripts.handle_yaml import do_yaml

class HandleMysql():
    def __init__(self):
        # 1.建立连接
        self.conn = pymysql.connect(host=do_yaml.read_yaml('mysql','host'),  # mysql服务器ip或域名
                                    user=do_yaml.read_yaml('mysql','user'),  # 用户名
                                    password=do_yaml.read_yaml('mysql','password'),  # 密码
                                    db=do_yaml.read_yaml('mysql','db'),  # 要连接的数据库名
                                    port=do_yaml.read_yaml('mysql','port'),  # 数据库端口号，默认3306
                                    charset='utf8',  # 数据库编码为utf8，不能写为utf-8
                                    # 默认返回的结果为元组或者嵌套元组的列表
                                    #可以指定cursorclass为DictCursor，那么返回的结果为字典或者嵌套字典的列表
                                    cursorclass=pymysql.cursors.DictCursor
                                    )

        # 2.创建游标对象
        self.cursor = self.conn.cursor()

    # def get_value(self,sql,args=None):
    #     self.cursor.execute(sql,args)
    #     self.conn.commit()
    #     return self.cursor.fetchone()
    #
    # def get_values(self,sql,args=None):
    #     self.cursor.execute(sql,args)
    #     self.conn.commit()
    #     return self.cursor.fetchall()

    def run(self, sql, args=None, is_more=False):
        self.cursor.execute(sql, args)
        self.conn.commit()
        if is_more:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.conn.close()


    @staticmethod
    def create_mobile():
        """
        随机生成11位手机号
        :return:
        """
        return '188'+''.join(random.sample('0123456789',8))

    def is_existed_mobile(self,mobile):
        """
        判断手机号是否被注册
        :param mobile:
        :return:
        """
        sql = do_yaml.read_yaml('mysql','select_user_sql')
        if self.run(sql,args=[mobile]):
            return True
        else:
            return False
    def create_not_existed_mobile(self):
        """
        随机生成一个数据库中不存在的手机号
        :return:
        """
        while True:
            one_mobile = self.create_mobile()
            if not self.is_existed_mobile(one_mobile):
                break
        return one_mobile






if __name__ == '__main__':
    # 当封装好一个类之后，要在下面自测一下
    # sql_1 = "select * from member where mobile_phone = '13888888889';"
    # sql_2 = "select * from member limit 0,10;"
    #
    do_mysql = HandleMysql()
    # print(do_mysql.run(sql_1))
    # print(do_mysql.run(sql_2, is_more=True))
    print(do_mysql.create_not_existed_mobile())

    do_mysql.close()
