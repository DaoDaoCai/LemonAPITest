# -*- coding: UTF-8 -*-
# file: run.py
# author:Administrator
# Time: 2019/11/20 10:16
# software: PyCharm


import unittest
from datetime import datetime
import os

from libs.HTMLTestRunnerNew import HTMLTestRunner
from scripts.handle_yaml import do_yaml
from scripts.handle_path import REPORT_DIR,USER_ACCOUNTS_FILE_PATH,CASES_DIR
from scripts.handle_user import generate_users_config

# 如果用户帐号所在文件不存在，则创建用户帐号，否则不创建
if not os.path.exists(USER_ACCOUNTS_FILE_PATH):
    generate_users_config()

# # 创建测试套件
# suite = unittest.TestSuite()
#
# # 加载测试用例套件
# loader = unittest.TestLoader()
# loader.discover()

suite = unittest.defaultTestLoader.discover(CASES_DIR)

result_full_path = do_yaml.read_yaml("report","name") + '_'+\
                   datetime.strftime(datetime.now(),'%Y%m%d%H%M%S')+".html"
result_full_path = os.path.join(REPORT_DIR,result_full_path)
# 生成html文件的测试报告
with open(result_full_path,'wb')as f:
    # 创建测试运行程序
    runner = HTMLTestRunner(stream=f,
                        title=do_yaml.read_yaml("report","title"),
                        description=do_yaml.read_yaml("report","description"),
                        tester=do_yaml.read_yaml("report","tester"))
    # 执行测试用例
    runner.run(suite)



