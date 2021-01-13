# -*- coding: UTF-8 -*-
# file: mylogger.py
# author:Administrator
# Time: 2019/11/1 22:15
# software: PyCharm
import logging
import os

from scripts.handle_yaml import do_yaml
from scripts.handle_path import LOGS_DIR

class MyLogger():

    @classmethod
    def creat_logger(cls):
        """创建日志收集器"""
        # 创建一个日志收集器
        my_log = logging.getLogger(do_yaml.read_yaml("log","logname"))
        # 设置日志收集器的收集等级
        my_log.setLevel(do_yaml.read_yaml("log","logger_level"))

        # 设置日志输出格式
        format = logging.Formatter(do_yaml.read_yaml("log","formatter"))

        # 日志的输出
        # 创建一个输出到控制台的收集等级
        sh = logging.StreamHandler()
        sh.setLevel(do_yaml.read_yaml("log","stream_level"))
        # 设置输出到控制台的格式
        sh.setFormatter(format)
        # 将输出渠道添加到日志收集器中
        my_log.addHandler(sh)

        # 创建一个输出到文件的渠道
        fh = logging.FileHandler(filename=os.path.join(LOGS_DIR,do_yaml.read_yaml("log","logfile_name")), encoding='utf-8')
        fh.setLevel(do_yaml.read_yaml("log","logfile_level"))
        # 设置输出到文件的日志格式
        fh.setFormatter(format)

        my_log.addHandler(fh)

        return my_log

do_log = MyLogger.creat_logger()


if __name__ == '__main__':
    log = MyLogger.creat_logger()
    log.info("hello")




