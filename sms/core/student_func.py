# -*- coding: UTF-8 -*-
from sqlalchemy.orm import sessionmaker
from config.setting import engine
from core.studentrole import StudentClass


def commit_homework():
    s.commit_homework()


def show_rank():
    s.ranking()


def login_out():
    exit()


def interactive():
    menu = '''\033[32m
  1. 提交作业
  2. 查询排名
  3. 退出

\033[0m-----------------------'''
    menu_dict = {
        "1": commit_homework,
        "2": show_rank,
        "3": login_out
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
    global s
    s = StudentClass(my_session)
    s.login()
    interactive()
