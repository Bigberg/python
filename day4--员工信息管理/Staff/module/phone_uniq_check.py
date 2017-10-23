# -*- coding: UTF-8 -*-
def phone_check(list1,list2,target):
    target_list = []
    target_index = list1.index(target)
    for i in range(len(list2)):
        target_list.append(list2[i][target_index])
    return target_list