# -*- coding: UTF-8 -*-
# file: handle_user.py
# author:Administrator
# Time: 2019/11/26 15:25
# software: PyCharm

from scripts.handle_mysql import HandleMysql
from scripts.handle_path import USER_ACCOUNTS_FILE_PATH
from scripts.handle_request import HandleRequest
from scripts.handle_yaml import do_yaml


def create_new_user(reg_name,pwd='12345678',user_type=1):
    """

    :param reg_name:
    :param pwd:
    :param user_type:
    :return:
    """
    # 建立连接
    do_mysql = HandleMysql()
    do_request = HandleRequest()
    # 添加公共请求头
    do_request.add_headers(do_yaml.read_yaml('api','version'))

    url = do_yaml.read_yaml('api','prefix')+'/member/register'
    sql = do_yaml.read_yaml('mysql','select_userid_sql')
    while True:
        mobile_phone = do_mysql.create_not_existed_mobile()
        data = {
            "mobile_phone":mobile_phone,
            "pwd":pwd,
            "reg_name":reg_name,
            "type":user_type
        }
        # 先注册接口发起请求
        do_request.send(url,data=data)

        # 查询数据库，获取用户id
        result = do_mysql.run(sql =sql, args=(mobile_phone,))
        if result:
            user_id = result["id"]
            break

    # 构造用户信息字典
    user_dict = {
        reg_name:{
            "id":user_id,
            "reg_name":reg_name,
            "mobile_phone":mobile_phone,
            "pwd":pwd
        }

        }
    #关闭连接
    do_mysql.close()
    do_request.close()

    return user_dict

def generate_users_config():
    """
    生成三个用户信息
    :return:
    """
    users_datas_dict = {}
    users_datas_dict.update(create_new_user("admin",user_type=0))
    users_datas_dict.update(create_new_user("borrow"))
    users_datas_dict.update(create_new_user("invest"))
    do_yaml.write_yaml(users_datas_dict,USER_ACCOUNTS_FILE_PATH)


if __name__ == '__main__':
    generate_users_config()