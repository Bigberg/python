# -*- coding: UTF-8 -*-
'''
    处理sql 语句中 where 条件的打印
    具体是 select name,age,phone （这些字段内容的打印） from staff_table where staff_id = 1

'''
from module.print_css import style3
from module.print_css import style4
def sql_query_condition(list_name,index_number,index_list):
    for j in range(len(index_list)):
        style3(list_name[index_number], index_list[j])
        if j == len(index_list) - 2:
            style4(list_name[index_number], index_list[len(index_list) - 1])
            break


