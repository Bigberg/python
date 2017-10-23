# -*- coding: UTF-8 -*-

# 随机生成10个100以内的分数，用于测试
import random
import os
import pickle


def scores(pathname):
    with open(pathname, 'rb') as f:
        info_dict = pickle.load(f)
        score_list = info_dict['score']
        for i in range(10):
            score = random.randint(1, 100)
            score_list.append(score)
    with open(pathname, 'wb') as f_write:
        info_dict['score'] = score_list
        pickle.dump(info_dict, f_write)

if __name__ == '__main__':
    scores("../db/student/Python01/P01002.dat")
