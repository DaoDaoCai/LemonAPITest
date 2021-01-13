# -*- coding: UTF-8 -*-
# file: test_register_case.py
# author:Administrator
# Time: 2019/10/23 15:55
# software: PyCharm
import json
import unittest

from scripts.handle_excel import HandleExcel
from libs.ddt import ddt, data
from scripts.handle_log import do_log
from scripts.handle_yaml import do_yaml
from scripts.handle_request import HandleRequest
from scripts.handle_mysql import HandleMysql
from scripts.handle_parameterize import Parameterize


@ddt
class TestRecharge(unittest.TestCase):
    """
    测试充值功能
    """
    excel = HandleExcel("recharge")
    cases = excel.read_data_obj()

    @classmethod
    def setUpClass(cls):
        cls.do_request = HandleRequest()
        cls.do_request.add_headers(do_yaml.read_yaml("api", "version"))
        cls.do_mysql = HandleMysql()

    @classmethod
    def tearDownClass(cls):
        cls.do_request.close()
        cls.do_mysql.close

    @data(*cases)
    def test_recharge(self, case):
        # 1、参数化
        new_data = Parameterize.to_param(case.data)

        # 2、拼接完整的url
        new_url = do_yaml.read_yaml("api", "prefix") + case.url

        check_sql = case.check_sql
        if check_sql:
            # 如果excel中sql列不为空，参数化sql
            check_sql = Parameterize.to_param(check_sql)
            mysql_data = self.do_mysql.run(sql=check_sql)  # 执行sql

            # 发起请求，得到充值前的金额
            leave_amount_before = round(float(mysql_data['leave_amount']), 2)

        # 3、向服务器发起请求
        res = self.do_request.send(url=new_url,
                                   method=case.method,
                                   data=new_data,
                                   is_json=True)
        # 将相应报文中的数据转化为字典
        actual_value = res.json()

        if case.case_id == 2:
            token = actual_value['data']['token_info']['token']
            # 更新请求体
            headers = {"Authorization": "Bearer " + token}
            self.do_request.add_headers(headers)

        # 获取该用例在excel中的行
        row = case.case_id + 1
        # 预期结果    将expected期望值转化为字典
        expected_result = case.expected

        msg = case.title  # 获取标题
        success_msg = do_yaml.read_yaml("msg", "success_result")  # 获取用例执行成功提示
        fail_msg = do_yaml.read_yaml("msg", "fail_result")  # 获取用例执行失败提示

        try:
            # assertEqual第三个参数为用例执行失败之后的提示信息
            # assertEqual第一个参数为期望值，第二个参数为实际值
            # self.assertEqual(expected_result, actual_value.get('code'), msg=msg)
            self.assertEqual(expected_result, actual_value.get('code'), msg=msg)
            if check_sql:
                mysql_data = self.do_mysql.run(sql=check_sql)
                leave_amount_after = round(float(mysql_data['leave_amount']), 2)

                one_dict = json.loads(new_data, encoding='utf-8')
                currrent_recharge_amount = one_dict['amount']
                actual_amount = round(leave_amount_before + currrent_recharge_amount, 2)
                self.assertEqual(actual_amount, leave_amount_after, msg="数据库中充值的金额有误")

        except AssertionError as e:
            # 将相应实际值写入到actual_col列
            self.excel.write_data(row=row,
                                  column=do_yaml.read_yaml("excel", "actual_col"),
                                  value=res.text)
            # 将用例执行结果写入到result_col列
            self.excel.write_data(row=row,
                                  column=do_yaml.read_yaml("excel", "result_col"),
                                  value=fail_msg)
            do_log.error(f"{msg},执行的结果为：{fail_msg}\n具体异常为{e}\n")
            raise e
        else:
            # 将相应实际值写入到actual_col列
            self.excel.write_data(row=row,
                                  column=do_yaml.read_yaml("excel", "actual_col"),
                                  value=res.text)
            # 将用例执行结果写入到result_col列
            self.excel.write_data(row=row,
                                  column=do_yaml.read_yaml("excel", "result_col"),
                                  value=success_msg)
            do_log.info(f"{msg},执行的结果为：{success_msg}\n")


if __name__ == '__main__':
    unittest.main
