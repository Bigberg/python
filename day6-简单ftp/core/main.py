# -*- coding: UTF-8 -*-
from core.user import User
from core.FtpClient import FtpClient
from modules import login_required

# 登入认证使用
account_data = {
    'account_name': None,
    'authentication': False
}


@login_required.login_required
def upload(data):
    ftp_client = FtpClient('localhost', 8888)
    ftp_client.client_upload(data)


@login_required.login_required
def download(data):
    ftp_client = FtpClient('localhost', 8887)
    ftp_client.client_download(data)


def login_out(data):
    print("\033[32m{},欢迎下次再使用!\033[0m".format(data['account_name']))
    exit()


def interaction(data):

    menu = '''----- FTP功能 ------
    \033[32m 1. 上传
     2. 下载
     3. 退出
--------------------'''
    menu_dict = {
        "1": upload,
        "2": download,
        "3": login_out
    }
    while True:
        print(menu)
        choice = input("输入编号选择您所需的功能:").strip()
        if choice in menu_dict:
            menu_dict[choice](data)
        else:
            print("\033[31;1m没有该项功能，请重新选择!\033[0m")


def run():
    print('欢迎使用FTP'.center(40, '*'))
    choice_list = ['1', '2']
    u = User('db')
    while True:
        print('\033[32m 1.注册 \n 2.登入')
        choice = input("输入编号选择您所需的功能:").strip()
        if choice in choice_list:
            if choice == '1':
                u.sign_up()
            else:
                acc_data = u.sign_in(account_data)
                if acc_data['authentication']:
                    interaction(acc_data)
        else:
            print("\033[31;1m没有该项功能，请重新选择!\033[0m")
