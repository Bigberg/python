# -*- coding: UTF-8 -*-

from core.role import BaseMode
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from config.setting import engine
from data.db_tables_create import Class
from data.db_tables_create import Student
from data.db_tables_create import Day
from data.db_tables_create import Class_m2m_Day
from data.sms_data import Record
import hashlib


class StudentClass(BaseMode):
    # 学生类

    def __init__(self, session):
        super(StudentClass, self).__init__(session)

    def login(self):

        # 查询数据库
        while True:
            # 登入
            m = hashlib.md5()
            user_name = input("请输入用户名:").strip()
            user_passwd = input("请输入密码:").strip()
            m.update(user_passwd.encode())
            md5_passwd = m.hexdigest()
            global stu_obj
            try:
                stu_obj = self.session.query(Student).filter(Student.s_qq == user_name).first()
                account = stu_obj.s_qq
                password = stu_obj.s_password
                if user_name == account and md5_passwd == password:
                    print("*" * 26)
                    print("* \033[31;1m欢迎使用学员管理系统\033[0m *")
                    print("*" * 26)

                    break
                else:
                    print('输入的用户号或密码不正确')
                    continue
            except Exception:
                print('输入的用户号或密码不正确')
                continue

    @staticmethod
    def choose_class():
        # 选择课程
        print("\033[31;1m选择课程\33[0m".center(32, '-'))
        choice_list = []
        for i in range(len(stu_obj.classes)):
            print(i+1, ':', stu_obj.classes[i])
            choice_list.append(i+1)
        while True:
            choice = input("选择班级:").strip()
            if choice.isdigit() is not True or int(choice) not in choice_list:
                print('\033[31;1m您的输入有误,请确认信息\033[0m')
                continue
            else:
                # print(stu_obj.classes[int(choice) - 1].c_id)
                return stu_obj.classes[int(choice) - 1].c_id

    def choose_day(self):
        # 选择哪天课程
        print("\033[31;1m选择提交作业的日期\33[0m".center(27, '-'))
        day_objs = self.session.query(Day).filter(Day.d_id > 0).all()
        choice_list = []
        for i in range(len(day_objs)):
            print(i + 1, ':', day_objs[i])
            choice_list.append(i + 1)
        while True:
            choice = input("选择日期:").strip()
            if choice.isdigit() is not True or int(choice) not in choice_list:
                print("输入有误,请重新输入")
                continue
            else:
                return day_objs[int(choice) - 1].d_id

    def commit_homework(self):
        # 选择交作业的课程和日期
        class_id = self.choose_class()

        day_id = self.choose_day()

        # 存在该课程和日期的对应关系？
        class_m2m_day_obj = self.session.query(Class_m2m_Day).filter(
            and_(Class_m2m_Day.class_id == class_id, Class_m2m_Day.day_id == day_id)
        ).first()
        if not class_m2m_day_obj:
            print("\033[31;1m该课程在此日期无课程记录,需先创建课程记录\033[0m")

        else:
            class_m2m_day_id = class_m2m_day_obj.id
            stu_id = stu_obj.s_id
            record_obj = self.session.query(Record).filter(
                and_(Record.class_m2m_day_id == class_m2m_day_id,
                     Record.s_id == stu_id)).first()
            if record_obj.commit == "已提交":
                print("\033[31;1m本次作业已交提交,无需再次提交\033[0m")

            else:
                record_obj.commit = "已提交"
                self.session.commit()
                print("\033[31;1m本次作业提交完成\033[0m")

    def ranking(self):
        # 查询排名
        class_id = self.choose_class()
        class_obj = self.session.query(Class).filter(Class.c_id == class_id).first()
        # 将学员qq信息和分数组成元组
        student_and_score_list = []
        # 单独分数列表
        score_list = []
        for j in range(len(class_obj.student)):
            print(class_obj.student[j].s_qq, class_obj.student[j].s_name)
            num = 0
            for i in range(len(class_obj.class_to_day)):
                record_obj = self.session.query(Record).filter(and_(
                    Record.s_id == class_obj.student[j].s_id,
                    Record.class_m2m_day_id == class_obj.class_to_day[i].id
                )).first()
                score = record_obj.score
                num += score
            print(num)
            student_and_score_list.append((class_obj.student[j].s_qq, num))
            score_list.append(num)
        # 分数使用集合去重
        rank_list = list(set(score_list))
        rank_list.sort()
        rank_list.reverse()
        # 获取该学员的分数
        student_score = 0
        for i in range(len(student_and_score_list)):
            if student_and_score_list[i][0] == stu_obj.s_qq:
                student_score = student_and_score_list[i][1]
        rank = rank_list.index(student_score) + 1
        print(stu_obj.s_qq, stu_obj.s_name, '排名为:', rank)

if __name__ == '__main__':
    session_class = sessionmaker(bind=engine)
    my_session = session_class()
    s = StudentClass(my_session)
    s.login()
    s.ranking()
    # s.commit_homework()
    # s.choose_class()
    # s.choose_day()
