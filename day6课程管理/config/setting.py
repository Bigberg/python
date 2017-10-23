# -*- coding: UTF-8 -*-

import os

Base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(Base_dir)

# 管理员账号和密码
admin_user = {
    'username': 'admin',
    'password': 'admin'
}

DATABASE = {
    'engine': 'file_storage',
    'path': "{}/db".format(Base_dir)
}

# 学生注册状态信息
status = {
    'wait_for_pass': 0,
    'authenticated': 1,
    'reject': 2
}

# 登入认证

authenticated_data = {
    'account_id': None,
    'authentication': False
}
