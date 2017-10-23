# -*- coding: UTF-8 -*-
import os

Base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(Base_dir)

DATABASE = {
    'engine': 'file_storage',
    'username': 'account',  # 用户信息
    'shop': 'record',  # 购买记录
    'goods': 'commodity',
    'path': "{}\mall_db".format(Base_dir)
}