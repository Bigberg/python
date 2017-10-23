# -*- coding: UTF-8 -*-

import os
import time
import pickle
# 自动生成id
from module.identified import identifer
from module.identified import student_id
from module.traverse_files import get_files_info
from test import test1
from config import setting

# authentication_data = setting.authenticated_data


class BaseModle(object):
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self, dbname):
        self.dbname = dbname

    # 装饰器认证是否通过认证
    @classmethod
    def login_required(cls, func):
        def wrapper(*args, **kwargs):
            if args[0].get('authentication'):
                res = func(*args, **kwargs)
                return res
            else:
                exit("\033[31m你还没有登入，请先登入.\033[0m")

        return wrapper

    # 账号和密码认证
    @classmethod
    def match_password(cls, pathname, account, account_passwd):
        file_path = os.path.join(pathname, "{}.dat".format(account))
        with open(file_path, 'rb') as f:
            account_dict = pickle.load(f)
        password = account_dict['password']
        if account_passwd == password:
            return True
        else:
            print("\033[31m密码错误\033[0m")

    # 登入
    @classmethod
    def login_func(cls, dbname, auth_data, retry_count):
        print("欢迎使用课程管理系统".center(50, '*'))
        account_id = input("请输入用户名:").strip()
        account_info = get_files_info(dbname)

        ids = []
        for i in range(len(account_info)):
            ids.append(account_info[i]['id'])
        # print(ids)
        # 判断用户是否存在
        while account_id not in ids:
            print("用户名错误，请重新输入!")
            account_id = input("请输入用户名:").strip()
        else:
            while auth_data['authentication'] is not True and retry_count < 3:
                account_password = input('请输入密码:').strip()
                # 认证结果
                match_result = BaseModle.match_password(dbname, account_id, account_password)
                if match_result:
                    print("登入成功，欢迎{}".format(account_id))
                    auth_data['account_id'] = account_id
                    auth_data['authentication'] = True
                    return auth_data
                retry_count += 1
            else:
                print("\033[31m您尝试登入的次数过多!\033[0m")
                exit()


class Admin(BaseModle):

    def __init__(self, dbname):
        super(Admin, self).__init__(dbname)
        self.teacher_name = ''
        self.nid = ''    # 登入账号
        self.course = ''
        self.password = ''

    # 管理员登入，用户和密码在 config/setting中
    @staticmethod
    def login(auth_data):
        # 登入次数
        retry_count = 0
        account_name = input('管理员账号:').strip()
        account_passwd = input('管理账号密码:').strip()
        while retry_count < 3 and auth_data['authentication'] is not True:
            if account_name == setting.admin_user.get('username') \
                    and account_passwd == setting.admin_user.get('password'):
                print('欢迎登入，管理员!')
                auth_data['account_id'] = account_name
                auth_data['authentication'] = True
                return auth_data
            retry_count += 1
        else:
            print("\033[31m您尝试登入的次数过多!\033[0m")
            exit()

    # 创建讲师方法
    # @BaseModle.login_required   # 认证登入装饰器
    def create_teacher(self, auth_data):
        db_path = os.path.join(BaseModle.base_path, 'db', self.dbname)
        print("开始创建授课讲师")
        self.teacher_name = input("请输入教师姓名:").strip()
        self.nid = identifer(db_path)
        self.course = input('请输入授课名称:').strip()
        self.password = input('请输入初始登入密码:').strip()
        self.save_func('teacher')
        print("讲师编号：{}".format(self.nid))
        print("初始密码：{}".format(self.password))

    # 定义一个保存教师信息的方法
    def save_func(self, dbname):
        db_path = os.path.join(BaseModle.base_path, 'db', dbname)
        file_path = os.path.join(db_path, '{}.dat'.format(self.nid))
        with open(file_path, 'wb') as f:
            data = {
                'teacher_name': self.teacher_name,
                'id': self.nid,
                'course': self.course,
                'password': self.password
            }
            pickle.dump(data, f)
        print('一个讲师已经招募!')


