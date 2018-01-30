# -*- coding: UTF-8 -*-

import test.db_tables_create
from test.db_tables_create import Teacher
from test.db_tables_create import Class
from test.db_tables_create import Student
from test.db_tables_create import Class_m2m_Day
from test.db_tables_create import Day
from test.db_tables_create import Record

from sqlalchemy.orm import sessionmaker
import hashlib

#md5
m = hashlib.md5()
m.update(b'111111')


# 初始化数据
def initialize_data():
    # 创建session会话
    session_class = sessionmaker(bind=test.db_tables_create.engine)
    # 生成session实例
    session = session_class()
    t_obj1 = Teacher(t_account='T0001', t_name='Jack', t_password=m.hexdigest())
    t_obj2 = Teacher(t_account='T0002', t_name='Henry', t_password=m.hexdigest())


    c_obj1 = Class(c_name="Python第一期")
    c_obj2 = Class(c_name="Mysql第一期")
    c_obj3 = Class(c_name="Linux第一期")

    t_obj1.classes = [c_obj1, c_obj3]
    t_obj2.classes = [c_obj2]

    s_obj1 = Student(s_name='Harry', s_qq='10001', s_password=m.hexdigest())
    s_obj2 = Student(s_name='Potter', s_qq='10002', s_password=m.hexdigest())
    s_obj3 = Student(s_name='Lily', s_qq='10003', s_password=m.hexdigest())
    s_obj4 = Student(s_name='Shary', s_qq='10004', s_password=m.hexdigest())
    s_obj5 = Student(s_name='Maro', s_qq='10005', s_password=m.hexdigest())
    s_obj6 = Student(s_name='Gary', s_qq='10006', s_password=m.hexdigest())
    s_obj7 = Student(s_name='Sandra', s_qq='10007', s_password=m.hexdigest())
    s_obj8 = Student(s_name='Catty', s_qq='10008', s_password=m.hexdigest())

    c_obj1.student = [s_obj1, s_obj2, s_obj5]
    c_obj2.student = [s_obj1, s_obj3, s_obj7]
    c_obj3.student = [s_obj4, s_obj6, s_obj8]

    day_obj1 = Day(d_day='day1')
    day_obj2 = Day(d_day='day2')
    day_obj3 = Day(d_day='day3')

    class_m2m_day_obj1 = Class_m2m_Day(day_id=1, class_id=1)
    class_m2m_day_obj2 = Class_m2m_Day(day_id=1, class_id=2)
    class_m2m_day_obj3 = Class_m2m_Day(day_id=1, class_id=3)
    class_m2m_day_obj4 = Class_m2m_Day(day_id=2, class_id=1)
    class_m2m_day_obj5 = Class_m2m_Day(day_id=2, class_id=2)
    class_m2m_day_obj6 = Class_m2m_Day(day_id=2, class_id=3)

    record_obj1 = Record(class_m2m_day_id=1,s_id=1, status="已签到",commit="已提交",score=90)
    record_obj2 = Record(class_m2m_day_id=1,s_id=4, status="已签到",commit="已提交",score=78)
    record_obj3 = Record(class_m2m_day_id=1,s_id=5, status="已签到",commit="已提交",score=86)
    record_obj4 = Record(class_m2m_day_id=2,s_id=1, status="已签到",commit="已提交",score=66)
    record_obj5 = Record(class_m2m_day_id=2,s_id=2, status="已签到",commit="已提交",score=98)
    record_obj6 = Record(class_m2m_day_id=2,s_id=3, status="已签到",commit="已提交",score=95)

    session.add_all([t_obj1, t_obj2, c_obj1, c_obj2 ,c_obj3, s_obj1, s_obj2, s_obj3,
                     s_obj4, s_obj5, s_obj6, s_obj7, s_obj8, day_obj1,
                     day_obj2, day_obj3, class_m2m_day_obj1, class_m2m_day_obj2,
                     class_m2m_day_obj3, class_m2m_day_obj4 ,class_m2m_day_obj6,
                     record_obj1, record_obj2, record_obj3, record_obj4, record_obj5,
                     record_obj6])

    session.commit()
