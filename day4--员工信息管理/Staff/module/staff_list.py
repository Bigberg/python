# -*- coding: UTF-8 -*-
'''
   create a list of the staff_table infomation
'''
def staff_list_get(filename):
    read_list = []
    with open(filename,"r",encoding="utf-8") as f_read:
        lines = f_read.readlines()
    for line in lines:
        read_list.append(line.strip())
    return read_list