class Teacher(BaseModle):

    # 判断教师是否选择了班级
    class_been_choice = {
        'account_id': None,
        'class_name': None
    }

    def __init__(self, dbname):
        super(Teacher, self).__init__(dbname)

    # 登入
    def login(self, auth_data):
        # 记录登入次数
        retry_count = 0
        db_path = os.path.join(BaseModle.base_path, 'db', self.dbname)
        BaseModle.login_func(db_path, auth_data, retry_count)
        return auth_data

    # 选择上课班级
    # @BaseModle.login_required
    def class_choice(self, auth_data):
        print("请选择上课的班级")
        account_id = auth_data['account_id']
        db_path = os.path.join(BaseModle.base_path, 'db', self.dbname)
        file_path = os.path.join(db_path, "{}.dat".format(account_id))
        with open(file_path, 'rb') as f:
            teacher_dict = pickle.load(f)
        course_name = teacher_dict['course']
        # 查询改课程开设的班级
        with open("{}/{}/{}/class_to_course.dat".format(BaseModle.base_path, 'db', 'relationship'), 'rb') as f_class:
            class_dict = pickle.load(f_class)
            class_list = class_dict[course_name]
        for i in range(len(class_list)):
            print(i + 1, ':', class_list[i])
        print("请输入编号选择班级:")
        choice = input("输入编号选择班级:").strip()
        # 判断选择的班级是否正确/存在
        while choice.isdigit() is False or int(choice) not in range(1, len(class_list) + 1):
            print("您的输入有误!")
            choice = input("输入编号选择班级:")
        else:
            # 返回选择的班级
            classroom = class_list[int(choice)-1]
            class_data = {
                'account_id': account_id,
                'class_name': classroom
            }
            print('您选择上课的班级为: {}'.format(classroom))
            Teacher.class_been_choice = class_data
            return Teacher.class_been_choice

    # 查看学员列表
    # @BaseModle.login_required
    def show_students(self, auth_data):
        # 判断是否已经选择上课班级,如果没有选择就先选择
        while Teacher.class_been_choice.get('class_name') is None:
            print("\033[31m您还没有选择上课的班级，请先选择!\033[0m")
            Teacher.class_been_choice = self.class_choice(auth_data)
        else:
            classroom = Teacher.class_been_choice['class_name']
            db_path = os.path.join(BaseModle.base_path, 'db', 'student', classroom)
            print('正在列出所有学员信息...')
            student_info = get_files_info(db_path)
            student_list = []
            for i in range(len(student_info)):
                s_list = []
                s_list.append(student_info[i]['id'])
                s_list.append(student_info[i]['student_name'])
                student_list.append(s_list)
            # print(student_list)
            print("{:^8}{:^8}".format("学号", "姓名"))
            for i in range(len(student_list)):
                print("{:^10}{:^10}".format(student_list[i][0], student_list[i][1]))

    # 修改分数
    # @BaseModle.login_required
    def manage_score(self, auth_data):
        # 判断是否已经选择上课班级,如果没有选择就先选择
        while Teacher.class_been_choice.get('class_name') is None:
            print("\033[31m您还没有选择上课的班级，请先选择!\033[0m")
            Teacher.class_been_choice = self.class_choice(auth_data)
        else:
            classroom = Teacher.class_been_choice['class_name']
            db_path = os.path.join(BaseModle.base_path, 'db', 'student', classroom)
            student_info = get_files_info(db_path)
            # 保存所有学号
            student_list = []
            for i in range(len(student_info)):
                student_list.append(student_info[i]['id'])
            s_id = input("请输入需要修改分数的学号:").strip()
            while s_id not in student_list:
                print("输入的学号不存在,请重新输入")
                s_id = input("请输入需要修改分数的学号:").strip()
            else:
                file_path = os.path.join(db_path, "{}.dat".format(s_id))
                with open(file_path, 'rb') as f_read:
                    info_list = pickle.load(f_read)
                    scores_list = info_list['score']
                for i in range(len(scores_list)):
                    print(i+1, ':', scores_list[i])
                choice = input('输入编号修改成绩:')
                while choice.isdigit() is not True and int(choice) \
                        not in range(1, len(scores_list)+1):
                    print("\033[31m您的输入有误，请重新输入\033[0m")
                else:
                    new_score = input("请输入新的分数:")
                    # 0-100内的数值
                    while new_score.isdigit() is not True or int(new_score) < 0 or \
                                    int(new_score) > 100:
                        print("\033[31m您的输入有误，请输入0-100的数值\033[0m")
                        new_score = input("请输入新的分数:")
                    scores_list[int(choice)-1] = new_score
                    print("修改完成!")
                    for i in range(len(scores_list)):
                        print(i+1, ':', scores_list[i])
                    info_list['score'] = scores_list
                    with open(file_path, 'wb') as f_write:
                        pickle.dump(info_list, f_write)


