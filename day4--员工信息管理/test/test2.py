# -*- coding: UTF-8 -*-
from module.make_query_dict import query_actions
from module.print_css import style1
from module.print_css import style3
from module.print_css import style4
from module.print_css import style5
from module.print_css import style6
from module.print_head_style import head_style

from Staff.module.staff_list import staff_list_get

# staff_table 包含字段
staff_table = staff_list_get("../config/table.txt")
print(staff_table)
field_all_names_list = staff_table[0].split(",")
print(field_all_names_list)
#print(field_all_names_list.index("age"))
# staff_info_list 没有字段
staff_info_list = []
for i in range(1, len(staff_table)):
	info_list = staff_table[i].split(",")
	staff_info_list.append(info_list)

# print(staff_info_list)

#打印匹配条数
query_count = 0

query = input(">>>")
#引用query_action函数，将 sql语句 转换为 字典形式
sql_dict = query_actions(query)
if  sql_dict["query_action"]== 'select':
	#没有where时,打印的是全部信息
	field_name = sql_dict["query_target"]
	# print(field_name == ['*'])
	if field_name[0] == "*":
		field_name = field_all_names_list

	length = len(field_name)
	head_style(length, field_name)
	if sql_dict["query_condition"] == "":
		if sql_dict["query_target"] == "*":
			for i in range(len(staff_info_list)):
				style6(staff_info_list[i],len(staff_info_list[i]))
			style5(length)
			print("{} rows in set".format(len(staff_info_list)))
		else:
			# 将被检索的字段名在table中的索引找出来
			# 添加索引是为了在select 字段名时,可以不按照顺序进行
			index_list = []
			for i in field_name:
				index_list.append(field_all_names_list.index(i))
			if length == 1:
				for i in range(len(staff_info_list)):
					#print("|{:^15}|".format(staff_info_list[i][index_list[0]]))
					style4(staff_info_list[i],index_list[0])

				style1()
				print("{} rows in set".format(len(staff_info_list)))
			else:
				for i in range(len(staff_info_list)):
					for j in range(len(index_list)):
						#print("|{:^15}".format(staff_info_list[i][index_list[j]]), end=" ")
						style3(staff_info_list[i],index_list[j])
						if j == len(index_list) - 2:
							#print("|{:^15}|".format(staff_info_list[i][index_list[len(index_list) - 1]]))
							style4(staff_info_list[i],index_list[len(index_list) - 1])
							break

				style5(length)
				print("{} rows in set".format(len(staff_info_list)))

	else:
		if sql_dict["query_matching"] == "=":
			target_object = sql_dict["matching_object"]
			#print(type(target_object))
			target_index = field_all_names_list.index(target_object)
			for i in range(len(staff_info_list)):
				if sql_dict["query_object_value"] == staff_info_list[i][target_index]:
					for j in range(len(staff_info_list[i])):
						style3(staff_info_list[i],j)
						if j == len(staff_info_list[i])-2:
							style4(staff_info_list[i],len(staff_info_list[i])-1)
							break
					query_count += 1
			style5(length)
			print("{} rows in set".format(query_count))

		else:
			pass


else:
	pass