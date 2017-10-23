# -*- coding: UTF-8 -*-
from core import role
from core import school
from config import setting

authentication_data = setting.authenticated_data


# 登入认证
@role.BaseModle.login_required
def create_school(data):
    s = school.School('school')
    s.create(data)


@role.BaseModle.login_required
def create_course(data):
    c = school.Course('course')
    c.create(data)


@role.BaseModle.login_required
def create_classroom(data):
    cla = school.Class('classinfo')
    cla.create(data)


@role.BaseModle.login_required
def create_teacher(data):
    t = role.Admin('teacher')
    t.create_teacher(data)


def login_out(data):
    print("\033[32m管理员{},欢迎下次再使用!\033[0m".format(data['account_id']))
    exit()


def interaction(data):
    menu = '''--- 课程管理系统后台 ---
        \033[32m 1. 创建学校
         2. 创建课程
         3. 创建教室
         4. 创建讲师
         5. 退出
\033[0m-----------------------'''
    menu_dict = {
        "1": create_school,
        "2": create_course,
        "3": create_classroom,
        "4": create_teacher,
        "5": login_out
    }
    while True:
        print(menu)
        choice = input("输入编号选择您所需的功能:").strip()
        if choice in menu_dict:
            menu_dict[choice](data)
        else:
            print("\033[31;1m没有该项功能，请重新选择!\033[0m")


def run():
    print("欢迎使用课程管理系统".center(40, '*'))
    a = role.Admin('admin')
    acc_data = a.login(authentication_data)
    if acc_data['authentication']:
        interaction(acc_data)
