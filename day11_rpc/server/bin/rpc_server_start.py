# -*- coding: UTF-8 -*-
import sys, os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)
from core.rpc_server import run

if __name__ == '__main__':
    run()
