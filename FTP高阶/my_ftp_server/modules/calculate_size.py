# -*- coding: UTF-8 -*-
import os
import json


def get_used_size(dirname):
    """
        遍历文件夹获取文件大小

    """
    size = 0
    for dir_path, dirs, files in os.walk(dirname):
        # size += sum([os.path.getsize(os.sep.join([dir_path, name])) for name in files])
        for name in files:
            size += os.path.getsize(os.sep.join([dir_path, name]))
    return size


def free_space(db_file, size):
    # 用于计算剩余空间
    with open(db_file, 'r') as f:
        info_dict = json.load(f)
        space_size = info_dict['dir_size']
    num = int(space_size[:-1])
    unit = space_size[-1]
    if unit.lower() == 'k':
        total_size = num * 1024
    elif unit.lower() == 'm':
        total_size = num * (1024 ** 2)
    else:
        total_size = num * (1024 ** 3)

    return total_size - size


# if __name__ == '__main__':
#     used_size = get_used_size(r'G:\ftp\home\bigberg')
#     print(used_size)
#     free_size = free_space("../db/bigberg.dat", used_size)
#     print(free_size)
