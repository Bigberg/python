# -*- coding: UTF-8 -*-

import os
import pickle
# 自动生成id
from module.identified import identifer

# 基类


class BaseModle(object):
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self, dbname):
        self.dbname = dbname
    # 定义一个方法，获取数据库中的数据

    @classmethod
    def get_obj_info(cls, dbname, *args):
        res = []
        # base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(BaseModle.base_path, 'db', dbname,)
        # print(db_path)
        for file_name in os.listdir(db_path):
            # print(filename)
            with open("{}\{}".format(db_path, file_name), 'rb') as f:
                obj_info = pickle.load(f)
            res.append(obj_info)
        return res

    # 定义一个方法来设置各个对象的关系
    @classmethod
    def relationship(cls, obj1, obj2, dbname, arg):
        # base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(BaseModle.base_path, 'db', dbname)
        file_path = os.path.join(db_path, '{}_to_{}.dat'.format(obj1, obj2))
        while True:
            try:
                with open(file_path, 'rb') as f_read:
                    relationship_info = pickle.load(f_read)
                    if arg not in relationship_info:
                        relationship_info[arg] = []
                        return relationship_info
                    else:
                        return relationship_info

            except FileNotFoundError:
                with open(file_path, 'wb') as f_write:
                    relation_dict = {

                    }
                    pickle.dump(relation_dict, f_write)

# 学校类


class School(BaseModle):

    def __init__(self, dbname):
        super(School, self).__init__(dbname)
        # self.dbname = dbname
        self.school_name = ''
        self.city = ''
        self.school_address = ''
        self.nid = ''

    # 定义创建学校的方法
    def create(self):
        # base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(BaseModle.base_path, 'db', self.dbname)
        self.school_name = input("请输入校名:").strip()
        self.city = input("请输入城市:").strip()
        self.school_address = input("请输入学校详细地址:").strip()
        self.nid = identifer(db_path)
        self.save_func('school')

    # 定义一个保存学校信息的方法
    def save_func(self, dbname):
        # base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(BaseModle.base_path, 'db', dbname)
        file_path = os.path.join(db_path, '{}.dat'.format(self.nid))
        # print(file_path)
        with open(file_path, 'wb') as f:
            data = {
                'name': self.school_name,
                'city': self.city,
                'address': self.school_address,
                'id': self.nid
            }
            pickle.dump(data, f)

# 课程类


class Course(BaseModle):

    def __init__(self, dbname):
        super(Course, self).__init__(dbname)
        self.course_name = ''
        self.price = ''
        self.circle = ''
        self.nid = ''
        self.school_name = ''

    # 定义一个创建课程的方法
    def create(self):
        # base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(BaseModle.base_path, 'db', self.dbname)
        print("请选择创建课程的学校")
        # 获取学校信息，打印出来以供选择
        info = BaseModle.get_obj_info('school')
        # print(info)
        school_id = []
        for i in range(len(info)):
            school_id.append(info[i]['id'])
            print("学校信息".center(30, '*'))
            print("学校编号: {}".format(info[i]['id']))
            print("所在城市: {}".format(info[i]['city']))
            print("学校名称: {}".format(info[i]['name']))
            print("学校地址: {}".format(info[i]['address']))
            print('\n')
        choice_school = input("请输入开课学校编号:").strip()
        # 判断学校是否存在
        while choice_school not in school_id:
            print("您的输入有误,请重新输入学校编号")
            choice_school = input("请输入开课学校编号:").strip()
        else:
            school_index = school_id.index(choice_school)
            self.school_name = info[school_index]['name']
            print(self.school_name)
            self.course_name = input("请输入课程名称:").strip()
            self.circle = input("请输入课程周期(按周):").strip()
            self.price = input("请输入课程价格:").strip()
            self.nid = identifer(db_path)
            # 保存创建的课程信息
            self.save_func('course')
            # 保存课程和学校的关系信息（课程属于哪个学校开的课）
            relationship = BaseModle.relationship('course', 'school', 'relationship', self.school_name)
            relationship[self.school_name].append(self.course_name)
            with open("../db/relationship/course_to_school.dat", 'wb') as f:
                pickle.dump(relationship, f)

    # 定义一个方法保存课程信息
    def save_func(self, dbname):
        # base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(BaseModle.base_path, 'db', dbname)
        file_path = os.path.join(db_path, '{}.dat'.format(self.course_name))
        # print(file_path)0
        with open(file_path, 'wb') as f:
            data = {
                'school_name': self.school_name,
                'course_name': self.course_name,
                'circle': self.circle,
                'price': self.price,
                'id': self.nid
            }
            pickle.dump(data, f)

# 班级类


class Class(BaseModle):

    def __init__(self, dbname):
        super(Class, self).__init__(dbname)
        self.class_name = ''
        self.nid = ''
        self.course_name = ''

    # 定义一个创建班级的方法
    def create(self):
        db_path = os.path.join(BaseModle.base_path, 'db', self.dbname)
        print("请选择开班的课程")
        # 获取课程信息，打印出来以供选择
        info = BaseModle.get_obj_info('course')
        course_id = []
        for i in range(len(info)):
            course_id.append(info[i]['id'])
            print("课程信息".center(30, '*'))
            print("课程编号: {}".format(info[i]['id']))
            print("课程名称: {}".format(info[i]['course_name']))
            print('\n')
        choice_course = input("请输入开班课程编号:").strip()
        # 判断学校是否存在
        while choice_course not in course_id:
            print("您的输入有误,请重新输入学校编号")
            choice_course = input("请输入开课学校编号:").strip()
        else:
            course_index = course_id.index(choice_course)
            self.course_name = info[course_index]['course_name']
            print(self.course_name)
            self.class_name = input("请输入班级名称:").strip()
            self.nid = identifer(db_path)
            # 保存创建的课程信息
            self.save_func('classinfo')
            # 保存课程和学校的关系信息（课程属于哪个学校开的课）
            relationship = BaseModle.relationship('class', 'course', 'relationship', self.course_name)
            relationship[self.course_name].append(self.class_name)
            with open("../db/relationship/class_to_course.dat", 'wb') as f:
                pickle.dump(relationship, f)
            # 创建完成班级后,我们在student目录下,创建一个学生所在的班级目录
            class_path = os.path.join(BaseModle.base_path, 'db', 'student')
            os.makedirs('{}/{}'.format(class_path, self.class_name))

    # 定义一个方法保存班级信息

    def save_func(self, dbname):
        db_path = os.path.join(BaseModle.base_path, 'db', dbname)
        file_path = os.path.join(db_path, '{}.dat'.format(self.nid))
        # print(file_path)0
        with open(file_path, 'wb') as f:
            data = {
                'class_name': self.class_name,
                'id': self.nid
            }
            pickle.dump(data, f)

if __name__ == '__main__':
    c = Course('course')
    c.create()
    # cla = Class('classinfo')
    # cla.create()

    # s = School('school')
    # s.create()
    # c_info = BaseModle.get_obj_info('classinfo')
    # print(c_info)
    # relation_info = BaseModle.get_obj_info('relationship')
    # print(relation_info)
