# -*- coding: UTF-8 -*-

# 自增id
import os
import re

# 用于学校、课程、教师id


def identifer(db_path):
    num = 0
    for i in os.listdir(db_path):
        num += 1
    num += 1
    str_num = str(num)
    if len(str_num) > 5:
        print('您的学校数量已经超过99999所,请重新设置数量值')
        exit()
    else:
        return '0' * (5-len(str_num)) + str_num


# 用于学生id
def student_id(db_path, class_name):
    num = 0
    for i in os.listdir(db_path):
        num += 1
    num += 1
    str_num = str(num)
    head = re.match(".", class_name).group()
    nid = re.search("\d+", class_name).group()
    if len(str_num) > 3:
        print('该班级学生数已满，请选择其他班级')
        exit()
    else:
        return head + nid + '0' * (3-len(str_num)) + str_num

# if __name__ == '__main__':
#     nid = student_id('../db/school', 'Python01')
#     print(nid)
