# -*- coding: UTF-8 -*-
import os
import sys
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, basedir)

from core.selectors_server import run

if __name__ == '__main__':
    run()

