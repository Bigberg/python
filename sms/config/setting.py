# -*- coding: UTF-8 -*-

from sqlalchemy import create_engine


# 如果插入数据有中文，需要指定 charset=utf8
engine = create_engine("mysql+pymysql://root:111111@172.16.200.49:3306/sms?charset=utf8",
                       encoding='utf-8')

