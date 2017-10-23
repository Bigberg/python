# -*- coding: UTF-8 -*-
import os
import logging
Base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(Base_dir)

DATABASE = {
    'engine': 'file_storage',
    'username': 'account',  # 用户信息
    'transaction': 'record',  # 记录交易信息
    'path': "{}\db".format(Base_dir)
}

Log_lev = logging.INFO

Log_type = {
    'transaction': 'transaction.log',  # 交易日志
    'access': 'access.log',  # 登入成功日志
    'error': 'error.log'  # 错误日志
}

TRANS_TYPE = {
    'repay': {'interest': 0, 'action': 'plus'},
    'withdraw': {'interest': 0.05, 'action': 'minus'},
    'transfer': {'interest': 0.05, 'action': 'minus'}
}
