# -*- coding: UTF-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import setting


engine = create_engine(setting.ConnParams)
# engine = create_engine(settings.DB_CONN,echo=True)

SessionCls = sessionmaker(bind=engine)
# 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
session = SessionCls()
