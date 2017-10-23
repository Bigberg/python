# -*- coding: UTF-8 -*-
import os
import sys
from MALL.core import main

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(basedir)
sys.path.append(basedir)


if __name__ == '__main__':
    main.run()