class Student(BaseModle):
    # 记录登入后学生的班级
    classroom_login = {'class_name': None}

    def __init__(self, dbname):
        super(Student, self).__init__(dbname)
        self.student_name = ''
        self.nid = ''      # 学号/登入账号
        self.course_id = ''
        self.course_name = ''
        self.classroom = ''
        self.password = '111111'  # 初始密码
        self.score = []
        self.status = 0

    # 学生注册
    def enroll(self):

        class_path = os.path.join(BaseModle.base_path, 'db', 'relationship')
        # 列出课程信息
        course_info = test1.BaseModle.get_obj_info('course')
        # print(course_info)
        course_id = []
        for i in range(len(course_info)):
            course_id.append(course_info[i]['id'])
            print("课程信息".center(30, '*'))
            print("课程编号: {}".format(course_info[i]['id']))
            print("课程名称: {}".format(course_info[i]['course_name']))
            print("课程周期: {}".format(course_info[i]['circle']))
            print("学费：{}".format(course_info[i]['price']))
            print('\n')
        print("请您填写注册信息".center(50, '*'))
        self.student_name = input("您的姓名:").strip()
        self.course_id = input("输入课程编号选择课程:").strip()
        while self.course_id not in course_id:
            print("您输入的信息有误!")
            self.course_id = input("输入课程id选择课程:").strip()
        else:
            course_index = course_id.index(self.course_id)
            with open('{}/{}'.format(class_path, 'class_to_course.dat'), 'rb') as f:
                class_to_course = pickle.load(f)
                # print(class_to_course)
            course_name = course_info[course_index]['course_name']
            self.course_name = course_name
            print("您所选择的课程是: {}".format(course_name))
            classroom_list = class_to_course[course_name]
            # 选择班级
            print("该课程的班级数如下：")
            for i in range(len(classroom_list)):
                print(i+1, ':', classroom_list[i])
            print("请输入编号选择班级:")
            class_choice = input("输入编号选择班级:").strip()
            # 判断选择的班级是否正确/存在
            while class_choice.isdigit() is False or int(class_choice) not in range(1, len(classroom_list)+1):
                print("您的输入有误!")
                class_choice = input("输入编号选择班级:")
            else:
                self.classroom = classroom_list[int(class_choice)-1]
                db_path = os.path.join(BaseModle.base_path, 'db', self.dbname, self.classroom)
                self.nid = student_id(db_path, self.classroom)
                print("恭喜，注册成功!".center(30, '*'))
                print("您所学课程为:{}".format(self.course_name))
                print("您的班级为:{}".format(self.classroom))
                print("系统自动为您分配的学号是:{}".format(self.nid))
                print("初始密码为:{}".format(self.password))
                print("登入后请及时修改密码!")
                self.save_func(db_path)

    # 登入
    def login(self, auth_data):
        # 记录登入次数
        retry_count = 0
        # 学生登入时要求先选择班级
        classroom = input("请输入您的班级:").strip()
        class_info = get_files_info("{}/{}/{}".format(BaseModle.base_path, 'db', 'classinfo'))
        classrooms = []
        for i in range(len(class_info)):
            classrooms.append(class_info[i]['class_name'])
        while classroom not in classrooms:
            print("您的输入有误,请重新输入!")
            classroom = input("请输入您的班级:").strip()
        else:
            db_path = os.path.join(BaseModle.base_path, 'db', self.dbname, classroom)
            BaseModle.login_func(db_path, auth_data, retry_count)
            Student.classroom_login['class_name'] = classroom
            return auth_data

    # 定义一个方法保存学生注册信息
    def save_func(self, db_path):
        file_path = os.path.join(db_path, '{}.dat'.format(self.nid))
        student_dict = {
            'id': self.nid,
            'student_name': self.student_name,
            'student_course': self.course_name,
            'student_class': self.classroom,
            'password': self.password,
            'score': self.score,
            'status': self.status
        }
        f_open = open(file_path, "wb")
        pickle.dump(student_dict, f_open)
        f_open.flush()
        f_open.close()
        time.sleep(2)

    # @BaseModle.login_required
    def reset_passwd(self, auth_data):
        # 修改初始密码
        db_path = os.path.join(BaseModle.base_path, 'db', 'student', Student.classroom_login['class_name'])
        file_path = os.path.join(db_path, "{}.dat".format(auth_data['account_id']))
        with open(file_path, 'rb') as f_read:
            student_dict = pickle.load(f_read)
        new_passwd = input('请输入新密码:').strip()
        retry_passwd = input("请重新输入新密码:").strip()
        while new_passwd != retry_passwd:
            print("您两次输入的密码不一致，请重新输入!")
            new_passwd = input('请输入新密码:').strip()
            retry_passwd = input("请重新输入新密码:").strip()
        else:
            with open(file_path, 'wb') as f_write:
                student_dict['password'] = new_passwd
                pickle.dump(student_dict, f_write)
        print('密码更改成功')

    # @BaseModle.login_required
    def pay_tuition(self, auth_data):
        student_db_path = os.path.join(BaseModle.base_path, 'db', 'student', Student.classroom_login['class_name'])
        student_file_path = os.path.join(student_db_path, '{}.dat'.format(auth_data['account_id']))
        with open(student_file_path, 'rb') as f_read:
            student_dict = pickle.load(f_read)
            status = student_dict.get('status')
            course_name = student_dict.get('student_course')
        # 判断学费是否已经交过了
        if int(status) == 1:
            print("\033[31m您的学费已经交过了!\033[0m")

        else:
            # 从课程数据库中读取课程费用
            course_file_path = os.path.join(BaseModle.base_path, 'db', 'course', '{}.dat'.format(course_name))
            with open(course_file_path, 'rb') as f_course:
                course_dict = pickle.load(f_course)
                price = course_dict['price']
                print(price)
            tuition = input("请输入学费金额:").strip()
            while tuition.isdigit() is not True or int(tuition) != int(price):
                print('\033[31m请输入正确的学费金额!\033[0m')
                tuition = input("请输入学费金额:").strip()
            else:
                # 我们将交了学费的学生状态改为 1
                student_dict['status'] = 1
                with open(student_file_path, 'wb') as f_write:
                    pickle.dump(student_dict, f_write)
                print('完成交学费!')


if __name__ == '__main__':
    pass
    # a = Admin('teacher')
    # a.login(authentication_data)
    # a.create_teacher(authentication_data)
    # s_info = test1.BaseModle.get_obj_info('student/Python01')
    # print(s_info)
    # s = Student('student')
    # s.login()
    # s.pay_tuition(authentication_data)
    # s.reset_passwd(authentication_data)
    # t = Teacher('teacher')
    # t.login()
    # t.show_students(authentication_data)
    # t.manage_score(authentication_data)
    #t.class_choice(authentication_data)



