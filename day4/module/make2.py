# -*- coding: UTF-8 -*-
'''
   字典内容：
   {'query_action': 'select', 'query_object_value': 'Alex Li', 'query_matching': '=', 'matching_object': 'name', 'query_condition': 'where', 'query_target': ['name', 'age']}
'''
#query="select name,age from staff_table where name = 'Alex Li'"
#query="select * from staff_table"
#query = '''select name,phone,age from staff_table where enroll_date like "2013"'''
#query = '''insert into staff_table (name,age,phone,dpet,enroll_date) values ('Li Si',22,'13423456789','2014-09-08')'''
#query = '''update staff_table set name = "Alex Li" where name = "Zhang San"'''

def query_function(query):
    #将 sql语句拆分进字典
    query_dict = {}
    #获取第一个单词，判断检索行为(诸如 select ,update)
    capital_list = []
    for i in range(len(query)):
        if query[i].isspace():
            length = len(capital_list)
            query=query[length:].strip()
            #print(query)
            break
        else:
            capital_list.append(query[i])
    capital_string = "".join(capital_list)
    #将值添加进字典中
    query_dict["query_action"]=capital_string
    #print(query_dict)
    if capital_string == "select":
        if "from" in query:
            query_list = query.strip().split("from")
            target_list = query_list[0].split(",")
            #处理输入中有空格,如 select name, age , phone
            target_final_list = []
            for i in target_list:
                target_final_list.append(i.strip())
                query_dict["query_target"] = target_final_list
            #print(query_dict)
            if "where" in query:
                query_dict["query_condition"] = "where"
                query_list2 = query.strip().split("where")
                target_list2 = query_list2[1].strip().split(" ")
                #print(target_list2)
                #匹配对象
                query_dict["matching_object"] = target_list2[0]
                #匹配符号
                query_dict["query_matching"] = target_list2[1]
                #print(target_list2[1])
                #去掉要匹配值的引号,如果是 数值 则不用
                query_list3 = query.strip().split(target_list2[1])
                object_value = query_list3[1].strip()
                if object_value.isnumeric():
                    query_dict["query_object_value"] = object_value
                else:
                    object_value_other = object_value[1:-1]
                    query_dict["query_object_value"] = object_value_other
                #print(query_dict)
            else:
                #没有where条件,全局匹配
                query_dict["query_condition"] = ""
                #print(query_dict)
        else:
            print('Error!Check the query about \033[31;1m from \033[0m')
            exit()
    elif capital_string == "delete":
        query_dict["query_target"]=""
    elif capital_string == "exit":
        query_dict["query_target"]=""
    elif capital_string == "insert":
        #去 括号和 引号
        query_target1 = query.split("values")[-1]
        query_target2 = query_target1.split("(")[1]
        query_target3 = query_target2.split(")")[0]
        query_target_list = query_target3.split(",")
        query_target_final_list = []
        for i in range(len(query_target_list)):
            if query_target_list[i].isnumeric():
                query_target_final_list.append(query_target_list[i])
            else:
                query_target_final_list.append(query_target_list[i][1:-1])

        query_dict["query_target"] = query_target_final_list
    elif capital_string == "update":
        query1 = query.strip().split('set')[1]
        #print(query1)
        target_ls = query1.split("where")[0].strip().split(" ")
        #print(target_ls)
        #获取匹配值和要更新的值，并去除引号
        object_ls = query.split("where")[1].strip().split(" ")
        query_dict["query_target"] = target_ls[0]
        query_dict["query_target_matching"] = target_ls[1]
        query_dict["query_target_value"] = query.split("where")[0].strip().split(target_ls[1])[1].strip()[1:-1]

        query_dict["query_object"] = object_ls[0]
        query_dict["query_object_matching"] = object_ls[1]
        query_dict["query_object_value"] = query.split("where")[1].strip().split(object_ls[1])[1].strip()[1:-1]
    else:
        print("Error!NO such function!")
        exit()
    return query_dict
#print(query_function(query))


