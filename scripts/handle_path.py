# -*- coding: UTF-8 -*-
# file: handle_path.py
# author:Administrator
# Time: 2019/11/20 20:13
# software: PyCharm

import os

# print(__file__)
# one_path = os.path.abspath(__file__)
# two_path = os.path.dirname(one_path)
# three_path = os.path.dirname(two_path)
# 项目根路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 获取配置文件所在的路径
CONFIGS_DIR = os.path.join(BASE_DIR,'configs')

# 获取配置文件所在的路径
CONFIG_FILE_PATH = os.path.join(CONFIGS_DIR,'testcase.yaml')

# 获取日志文件所在的路径
LOGS_DIR = os.path.join(BASE_DIR,'logs')

# 获取报告文件所在的路径
REPORT_DIR = os.path.join(BASE_DIR,'reports')

# 获取excel文件所在的路径
DATAS_DIR = os.path.join(BASE_DIR,'datas')

#
CASES_DIR = os.path.join(BASE_DIR,'cases')

#获取用户帐号所在配置文件路径
USER_ACCOUNTS_FILE_PATH = os.path.join(CONFIGS_DIR,'user_account.yaml')

pass