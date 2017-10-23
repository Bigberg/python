# -*- coding: UTF-8 -*-
import os
import sys
from ATM.core import mgmt
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basedir)


if __name__ == '__main__':
    mgmt.run()
