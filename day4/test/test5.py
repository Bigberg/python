# -*- coding: UTF-8 -*-

# query_list = ['select', 'name', 'from', 'staff_table', 'where', 'staff_id', '=', "'1'"]
# print(query_list[1])
# field_name = query_list[1].split(",")
# print(field_name)
# field_name = ["name","age","enroll_date"]
# staff_table = ['staff_id,name,age,phone,dept,enroll_date', '1,Alex Li,22,13651054688,IT,2013-04-01', '2,Jack Wang,30,13323457899,HR,2015-05-03', '3,Rain Liu,25,13887962376,Sales,2016-04-22', '4,Mack Cao,40,13567843245,HR,2009-03-01']
# staff_list = staff_table[0].split(",")
# #print(staff_list)
# index_list = []
# for i in field_name:
# 	index_list.append(staff_list.index(i))
#
# print(index_list)
# a = '22'
# print(a.isnumeric())

'''
staff_id,name,age,phone,dept,enroll_date
1,Alex Li,22,13651054688,IT,2013-04-01
2,Jack Wang,30,13323457899,HR,2015-05-03
3,Rain Liu,25,13887962376,Sales,2016-04-22
4,Mack Cao,40,13567843245,HR,2009-03-01

# '''
# #
# with open("../config/table.txt", 'r', encoding="utf-8") as read_file:
# 	lines = read_file.readlines()
# for i in range(len(lines)):
# 	print(i,lines[i])
# # for line in lines:
# # 	print(line)
with open("../config/staff_info.txt",'w') as f:
	f.write("1")
