# -*- coding: UTF-8 -*-

# staff_table = ['staff_id,name,age,phone,dept,enroll_date', '1,Alex Li,22,13651054688,IT,2013-04-01', '2,Jack Wang,30,13323457899,HR,2015-05-03', '3,Rain Liu,25,13887962376,Sales,2016-04-22', '4,Mack Cao,40,13567843245,HR,2009-03-01']
# field_name=staff_table[0].split(",")

from module.print_head_style import head_style

from Staff.module.get_field_name import field_name_list

query_list = ['select', 'name,age,phone', 'from', 'staff_table', 'where', 'staff_id', '=', "'1'"]
field_name = field_name_list("../config/table.txt",query_list)
#print(type(query_list[-1]))
#print(field_name)
length=len(field_name)
#print(length)
head_style(length,field_name)
# if length == 1:
# 	print("+ - - - - - - - +")
# 	print("|{: ^15}|".format(field_name[length-1]))
# 	print("+ - - - - - - - +")
# else:
# 	for i in range(length):
# 		print("+ - - - - - - - ",end=" ")
# 		if i == length-2:
# 			print("+ - - - - - - - +")
# 			break
# 	for i in range(length):
# 		print("|{: ^15}".format(field_name[i]),end=" ")
# 		if i == length-2:
# 			print("|{: ^15}|".format(field_name[length-1]))
# 			break
# 	for i in range(length):
# 		print("+ - - - - - - - ",end=" ")
# 		if i == length-2:
# 			print("+ - - - - - - - +")
# 			break