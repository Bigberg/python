# -*- coding: UTF-8 -*-

from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from config.setting import engine
from data.db_tables_create import Teacher
from data.db_tables_create import Class
from data.db_tables_create import Student
from data.db_tables_create import Day
from data.db_tables_create import Class_m2m_Day
from data.sms_data import create_data
from data.sms_data import Record
import hashlib

# 定义一个教师全局变量


class BaseMode(object):
    '''
    基础功能
    '''
    def __init__(self, session):
        self.session = session
        # self.initialize_data()

    def initialize_data(self):
        # 如果没有数据，就初始化
        res = self.session.query(Teacher).filter_by().all()
        # print(res)
        if not res:
            create_data()


class TeacherClass(BaseMode):
    '''
    教师类
    '''
    def __init__(self, session):
        super(TeacherClass, self).__init__(session)

    def login(self):

        # 查询数据库
        while True:
            # 验证密码
            m = hashlib.md5()
            # 登入
            user_name = input("请输入用户名:").strip()
            user_passwd = input("请输入密码:").strip()
            m.update(user_passwd.encode())
            md5_passwd = m.hexdigest()
            global t_obj
            try:
                t_obj = self.session.query(Teacher).filter(Teacher.t_account == user_name).first()
                account = t_obj.t_account
                password = t_obj.t_password
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
        # 选择班级
        print('请选择班级')
        choice_list = []
        for i in range(len(t_obj.classes)):
            print(i+1, ':', t_obj.classes[i])
            choice_list.append(i+1)
        choice = input("请选择班级:").strip()
        while True:
            if choice.isdigit() is False or int(choice) not in choice_list:
                print('\033[31;1m选择有误,请重新输入\033[0m')
                choice = input("请选择班级:").strip()
            else:
                print('该班的学生如下:')
                student_obj = t_obj.classes[int(choice)-1].student
                for i in student_obj:
                    print(i)
                return t_obj.classes[int(choice)-1]

    def create_class(self):
        # 新建课程，并为新课程添加教师
        print("\033[31;1m 创建课程\033[0m".center(32, '-'))
        courses = input("课程名称:").strip()
        # 教师表插入数据
        class_obj = Class(c_name=courses)
        # 打印教师信息，以供选择
        teacher_objs = self.session.query(Teacher).filter(Teacher.t_id > 0).all()
        choice_list = []
        for i in range(len(teacher_objs)):
            print(i+1, ':', teacher_objs[i])
            choice_list.append(i+1)
        choice = input("请选择教师:")
        while True:
            if choice.isdigit() is False or int(choice) not in choice_list:
                print('\033[31;1m选择有误,请重新输入\033[0m')
                choice = input("请选择授课教师:").strip()
            else:
                teacher_to_class = self.session.query(Teacher).filter(
                    Teacher.t_account == teacher_objs[int(choice) - 1].t_account).first()
                teacher_to_class.classes.append(class_obj)
                self.session.add(class_obj)
                self.session.commit()
                print('新课程添加完成!')
                new_class_obj = self.session.query(Class).filter(Class.c_name == courses).first()
                print('新增课程:', new_class_obj.c_name)
                print("授课教师:", new_class_obj.teacher)
                break

    def add_teacher(self):
        # 新增教师
        m_teacher = hashlib.md5()
        print("\033[31;1m新增教师\033[0m".center(32, '-'))
        # 编号唯一,不能冲突
        account = input("教师编号:").strip()
        exist_account = self.session.query(Teacher).filter(Teacher.t_account==account).first()
        while exist_account:
            print('该教师编号已存在,请重新分配')
            account = input("教师编号:").strip()
            exist_account = self.session.query(Teacher).filter(Teacher.t_account == account).first()
        name = input("教师姓名:").strip()
        password = input("输入密码:").strip()
        m_teacher.update(password.encode())
        m_teacher_password = m_teacher.hexdigest()
        new_teacher_obj = Teacher(t_account=account, t_name=name, t_password=m_teacher_password)
        self.session.add(new_teacher_obj)
        self.session.commit()
        print("新教师添加完成!")

    def add_new_student(self):
        # 新增学生，并将其加入班级
        m_student = hashlib.md5()
        print("\033[31;1m新增学生\033[0m".center(32, '-'))
        # 新增学生qq唯一，不能和已有冲突，这里不验证qq是否正确了
        qq_number = input("学生qq号:").strip()
        exist_qq = self.session.query(Student).filter(Student.s_qq == qq_number).first()
        while exist_qq:
            print("该qq号已经存在,请核实该学员信息")
            qq_number = input("学生qq号:").strip()
            exist_qq = self.session.query(Student).filter(Student.s_qq == qq_number).first()
        name = input("学生姓名:").strip()
        password = input("输入密码:").strip()
        m_student.update(password.encode())
        m_student_password = m_student.hexdigest()
        new_student_obj = Student(s_name=name, s_qq=qq_number, s_password=m_student_password)
        # 选择班级
        print("\033[31;1m选择班级\033[0m".center(32, '-'))
        class_objs = self.session.query(Class).filter(Class.c_id > 0).all()
        choice_list = []
        for i in range(len(class_objs)):
            print(i + 1, ':', class_objs[i])
            choice_list.append(i + 1)
        # print(choice_list)
        # 学生可以报多个课程
        choice = input("选择班级，多个班级以','分开:")
        class_num = choice.split(',')
        for i in range(len(class_num)):
            class_num[i] = class_num[i].lstrip().rstrip()
        # print(class_num)
        while True:
            for i in range(len(class_num)):
                if class_num[i].isdigit() is not True or int(class_num[i]) not in choice_list:
                    print("编号输入有误,请重新输入")
                    break
            else:
                print("该学生选择的课程如下:")
                for i in range(len(class_num)):
                    class_name = str(class_objs[int(class_num[i]) - 1])
                    print(class_name)
                    class_to_student_obj = self.session.query(Class).filter(Class.c_name == class_name).first()
                    class_to_student_obj.student.append(new_student_obj)
                self.session.add(new_student_obj)
                self.session.commit()
                print('\033[31;1m信息注册完成!\033[0m')
                break
            choice = input("选择班级，多个班级以','分开:")
            class_num = choice.split(',')
            for i in range(len(class_num)):
                class_num[i] = class_num[i].lstrip().rstrip()

    def class_add_student(self):
        # 如果有老学员需要选择新课程
        print("\033[31;1m添加课程\033[0m".center(32, '-'))
        qq_num = input('学生qq号:')
        stu_obj = self.session.query(Student).filter(Student.s_qq == qq_num).first()
        while not stu_obj:
            print('你输入的学生qq不存在,请重新输入!')
            qq_num = input('学生qq号:')
            stu_obj = self.session.query(Student).filter(Student.s_qq == qq_num).first()
        else:
            class_obj = self.session.query(Class).filter(Class.c_id > 0).all()
            # 将该学员已有课程排除，防止重复选择
            all_classes_set = set(class_obj)
            stu_classes_set = set(stu_obj.classes)
            # 差集
            different_set = all_classes_set.difference(stu_classes_set)
            classes_benn_choice = list(different_set)

            choice_list = []
            for i in range(len(classes_benn_choice)):
                print(i+1, ':', classes_benn_choice[i])
                choice_list.append(i+1)
            choice = input("选择班级:").strip()
            while choice.isdigit() is False or int(choice) not in choice_list:
                print('\033[31;1m您的输入有误!\033[0m')
                choice = input("选择班级:").strip()
            else:
                class_name = str(classes_benn_choice[int(choice) - 1])
                # print(class_name)
                class_add_student_obj = self.session.query(Class).filter(Class.c_name == class_name).first()
                class_add_student_obj.student.append(stu_obj)
                self.session.commit()
                print("学员:", qq_num)
                print("所选课程:", class_name)
                print("\033[31;1m学员信息更新完毕\033[0m")

    def generate_day(self):
        # 生成日期,如day1, day2
        day_objs = self.session.query(Day).filter(Day.d_id > 0).all()
        # print(day_objs)
        day_list = []
        for i in day_objs:
            print(i)
            day_list.append(str(i))
        while True:
            day = input("课程日期(like:day1):")
            if day in day_list:
                print("该日期已经建立,不能重复")
                continue
            else:
                day_obj = Day(d_day=day)
                self.session.add(day_obj)
                self.session.commit()
                print("新日期创建完成")
                break

    def generate_record(self):
        # 生成课程记录

        # 选择课程
        print("\033[31;1m选择课程\033[0m".center(32, '-'))
        courses_name = self.choose_class()
        # print(courses_name)
        # print(type(courses_name))
        # 选择日期
        print("\033[31;1m选择日期\033[0m".center(32, '-'))
        day_objs = self.session.query(Day).filter(Day.d_id > 0).all()

        choice_list = []
        for i in range(len(day_objs)):
            print(i+1, ':', day_objs[i])
            choice_list.append(i+1)
        while True:
            choice = input("选择日期(Q/q退出):").strip()
            if choice.lower() == 'q':
                break
            elif choice.isdigit() is not True or int(choice) not in choice_list:
                print("输入有误,请重新输入")
                continue
            else:
                # 先判断该课程和日期的关系是否已经建立，避免重复
                day_obj = self.session.query(Day).filter(Day.d_day == str(day_objs[int(choice) - 1])).first()
                class_obj = self.session.query(Class).filter(Class.c_name == str(courses_name)).first()
                # print(day_obj, class_obj)
                day_id = day_obj.d_id
                class_id = class_obj.c_id
                # print(day_id, class_id)
                class_m2m_day_obj = self.session.query(Class_m2m_Day).filter(
                    and_(Class_m2m_Day.day_id == day_id, Class_m2m_Day.class_id == class_id)).all()
                if class_m2m_day_obj:
                    print("该条记录已经被创建,请确认信息是否正确!")
                    continue
                else:
                    # 新建课程和日期记录，并创建该课程所有学员当前日期的记录
                    new_class_to_day_obj = Class_m2m_Day(class_id=class_id, day_id=day_id)
                    self.session.add(new_class_to_day_obj)
                    self.session.commit()
                    class_to_day_obj = self.session.query(Class_m2m_Day).filter(
                        and_(Class_m2m_Day.day_id == day_id, Class_m2m_Day.class_id == class_id)).first()
                    class_to_day_id = class_to_day_obj.id
                    # 获取该班级所有学员
                    student_in_class_obj = self.session.query(Class).filter(Class.c_name == str(courses_name)).first()
                    # print(student_in_class_obj.student)
                    for i in range(len(student_in_class_obj.student)):
                        record_obj = Record(class_m2m_day_id=class_to_day_id, s_id=student_in_class_obj.student[i].s_id,
                                            status="已签到")
                        self.session.add(record_obj)
                        self.session.commit()
                    print("\033[31;1m初始化[%s][%s]完成!\033[0m" % (courses_name, day_obj.d_day))
                    break

    def set_score(self):
        # 为学员评分

        # 选择课程
        print("\033[31;1m选择课程\033[0m".center(32, '-'))
        courses_name = self.choose_class()

        # 选择日期
        print("\033[31;1m选择日期\033[0m".center(32, '-'))
        day_objs = self.session.query(Day).filter(Day.d_id > 0).all()

        choice_list = []
        for i in range(len(day_objs)):
            print(i + 1, ':', day_objs[i])
            choice_list.append(i + 1)
        while True:
            choice = input("选择日期(Q/q退出):").strip()
            if choice.lower() == 'q':
                break
            elif choice.isdigit() is not True or int(choice) not in choice_list:
                print("输入有误,请重新输入")
                continue
            else:
                # 先判断该条记录是否存在
                day_obj = self.session.query(Day).filter(Day.d_day == str(day_objs[int(choice) - 1])).first()
                class_obj = self.session.query(Class).filter(Class.c_name == str(courses_name)).first()
                # print(day_obj, class_obj)
                day_id = day_obj.d_id
                class_id = class_obj.c_id
                # print(day_id, class_id)
                class_m2m_day_obj = self.session.query(Class_m2m_Day).filter(
                    and_(Class_m2m_Day.day_id == day_id, Class_m2m_Day.class_id == class_id)).first()
                # 如果没有该条记录，则该天课程还没有建立，无法修改作业成绩
                if not class_m2m_day_obj:
                    print("\033[31;1m尚未有当天课程记录,请先创建课程记录\033[0m")
                    print("请重新选择日期")
                    continue
                else:
                    # 打印学员信息
                    class_m2m_day_id = class_m2m_day_obj.id
                    record_obj = self.session.query(Record).filter(
                        Record.class_m2m_day_id == str(class_m2m_day_id)).all()
                    for i in range(len(record_obj)):
                        print(record_obj[i].student.s_qq, record_obj[i].student.s_name, record_obj[i].commit,
                              record_obj[i].score)

                    # 修改已提交的作业
                    commit_obj = self.session.query(Record).filter(
                        and_(Record.class_m2m_day_id == str(class_m2m_day_id),
                             Record.commit == "已提交")
                    ).all()

                    # 如果没有人提交作业,重新选择
                    if len(commit_obj) == 0:
                        print("\033[31;1m当前日期课程未有人提交作业\033[0m")
                        continue
                    else:
                        print("\033[31;1m为已提交学员评分\033[0m")
                        for i in range(len(commit_obj)):
                            print(commit_obj[i].student.s_qq, commit_obj[i].student.s_name)
                            while True:
                                score = input("请为学员评分(0-100):")
                                if score.isdigit() is not True or int(score) > 100 or int(score) <= 0:
                                    print("输入有误,请重新输入")
                                    continue
                                else:
                                    commit_obj[i].score = int(score)
                                    self.session.commit()
                                    break
                        print("\033[31;1m该次已提交学员成绩评分完成\033[0m")
                    break


if __name__ == '__main__':
    session_class = sessionmaker(bind=engine)
    my_session = session_class()
    t = TeacherClass(my_session)
    t.login()
    # t.set_score()
    # t.generate_record()
    t.generate_day()
    # t.class_add_student()
    # t.add_new_student()
    # t.add_teacher()
    # t.create_class()


