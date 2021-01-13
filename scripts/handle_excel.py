# -*- coding: UTF-8 -*-
# file: read_excel.py
# author:Administrator
# Time: 2019/10/25 16:20
# software: PyCharm
import openpyxl
import os

from scripts.handle_path import DATAS_DIR
from scripts.handle_yaml import do_yaml


class CaseData():
    """测试用例数据类，专门用来创建对象，存放用例数据"""
    pass


class HandleExcel():
    def __init__(self,sheetname, filename=None ):
        if filename is None:
            self.filename = os.path.join(DATAS_DIR,do_yaml.read_yaml("excel", "cases_path"))
        else:
            self.filename = filename
        self.sheetname = sheetname

    def open(self):
        """打开工作簿和表单"""
        self.wb = openpyxl.load_workbook(self.filename)
        self.sh = self.wb[self.sheetname]

    def read_data(self):
        # 读取数据的方法
        # 打开工作簿和表单
        self.open()
        # 将表单中的内容，按行获取所有的格子
        rows = list(self.sh.rows)

        # 创建一个空列表，用来存放所有的用力数据
        cases = []
        #  获取表头，放到一个列表中
        title = []
        for c in rows[0]:
            title.append(c.value)
        # 获取除了表头以外的其他行中的数据
        for r_obj in rows[1:]:
            # 每遍历一行，创建一个列表，用来存放该行数据
            data = []
            for r in r_obj:
                data.append(r.value)
            # 将表头和该行的数据进行聚合打包，转换成字典
            case_data = dict(zip(title, data))

            # 将该行的用力数据加入到cases这个列表中
            cases.append(case_data)
        self.wb.close()
        # 将读取好的数据返回出去
        return cases

    def read_data_obj(self):
        # 读取数据的方法
        # 打开工作簿和表单
        self.open()
        # 将表单中的内容，按行获取所有的格子
        rows = list(self.sh.rows)
        # 创建一个空列表，用来存放所有的用力数据
        cases = []
        #  获取表头，放到一个列表中
        title = [c.value for c in rows[0]]
        # 获取除了表头以外的其他行中的数据
        for r_obj in rows[1:]:
            # 每遍历一行，创建一个列表，用来存放该行数据
            data = [r.value for r in r_obj]
            # 将表头和该行的数据进行聚合打包，转换成字典
            case_data = dict(zip(title, data))
            case = CaseData()
            for k, v in case_data.items():
                setattr(case, k, v)
            # 将该行的用例数据加入到cases这个列表中
            cases.append(case)

        self.wb.close()
        # 将读取好的数据返回出去
        return cases

    def write_data(self, row, column, value):
        """写入数据"""
        # 打开工作簿和表单
        self.open()
        # 写入内容
        self.sh.cell(row=row, column=column, value=value)
        # 保存文件
        self.wb.save(self.filename)
        # 关闭工作簿
        self.wb.close()


if __name__ == '__main__':
    read = HandleExcel('cases.xlsx', 'register')

    data = read.read_data_obj()
    print(data)
