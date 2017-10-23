# -*- coding: UTF-8 -*-
# from module.staff_list import file_read
#
# staff_table = file_read("../config/table.txt")
# #print(staff_table)
# print("-".center(61,'-'))
# print("|{}|\t\t{}\t| {}|   {}   |{}\t|{}|" \
# 	  .format("staff_id","name","age","phone","dept","enroll_date"))
# for i in range(len(staff_table)):
# 	item_list=staff_table[i].split(',')
# 	print("| {}\t\t |   {} \t| {} |{}|{}\t|{}\t|" \
# 		  .format(item_list[0],item_list[1],item_list[2], \
# 				  item_list[3],item_list[4],item_list[5]))
# print("-".center(61,'-'))
#
# def test(list_name1,*args):
# 	print(list_name1)
# 	print(args)
#
# a = [1,2,3,4]
# b = [5,6,7,8]
#
# test(a,*b)



query_dict = {}
query='''name, age from staff_table where age = 22'''
print(query)
query_list = query.split("=")
print(query_list)
target = query_list[1].strip()
print(type(target))
target_value = target[1:-1]
print(target_value)

# query_list = query.strip().split("where")
# target_list = query_list[1].strip().split(" ")
# print(target_list)
# target_final_list = []
# for i in target_list:
# 	target_final_list.append(i.strip())
# print(target_final_list)
# print(query_list)
# query_dict["query_target"]=query_list[0]
# print(query_dict)
# print(query)
# capital_list = []
# for i in range(len(query)):
# 	if query[i].isspace():
# 		break
# 	else:
# 		capital_list.append(query[i])
# capital_string ="".join(capital_list)
# print(capital_string)