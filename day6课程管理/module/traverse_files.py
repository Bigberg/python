# -*- coding: UTF-8 -*-
import os
import pickle


# 遍历文件夹，获取文件信息
def get_files_info(pathname):
    all_info = []
    for file_name in os.listdir(pathname):
        # print(filename)
        with open("{}\{}".format(pathname, file_name), 'rb') as f:
            obj_info = pickle.load(f)
        all_info.append(obj_info)
    return all_info
