# -*- coding: UTF-8 -*-
from core import role

from config import setting
authentication_data = setting.authenticated_data


@role.BaseModle.login_required
def pay_tuition(data):
    s = role.Student('student')
    s.pay_tuition(data)


@role.BaseModle.login_required
def reset_passwd(data):
    s = role.Student('student')
    s.reset_passwd(data)


def login_out(data):
    print("\033[32m学员{},欢迎下次再使用!\033[0m".format(data['account_id']))
    exit()


def interaction(data):
    menu = '''--- 课程管理系统 ---
    \033[32m 1. 交学费
     2. 修改密码
     3. 退出
-----------------------'''
    menu_dict = {
        "1": pay_tuition,
        "2": reset_passwd,
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
    choice_list = ['1', '2']
    s = role.Student('student')
    while True:
        print('\033[32m 1.注册 \n 2.登入')
        choice = input("输入编号选择您所需的功能:").strip()
        if choice in choice_list:
            if choice == '1':
                s.enroll()
            else:
                acc_data = s.login(authentication_data)
                if acc_data['authentication']:
                    interaction(acc_data)
        else:
            print("\033[31;1m没有该项功能，请重新选择!\033[0m")