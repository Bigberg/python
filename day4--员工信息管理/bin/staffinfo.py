# -*- coding: UTF-8 -*-
import json

from module.get_now_staff_id import get_id
from module.make_query_dict import query_function
from module.phone_uniq_check import phone_check
from module.print_css import style1
from module.print_css import style4
from module.print_css import style5
from module.print_css import style6
from module.print_head_style import head_style
from module.staff_list import staff_list_get
from module.update_write import update_write_in_file

from Staff.module.query_condition import sql_query_condition

#在此我们指定一下主键
unique_key = "phone"

#先将staff_id存入json文件中，用来自增
get_id("../config/table.txt", "../config/id.json")

while True:
    # staff_table 包含字段
    staff_table = staff_list_get("../config/table.txt")

    # 所有字段名称
    field_all_names_list = staff_table[0].split(",")

    # staff_info_list 没有字段
    staff_info_list = []
    for i in range(1, len(staff_table)):
        info_list = staff_table[i].split(",")
        staff_info_list.append(info_list)

    # 打印匹配条数
    query_count = 0
    query = input(">>>")

    #引用query_action函数，将 sql语句 转换为 字典形式
    sql_dict = query_function(query)
    #print(sql_dict)
    #将要检索的关键词提取出来
    sql_field_name = sql_dict["query_target"]

    if sql_dict["query_action"] == "select":
    #判断检索的关键词是否存在
        for i in range(len(sql_field_name)):
            if sql_field_name[i] not in field_all_names_list and sql_field_name[i] != "*":
                print("Error! \033[31;1m {} \033[0m not in the table.".format(sql_field_name[i]))
                exit()

        # 检索的内容,如 select name,age / *  ,提取出这块
        if sql_field_name[0] == "*":
            sql_field_name = field_all_names_list

        length = len(sql_field_name)
        #打印字段名信息
        head_style(length,sql_field_name)

        # 全部匹配 *
        if sql_dict["query_target"] == ["*"]:
            if sql_dict["query_condition"] == "":
                for i in range(len(staff_info_list)):
                    style6(staff_info_list[i],len(staff_info_list[i]))
                style5(length)
                print("{} rows in set".format(len(staff_info_list)))
            else:
                # 检索的字段名在整个字段名中的 index
                target_object = sql_dict["matching_object"]

                target_index = field_all_names_list.index(target_object)

                if sql_dict["query_matching"] == "=":
                    for i in range(len(staff_info_list)):
                        if sql_dict["query_object_value"] == staff_info_list[i][target_index]:
                            style6(staff_info_list[i], length)
                            query_count += 1

                elif sql_dict["query_matching"] == ">":
                    for i in range(len(staff_info_list)):
                        if staff_info_list[i][target_index] > sql_dict["query_object_value"]:
                            style6(staff_info_list[i],length)
                            query_count += 1

                elif sql_dict["query_matching"] == "<":
                    for i in range(len(staff_info_list)):
                        if staff_info_list[i][target_index] < sql_dict["query_object_value"]:
                            style6(staff_info_list[i],length)
                            query_count += 1

                elif sql_dict["query_matching"] == "!=":
                    for i in range(len(staff_info_list)):
                        if staff_info_list[i][target_index] != sql_dict["query_object_value"]:
                            style6(staff_info_list[i],length)
                            query_count += 1

                elif sql_dict["query_matching"] == "like":
                    for i in range(len(staff_info_list)):
                        if sql_dict["query_object_value"] in staff_info_list[i][target_index]:
                            style6(staff_info_list[i], length)
                            query_count += 1

                else:
                    print("Error!{} is wrong".format(sql_dict["query_matching"]))

                style5(length)
                print("{} rows in set".format(query_count))
        else:
            #不是全部检索，如select name,age


			# 将被检索的字段名在table中的索引找出来
			# 添加索引是为了在select 字段名时,可以不按照顺序进行
            index_list = []
            for i in sql_field_name:
                index_list.append(field_all_names_list.index(i))

            #没有where 条件
            if sql_dict["query_condition"] == "":
                if length == 1:
                    for i in range(len(staff_info_list)):
                        style4(staff_info_list[i], index_list[0])
                    style1()
                    print("{} rows in set".format(len(staff_info_list)))
                else:
                     for i in range(len(staff_info_list)):
                         sql_query_condition(staff_info_list,i,index_list)
                     style5(length)
                     print("{} rows in set".format(len(staff_info_list)))
            else:
                # 检索的字段名在整个字段名中的 index
                target_object = sql_dict["matching_object"]
                # print(type(target_object))
                target_index = field_all_names_list.index(target_object)
                if sql_dict["query_matching"] == "=":
                    if length == 1:
                        for i in range(len(staff_info_list)):
                            if sql_dict["query_object_value"] == staff_info_list[i][target_index]:
                                style4(staff_info_list[i], index_list[0])
                                query_count += 1
                        style1()
                        print("{} rows in set".format(query_count))
                    else:
                        for i in range(len(staff_info_list)):
                            if sql_dict["query_object_value"] == staff_info_list[i][target_index]:
                                sql_query_condition(staff_info_list, i, index_list)
                                query_count += 1
                        style5(length)
                        print("{} rows in set".format(query_count))

                elif sql_dict["query_matching"] == ">":
                     if length == 1:
                        for i in range(len(staff_info_list)):
                            if staff_info_list[i][target_index] > sql_dict["query_object_value"]:
                                style4(staff_info_list[i], index_list[0])
                                query_count += 1
                        style1()
                        print("{} rows in set".format(query_count))
                     else:
                         for i in range(len(staff_info_list)):
                             if staff_info_list[i][target_index] > sql_dict["query_object_value"]:
                                 sql_query_condition(staff_info_list, i, index_list)
                                 query_count += 1

                         style5(length)
                         print("{} rows in set".format(query_count))
                elif sql_dict["query_matching"] == "<":
                    if length == 1:
                        for i in range(len(staff_info_list)):
                            if staff_info_list[i][target_index] < sql_dict["query_object_value"]:
                                style4(staff_info_list[i], index_list[0])
                                query_count += 1
                        style1()
                        print("{} rows in set".format(query_count))
                    else:
                         for i in range(len(staff_info_list)):
                             if staff_info_list[i][target_index] < sql_dict["query_object_value"]:
                                 sql_query_condition(staff_info_list, i, index_list)
                                 query_count += 1
                         style5(length)
                         print("{} rows in set".format(query_count))
                elif sql_dict["query_matching"] == "!=":
                    if length == 1:
                        for i in range(len(staff_info_list)):
                            if staff_info_list[i][target_index] != sql_dict["query_object_value"]:
                                style4(staff_info_list[i], index_list[0])
                                query_count += 1
                        style1()
                        print("{} rows in set".format(query_count))
                    else:
                        for i in range(len(staff_info_list)):
                            if staff_info_list[i][target_index] != sql_dict["query_object_value"]:
                                sql_query_condition(staff_info_list, i, index_list)
                                query_count += 1
                        style5(length)
                        print("{} rows in set".format(query_count))
                elif sql_dict["query_matching"] == "like":
                    if length == 1:
                        for i in range(len(staff_info_list)):
                            if sql_dict["query_object_value"] in staff_info_list[i][target_index]:
                                style4(staff_info_list[i], index_list[0])
                                query_count += 1
                        style1()
                        print("{} rows in set".format(query_count))
                    else:
                        for i in range(len(staff_info_list)):
                            if sql_dict["query_object_value"] in staff_info_list[i][target_index]:
                                sql_query_condition(staff_info_list, i, index_list)
                                query_count += 1

                        style5(length)
                        print("{} rows in set".format(query_count))
                else:
                    print("Error!{} is wrong".format(sql_dict["query_matching"]))
    elif sql_dict["query_action"] == "delete":
        #打印出信息
        for i in range(len(staff_info_list)):
            for j in range(len(staff_info_list[i])):
                if j == len(staff_info_list[i])-1:
                    print(staff_info_list[i][j]+"\n")
                    break
                print(staff_info_list[i][j],end=" ")

        # staff_id列表
        staff_id_list = []
        for i in range(len(staff_info_list)):
            staff_id_list.append(staff_info_list[i][0])
        #print(staff_id_list)

        while True:
            delete_number = input("\033[31;1minput the staff_id to delete infomation\033[0m:")
            #判断输入是否为整数
            if delete_number.isdigit():
                #判断staff_id 是否存在
                if delete_number not in staff_id_list:
                    print("Error!No such staff_id!")
                    continue
                else:
                    with open("../config/table.txt",'r',encoding="utf-8") as read_file:
                        lines = read_file.readlines()
                    with open("../config/table.txt",'w',encoding="utf-8") as write_file:
                        for line in lines:
                            line_list = line.split(",")
                            if delete_number == line_list[0]:
                                continue
                            write_file.write(line)
                    print("Sueecssfully delete the infomation!")
                    break
            else:
                print("Error!The input should be a number!")
                continue
    elif sql_dict["query_action"] == "insert":

        while True:
            with open("../config/id.json", 'r') as load_f:
                staff_id = json.load(load_f)
                #实现staff_id 自增
                new_id = int(staff_id["staff_id"]) + 1
            phone_list = phone_check(field_all_names_list, staff_info_list, unique_key)
            insert_value = sql_dict["query_target"]
            #判断是否和 phone 这个唯一键冲突
            if insert_value[2] in phone_list:
                print("The phone number must bu unique!")
                query = input(">>>")
                sql_dict = query_function(query)
            else:
                insert_value.insert(0,str(new_id))
                new_line = ",".join(insert_value)
                with open("../config/table.txt",'a',encoding="utf-8") as write_f:
                    write_f.write("\n"+new_line)
                print("Query OK,1 row affected.")
                get_id("../config/table.txt", "../config/id.json")
                break
    elif sql_dict["query_action"] == "update":
        phone_list = phone_check(field_all_names_list, staff_info_list, unique_key)
        #print(sql_dict["query_target_value"])
        if sql_dict["query_target_value"] in phone_list:
            print("Sorry!The phone number muset be unique.")
            continue
        else:
            if sql_dict["query_object"] not in field_all_names_list \
                    or sql_dict["query_target"] not in field_all_names_list:
                print("No such field name in staff_table!")
                continue
            else:
                sql_target = sql_dict["query_target"]
                sql_target_index = field_all_names_list.index(sql_target)
                sql_object = sql_dict["query_object"]
                sql_object_index = field_all_names_list.index(sql_object)
                if sql_dict["query_object_matching"] == "=":
                    for i in range(len(staff_info_list)):
                        if staff_info_list[i][sql_object_index] == sql_dict["query_object_value"]:
                            staff_info_list[i][sql_target_index] = sql_dict["query_target_value"]
                            new_content = ",".join(staff_info_list[i])
                            update_write_in_file("../config/table.txt", i, new_content)
                            query_count += 1

                elif sql_dict["query_object_matching"] == ">":
                    for i in range(len(staff_info_list)):
                        if staff_info_list[i][sql_object_index] > sql_dict["query_object_value"]:
                            staff_info_list[i][sql_target_index] = sql_dict["query_target_value"]
                            new_content = ",".join(staff_info_list[i])
                            update_write_in_file("../config/table.txt", i, new_content)
                            query_count += 1

                elif sql_dict["query_object_matching"] == "<":
                    for i in range(len(staff_info_list)):
                        if staff_info_list[i][sql_object_index] < sql_dict["query_object_value"]:
                            staff_info_list[i][sql_target_index] = sql_dict["query_target_value"]
                            new_content = ",".join(staff_info_list[i])
                            update_write_in_file("../config/table.txt", i, new_content)
                            query_count += 1

                elif sql_dict["query_object_matching"] == "like":
                    for i in range(len(staff_info_list)):
                        if sql_dict["query_object_value"] in staff_info_list[i][sql_object_index]:
                            staff_info_list[i][sql_target_index] = sql_dict["query_target_value"]
                            new_content = ",".join(staff_info_list[i])
                            update_write_in_file("../config/table.txt", i, new_content)
                            query_count += 1
                else:
                    print("Error!{} is wrong".format(sql_dict["query_object_matching"]))

                print("Query OK,{} row affected.".format(query_count))
    elif sql_dict["query_action"] == "exit":
        exit()
    else:
        print("Sorry!{} no such function.".format(sql_dict["query_action"]))