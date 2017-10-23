# -*- coding: UTF-8 -*-
'''
    get the biggest staff_id and store it in the json file,
    for the use of increasing staff_id automatic
'''
import json

from module.staff_list import staff_list_get


def get_id(read_file,write_file):
    read_list = staff_list_get(read_file)
    staff_id_list = []
    for i in range(1,len(read_list)):
        staff_id_list.append(read_list[i][0])
    staff_id_list.sort()
    now_id = staff_id_list[-1]
    with open(write_file, "w", encoding="utf-8") as f_wead:
        id_dict = {"staff_id":now_id}
        json.dump(id_dict,f_wead)
get_id("../config/staff_info.txt","../config/staff_id.json")