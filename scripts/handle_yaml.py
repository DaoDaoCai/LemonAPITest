# -*- coding: UTF-8 -*-
# file: read_yaml_test.py
# author:Administrator
# Time: 2019/11/4 15:16
# software: PyCharm


import yaml
from scripts.handle_path import CONFIG_FILE_PATH

class HandleYaml:
    def __init__(self,filename):
        with open(filename, "r", encoding="utf-8")as one_file:
            self.datas = yaml.load(one_file, Loader=yaml.FullLoader)

    def read_yaml(self,dic1,dic2):
        return self.datas[dic1][dic2]

    @staticmethod
    def write_yaml(datas,filename):
        with open(filename, "w", encoding="utf-8")as one_file:
            yaml.dump(datas, one_file, allow_unicode=True)

do_yaml = HandleYaml(CONFIG_FILE_PATH)

if __name__ == '__main__':
    w = HandleYaml()
    datas = {
        "excel": {
            "cases_path": "cases.xlsx"
        },
        "user": {
            "username": "H.Y",
            "password": "123456"
        }
    }
    w.write_yaml("t1.yaml",datas)

    r = HandleYaml(CONFIG_FILE_PATH)
    p = r.read_yaml('excel','cases_path')
    print(p)
