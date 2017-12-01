# -*- coding: UTF-8 -*-
import os
import json
import configparser
from core.itemlog import item_log


# 登入认证

def auth_login():
    # 读取配置文件admin用户信息
    config = configparser.ConfigParser()
    config.read("../conf/setting.ini", encoding='utf-8')
    user_name = config['DEFAULT']['AdminUser']
    user_password = config['BASE']['AdminPassword']
    access_log = item_log('access')
    error_log = item_log('error')
    # 登入次数计算器
    count = 0

    # 输入用户名和密码
    while count < 3:
        user = input('请输入用户名:').strip()
        password = input('请输入密码:').strip()

        if user == user_name and password == user_password:
            print('Welcome Admin.')
            access_log.info('admin login successfully.')
            return True
        else:
            error_log.error('登入认证失败.')
            if count < 2:
                print('您输入的信息有误!请重新输入。')

        count += 1
    else:
        print("您尝试登入次数过多，请稍后登入!")
        return False

if __name__ == '__main__':
    auth_login()