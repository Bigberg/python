# -*- coding: UTF-8 -*-
import os
import configparser
import json
import hashlib
# 路径
BasePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = configparser.ConfigParser()
config.read("{}/config/setting.ini".format(BasePath), encoding='utf-8')


class User(object):
    # 用于生成ftp用户

    def __init__(self):
        self.name = ''
        self.password = ''
        self.dir_size = ''
        self.dir = config.get('DEFAULT', 'ftp_dir')

    def user_create(self):
        # 创建用于
        self.name = input('输入用户名:').strip()
        # 判断文件夹是否重复
        while os.path.exists(os.sep.join([self.dir, self.name])):
            print('用户名已存在,请重新输入')
            self.name = input('输入用户名:').strip()
        self.password = input('输入密码:').strip()
        repeat_password = input('请重新输入密码:').strip()
        while not repeat_password == self.password:
            print("两次输入的密码不一致,请重新输入密码:")
            self.password = input('输入密码:').strip()
            repeat_password = input('请重新输入密码:').strip()
        else:
            # 磁盘配额，默认10
            choice = input('请输入磁盘配额,默认10M：').strip()

            if choice.lower() == 'y':
                self.dir_size = config.get('DEFAULT', 'default_size')
            else:
                number = choice[:-1]
                unit = choice[-1]
                units = ['k', 'K', 'm', 'M', 'g', 'G']
                while number.isdigit() is not True or unit not in units:
                    print('please input the size like: 10M')
                    choice = input('请输入磁盘配额,默认10M[Y/y]：').strip()
                    number = choice[:-1]
                    unit = choice[-1]

                else:
                    self.dir_size = choice

            # 保存用户信息
            db_path = os.sep.join([BasePath, 'db'])
            file_path = os.sep.join([db_path, '%s.dat' % self.name])
            # md5 加密
            m = hashlib.md5()
            m.update(self.password.encode('utf-8'))
            passwd_md5 = m.hexdigest()
            # print(passwd_md5)
            with open(file_path, 'w') as f:
                user_dict = {
                    'username': self.name,
                    'password': passwd_md5,
                    'dir_size': self.dir_size
                }
                json.dump(user_dict, f)
            # 创建用户家目录
            user_dir = os.sep.join([self.dir, self.name])
            os.makedirs(user_dir)


if __name__ == '__main__':
    someone = User()
    someone.user_create()
