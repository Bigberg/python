# -*- coding: UTF-8 -*-

from sqlalchemy import Table, Column, Integer, String, DATE, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# 如果插入数据有中文，需要指定 charset=utf8
engine = create_engine("mysql+pymysql://root:111111@172.16.200.49:3306/sms?charset=utf8",
                       encoding='utf-8')

Base = declarative_base()  # 创建orm基类
Base.metadata.create_all(engine)

# 建表
# 教师和班级关联表
teacher_m2m_class = Table("teacher_m2m_class", Base.metadata,
                          Column("id", Integer, primary_key=True),
                          Column('t_id', Integer, ForeignKey("sms_teacher.t_id")),
                          Column('c_id', Integer, ForeignKey("sms_class.c_id"))
                          )
# 学生和班级关联表
student_m2m_class = Table("student_m2m_class", Base.metadata,
                          Column("id", Integer, primary_key=True),
                          Column('s_id', Integer, ForeignKey("sms_student.s_id")),
                          Column('c_id', Integer, ForeignKey("sms_class.c_id"))
                          )

class Teacher(Base):
    '''
    教师表
    '''
    __tablename__='sms_teacher'
    t_id = Column(Integer,primary_key=True)
    t_account = Column(String(32), nullable=False)
    t_name = Column(String(32), nullable=False)
    t_password = Column(String(32),nullable=False)
    # 教师关联班级
    classes = relationship("Class", secondary= teacher_m2m_class, backref="teacher")
    def __repr__(self):
        return "教师编号:%s" % self.t_account

class Class(Base):
    '''
    班级表
    '''
    __tablename__='sms_class'
    c_id = Column(Integer, primary_key=True)
    c_name = Column(String(32), nullable=False)

    def __repr__(self):
        return self.c_name

class Student(Base):
    '''
    学生表
    '''
    __tablename__='sms_student'
    s_id = Column(Integer, primary_key=True)
    s_name = Column(String(32), nullable=False)
    s_qq = Column(String(20), nullable=False)
    s_password = Column(String(32), nullable=False)
    classes = relationship("Class", secondary=student_m2m_class, backref="student")


    def __repr__(self):
        return "%s %s" % (self.s_id, self.s_name)


class Day(Base):
    '''
    课程日期表
    '''
    __tablename__='sms_day'
    d_id = Column(Integer, primary_key=True)
    d_day = Column(String(15), nullable=False)

    # classes = relationship("Class", backref="day")

    def __repr__(self):
        return self.d_day


class Class_m2m_Day(Base):
    __tablename__="class_m2m_day"
    id = Column(Integer, primary_key=True)
    day_id = Column(Integer, ForeignKey("sms_day.d_id"))
    class_id = Column(Integer, ForeignKey("sms_class.c_id"))

    classes = relationship("Class", backref="class_to_day")
    day = relationship("Day", backref="class_to_day")

    def __repr__(self):
        return "%s %s" % (self.classes, self.day)

class Record(Base):
    __tablename__='sms_record'
    r_id = Column(Integer, primary_key=True)
    class_m2m_day_id = Column(Integer, ForeignKey("class_m2m_day.id"))
    s_id = Column(Integer, ForeignKey("sms_student.s_id"))
    status = Column(String(32), default="未签到")
    commit = Column(String(32), default="未提交")
    score = Column(Integer, default=0, nullable=False)

    m2m = relationship("Class_m2m_Day", backref="record")
    student = relationship("Student", backref="record")

    def __repr__(self):
        return "%s %s %s" %(self.s_id, self.status, self.score)
# 创建表
Base.metadata.create_all(engine)