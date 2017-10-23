# -*- coding: UTF-8 -*-


# class School(object):
#     ' 创建一个school类 '
#
#     def __init__(self, name, location):
#         self.name = name
#         self.location = location
#
#     @staticmethod
#     def create_school():
#         school_name = input('Please input the name of the school:')
#         school_location = input('Please input the location of the school:')
#         school_data = {
#             ''
#         }


# import random
#
# s = random.randint(1, 100)
# print(s)
import pickle
#
with open("../db/student/Python01/P01001.dat", 'rb') as f_r:
    s_dict = pickle.load(f_r)

    print(s_dict)
# with open("../db/student/Python02/P02001.dat", 'wb') as f_w:
#     pickle.dump(s_dict, f_w)

