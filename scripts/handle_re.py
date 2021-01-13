# -*- coding: UTF-8 -*-
# file: handle_re.py
# author:Administrator
# Time: 2019/11/21 19:33
# software: PyCharm

import re

# 1、创建待替换的字符串
one_str = '{"mobile_phone":"{not_existed_tel}","pwd":"12345678","type":1,"reg_name":"xiaobai"}'

# 2、创建正则表达式
# 正则表达式中一定要加r，如果有些字符串有特殊含义，需要在前面加一个\
re_str = r'{not_existed_tel}'

# match方法第一个参数为正则表达式，第二个参数为带查询的字符串
# match方法只能从头开始匹配
# 如果匹配不上，会返回None
# 如果能匹配上，会返回match对象

# mtch = re.match(r'{"mobile_phone":"{not_existed_tel}',one_str)
# 可以使用mtch.group()获取匹配成功之后的值
# mtch = re.match(r'{"mobile_phone":"{not_existed_tel}',one_str)

# search
# search方法，不用从头开始匹配，只要能匹配上，就直接返回
# 如果能匹配上，返回Match
# 如果匹配不上，会返回None
# 可以使用mtch.group()获取匹配成功之后的值
mtch = re.search(r'{not_existed_tel}', one_str)

# sub
# sub方法第一个参数为正则表达式字符串，第二个参数为新的值（字符串），
# 第三个参数为待替换的字符串（原始字符串）
# 如果匹配上，会返回替换之后的值（一定为字符串类型）
# 如果匹配不上，会返回原始字符
re.sub(r'{not_existed_tel}','18822226666',one_str)

# 在项目中search方法和sub方法会合在一起用
if re.search(r'{not_existed_tel}', one_str):
    res = re.sub(r'{not_existed_tel}','18822226666',one_str)
# split    分割
# findall    把所有满足条件的值放入一个列表返回
# finditer   把所有满足条件的值构造成一个生成器返回