# -*- coding: UTF-8 -*-
from sqlalchemy.orm import sessionmaker
from config.setting import engine
from core.role import TeacherClass
from core.role import BaseMode


def add_courses():
    t.create_class()


def add_teacher():
    t.add_teacher()


def add_student():
    t.add_new_student()


def append_courses():
    t.class_add_student()


def add_day():
    t.generate_day()


def add_record():
    t.generate_record()


def set_score():
    t.set_score()


def login_out():
    exit()


def interactive():
    menu = '''\033[32m
   1. 创建新课程
   2. 新增教师
   3. 新增学员
   4. 老学员新增课程
   5. 增加课程日期
   6. 新增课程记录
   7. 评分
   8. 退出
\033[0m-----------------------'''
    menu_dict = {
        "1": add_courses,
        "2": add_teacher,
        "3": add_student,
        "4": append_courses,
        "5": add_day,
        "6": add_record,
        "7": set_score,
        "8": login_out
    }
    while True:
        print(menu)
        choice = input("输入编号选择您所需的功能:").strip()
        if choice in menu_dict:
            menu_dict[choice]()
        else:
            print("\033[31;1m没有该项功能，请重新选择!\033[0m")


def run():
    session_class = sessionmaker(bind=engine)
    my_session = session_class()
    global t
    t = TeacherClass(my_session)

    t.login()
    interactive()
