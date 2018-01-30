# -*- coding: UTF-8 -*-
from core.role import BaseMode
from sqlalchemy.orm import sessionmaker
from config.setting import engine

if __name__ == '__main__':
    session_class = sessionmaker(bind=engine)
    my_session = session_class()
    init = BaseMode(my_session)
    init.initialize_data()
