# -*- coding: UTF-8 -*-
from data import db_tables_create
from data.db_tables_create import Teacher
from data.db_tables_create import Class
from data.db_tables_create import Student
from data.db_tables_create import Class_m2m_Day
from data.db_tables_create import Day
from data.db_tables_create import Record
from config.setting import engine
from sqlalchemy.orm import sessionmaker
import hashlib

from sqlalchemy.orm import sessionmaker
import hashlib
m = hashlib.md5()
m.update(b'111111')
# 创建session会话
Session_class = sessionmaker(bind=db_tables_create.engine)
# 生成session实例
session = Session_class()

# stu_obj = session.query(Student).filter(Student.s_id==1).first()
# print(stu_obj.record)
# class_obj = session.query(Class).filter(Class.c_id==1).first()
# # print(class_obj.student)
# print(class_obj.class_to_day[0].record[0].commit)
# user_name = input('>>:').strip()
# t_obj = session.query(Teacher).filter(Teacher.t_id == 1).first()
# print(t_obj, t_obj.t_id)
# c_obj = session.query(Class).filter(Class.c_id == 2).first()
# print(c_obj.c_name, c_obj.c_id)
#
# classes = t_obj.classes
# classes.append(c_obj)
# print(classes)
# t_obj.classes = classes
# class_obj = session.query(Class).filter(Class.c_id > 0).all()
#
# choice_list = []
# for i in range(len(class_obj)):
#     print(i+1, ':', class_obj[i])
#     choice_list.append(i+1)
# # print(choice_list)
# choice = input("选择班级，多个班级以','分开:")
# class_num = choice.split(',')
# for i in range(len(class_num)):
#     class_num[i]= class_num[i].lstrip().rstrip()
# # print(class_num)
# while True:
#     for i in range(len(class_num)):
#         if class_num[i].isdigit() is not True or  int(class_num[i]) not in choice_list:
#             print("编号输入有误,请重新输入")
#             break
#     else:
#         print("该学生选择的课程如下:")
#         for i in range(len(class_num)):
#             class_name = str(class_obj[int(class_num[i]) - 1])
#             print(type(class_name))
#             print(class_name)
#             print(type(class_obj[int(class_num[i]) - 1]))
#
#         break
#
#     choice = input("选择班级，多个班级以','分开:")
#     class_num = choice.split(',')
#     for i in range(len(class_num)):
#         class_num[i] = class_num[i].lstrip().rstrip()
# t_obj.classes.append(c_obj)
# stu_obj = session.query(Student).filter(Student.s_qq == 10008).first()
# print(stu_obj.s_name)
# print(type(stu_obj.s_name))
# print(type(stu_obj.classes[0]))
class_obj = session.query(Class).filter(Class.c_name == "Python第一期").first()
for i in range(len(class_obj.student)):
    print(class_obj.student[i].s_id)

# session.commit()