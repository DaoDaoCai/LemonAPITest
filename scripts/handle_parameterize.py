# -*- coding: UTF-8 -*-
# file: handle_parameterize.py
# author:Administrator
# Time: 2019/11/22 13:51
# software: PyCharm

import re

from scripts.handle_mysql import HandleMysql
from scripts.handle_yaml import HandleYaml
from scripts.handle_path import USER_ACCOUNTS_FILE_PATH

class Parameterize:
    """
    参数化类
    """
    # 不存在的数据相关正则表达式
    not_existed_id_pattern = r'{not_existed_id}'  # 不存在的id
    not_existed_tel_pattern = r'{not_existed_tel}' # 未注册的手机号
    not_existed_loan_id_pattern = r'{not_existed_loan_id}'  # 不存在的loan id

    # 投资人相关正则表达式
    invest_user_tel_pattern = r'{invest_user_tel}' # 投资人手机号
    invest_user_pwd_pattern = r'{invest_user_pwd}' # 投资人密码
    invest_user_id_pattern = r'{invest_user_id}'  # 投资人用户id

    # 借款人相关正则表达式
    borrow_user_id_pattern = r'{borrow_user_id}'  # 借款用户id
    borrow_user_tel_pattern = r'{borrow_user_tel}'  # 借款人手机号
    borrow_user_pwd_pattern = r'{borrow_user_pwd}'  # 借款人密码

    # 管理人相关正则表达式
    admin_user_tel_pattern = r'{admin_user_tel}'  # 管理人手机号
    admin_user_pwd_pattern = r'{admin_user_pwd}'  # 管理人密码

    # 其他相关正则表达式
    loan_id_pattern = r'{loan_id}'  # 标id

    do_user_account = HandleYaml(USER_ACCOUNTS_FILE_PATH)

    @classmethod
    def not_existed_replace(cls,data):
        do_mysql = HandleMysql()
        # 不存在手机号码替换
        # if re.search(cls.not_existed_tel_pattern,data):
        if cls.not_existed_tel_pattern in data:
            data = re.sub(cls.not_existed_tel_pattern, do_mysql.create_not_existed_mobile(), data)

        # 不存在的用户id替换
        if re.search(cls.not_existed_id_pattern, data):

            sql = "SELECT id FROM member ORDER BY id DESC LIMIT 0,1;"
            not_existed_id = do_mysql.run(sql).get('id') + 1  # 获取最大的用户id + 1
            data = re.sub(cls.not_existed_id_pattern, str(not_existed_id), data)

        # 不存在的load_id替换
        if cls.not_existed_loan_id_pattern in data:
            sql = "SELECT id FROM loan ORDER BY id DESC LIMIT 0, 1;"
            not_existed_load_id = do_mysql.run(sql).get('id') + 1  # 获取最大的用户id + 1
            data = re.sub(cls.not_existed_loan_id_pattern, str(not_existed_load_id), data)

        do_mysql.close()
        return data

    @classmethod
    def invest_user_replace(cls,data):
        # 投资人手机号替换
        if re.search(cls.invest_user_tel_pattern, data):
            invest_user_tel = cls.do_user_account.read_yaml("invest", "mobile_phone")
            data = re.sub(cls.invest_user_tel_pattern, invest_user_tel, data)

        # 投资人密码替换
        if re.search(cls.invest_user_pwd_pattern, data):
            invest_user_pwd = cls.do_user_account.read_yaml("invest", "pwd")
            data = re.sub(cls.invest_user_pwd_pattern, invest_user_pwd, data)

        if re.search(cls.invest_user_id_pattern, data):
            invest_user_id = cls.do_user_account.read_yaml('invest', 'id')
            # 投资人id为int类型, 要转化为str类型
            data = re.sub(cls.invest_user_id_pattern, str(invest_user_id), data)

        return data

    @classmethod
    def borrow_user_replace(cls,data):
        # 借款人id替换
        if re.search(cls.borrow_user_id_pattern, data):
            borrow_user_id = cls.do_user_account.read_yaml("borrow", "id")  # 获取已经注册的借款人用户id
            data = re.sub(cls.borrow_user_id_pattern, str(borrow_user_id), data)

        # 借款人手机号替换
        if re.search(cls.borrow_user_tel_pattern, data):
            borrow_user_mobile = cls.do_user_account.read_yaml("borrow", "mobile_phone")  # 获取已经注册的借款人手机号
            data = re.sub(cls.borrow_user_tel_pattern, borrow_user_mobile, data)

        # 借款人密码替换
        if re.search(cls.borrow_user_pwd_pattern, data):
            borrow_user_pwd = cls.do_user_account.read_yaml("borrow", "pwd")  # 获取已经注册的借款人密码
            data = re.sub(cls.borrow_user_pwd_pattern, borrow_user_pwd, data)

        return data

    @classmethod
    def admin_user_replace(cls,data):
        # 管理员手机号替换
        if cls.admin_user_tel_pattern in data:
            admin_user_mobile = cls.do_user_account.read_yaml("admin", "mobile_phone")  # 获取已经注册的管理员手机号
            data = re.sub(cls.admin_user_tel_pattern, admin_user_mobile, data)

        # 管理员密码替换
        if cls.admin_user_pwd_pattern in data:
            admin_user_pwd = cls.do_user_account.read_yaml("admin", "pwd")  # 获取已经注册的管理员密码
            data = re.sub(cls.admin_user_pwd_pattern, admin_user_pwd, data)

        return data

    @classmethod
    def other_replace(cls,data):
        # load_id替换
        if re.search(cls.loan_id_pattern, data):
            loan_id = getattr(cls, 'loan_id')
            data = re.sub(cls.loan_id_pattern, str(loan_id), data)
        return data

    @classmethod
    def to_param(cls, data):
        data = cls.not_existed_replace(data)
        data = cls.invest_user_replace(data)
        data = cls.admin_user_replace(data)
        data = cls.borrow_user_replace(data)
        data = cls.other_replace(data)

        return data


if __name__ == '__main__':
    #     注册接口参数化
    one_str = '{"mobile_phone":"{not_existed_tel}","pwd":"12345678","type":1,"reg_name":"xiaobai"}'
    two_str = '{"mobile_phone":"","pwd":"12345678","type":1}'
    three_str = '{"mobile_phone":"{not_existed_tel}","pwd":"qwertyuiop12345678","type":1,"reg_name":"xiaobai"}'
    four_str = '{"mobile_phone":"{invest_user_tel}","pwd":"12345678","reg_name":"xiaobai"}'
    # 登录接口参数化
    five_str = '{"mobile_phone":"{invest_user_tel}","pwd":"{invest_user_pwd}"}'
    six_str = '{"pwd":"{invest_user_pwd}"}'
    # param = Parameterize()
    # print(param.to_param(one_str))
    # print(param.to_param(two_str))
    # print(param.to_param(three_str))
    # print(param.to_param(four_str))

    print(Parameterize.to_param(one_str))
    print(Parameterize.to_param(two_str))
    print(Parameterize.to_param(three_str))
    print(Parameterize.to_param(four_str))
    print(Parameterize.to_param(five_str))
    print(Parameterize.to_param(six_str))
