# -*- coding: UTF-8 -*-
import os
import configparser
import pickle
from modules import get_user_infomation
from core import FtpLog
from modules import login_required

# 路径
BasePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = configparser.ConfigParser()
config.read("{}/config/setting.ini".format(BasePath), encoding='utf-8')
# print(config.get('DEFAULT', 'FtpHomeDir'))

account_data = {
    'account_name': None,
    'authentication': False
}

f_log = FtpLog.FTPLog('logs')
ftp_logger = f_log.ftp_log()


class User(object):
    # ftp根目录
    ftp_dir = config.get('DEFAULT', 'FtpHomeDir')

    def __init__(self, dbname):
        self.dbname = dbname

    # 注册方法
    def sign_up(self):
        username = input("请输入用户名:").strip()
        # 判断用户名是否重复
        info_list = get_user_infomation.get_files_info(os.path.join(BasePath, self.dbname))
        name_list = []
        for i in range(len(info_list)):
            name_list.append(info_list[i]['username'])
        while username in name_list:
            print("用户名已经存在，请重新输入!")
            username = input("请输入用户名:").strip()
        password = input("请输入密码:").strip()
        repeat_password = input("请重新输入密码:").strip()
        while not repeat_password == password:
            print("您两次输入的密码不一致，请重新输入")
            repeat_password = input("请重新输入密码:").strip()
        else:
            # pickle 序列化, 新建用户家目录
            file_path = os.path.join("{}/{}/{}.txt".format(BasePath, self.dbname, username))
            with open(file_path, 'wb') as f_write:
                user_dict = {
                    'username': username,
                    'password': password,
                    'status': 0  # 0代表正常，1 代表不正常
                }
                pickle.dump(user_dict, f_write)

            user_dir = "{}".format(os.sep).join([self.ftp_dir, username])
            # 创建家目录
            os.makedirs(user_dir)
            print("注册成功!")
            ftp_logger.info("新用户{}注册成功".format(username))

    # 账号和密码认证
    @staticmethod
    def match_password(pathname, account, account_passwd):
        file_path = os.path.join(pathname, "{}.txt".format(account))
        with open(file_path, 'rb') as f_read:
            account_dict = pickle.load(f_read)
        password = account_dict['password']
        if account_passwd == password:
            return True
        else:
            print("\033[31m密码错误\033[0m")

    # 登入方法
    def sign_in(self, auth_data):
        user_name = input('请输入用户名:').strip()
        info_list = get_user_infomation.get_files_info(os.path.join(BasePath, self.dbname))
        name_list = []
        for i in range(len(info_list)):
            name_list.append(info_list[i]['username'])
        while user_name not in name_list:
            print('用户名不存在，请重新输入')
            ftp_logger.error("用户名{}不存在".format(user_name))
            user_name = input('请输入用户名:').strip()
        else:
            name_index = name_list.index(user_name)
            # 判断用户状态是否正常
            user_info = info_list[name_index]
            status = user_info['status']
            if status == 1:
                print("您的账号存在风险,现在不能登入!")
                ftp_logger.error("账号{}存在风险,登入失效!".format(user_name))
            else:
                retry_count = 0
                while auth_data.get('authentication') is not True and retry_count < 3:
                    user_password = input('请输入密码:').strip()
                    match_result = User.match_password(os.path.join(BasePath, 'db'), user_name, user_password)
                    if match_result:
                        print("登入成功，欢迎{}".format(user_name))
                        ftp_logger.info("{}成功登入".format(user_name))
                        auth_data['account_name'] = user_name
                        auth_data['authentication'] = True
                        return auth_data
                    retry_count += 1
                else:
                    print("\033[31m您尝试登入的次数过多!\033[0m")
                    ftp_logger.error('{}多次登入密码错误,可能存在风险,将被限制登入！')
                    with open('{}'.format(os.sep).join([BasePath, self.dbname, "{}.txt".format(user_name)]), 'wb') \
                            as f_write:
                        user_info['status'] = 1
                        pickle.dump(user_info, f_write)
                    exit()

    # 列出ftp用户目录下的文件
    @login_required.login_required
    def show_files(self, auth_data):
        print("{}目录下的文件".format(auth_data.get('account_name')))
        user_dir = os.path.join(self.ftp_dir, auth_data.get('account_name'))
        os.listdir(user_dir)

if __name__ == '__main__':
    u = User('db')
    # u.sign_in(account_data)
    u.show_files(account_data)
