# -*- coding: UTF-8 -*-
from core import role

from config import setting
authentication_data = setting.authenticated_data


def choose_class(data):
    t = role.Teacher('teacher')
    t.class_choice(data)


def show_students(data):
    t = role.Teacher('teacher')
    t.show_students(data)


def manage_scores(data):
    t = role.Teacher('teacher')
    t.manage_score(data)


def login_out(data):
    print("\033[32m讲师{},欢迎下次再使用!\033[0m".format(data['account_id']))
    exit()


def interaction(data):
    menu = '''--- 课程管理系统后台 ---
    \033[32m 1. 选择上课班级
     2. 查看学员
     3. 修改分数
     4. 退出
\033[0m-----------------------'''
    menu_dict = {
        "1": choose_class,
        "2": show_students,
        "3": manage_scores,
        "4": login_out
    }
    while True:
        print(menu)
        choice = input("输入编号选择您所需的功能:").strip()
        if choice in menu_dict:
            menu_dict[choice](data)
        else:
            print("\033[31;1m没有该项功能，请重新选择!\033[0m")


def run():
    t = role.Teacher('teacher')
    acc_data = t.login(authentication_data)
    if acc_data['authentication']:
        interaction(acc_data)
