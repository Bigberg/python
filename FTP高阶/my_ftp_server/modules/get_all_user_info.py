# -*- coding: UTF-8 -*-

import os
import json


# 遍历文件夹，获取文件信息
def get_user_info(pathname):
    all_info = []
    for file_name in os.listdir(pathname):
        # print(filename)
        with open("{}\{}".format(pathname, file_name), 'r') as f_read:
            obj_info = json.load(f_read)
        all_info.append(obj_info)
    return all_info

# info = get_user_info('..\db')
# print(info)

