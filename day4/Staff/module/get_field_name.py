# -*- coding: UTF-8 -*-
'''
   get the query field name(字段名)
'''
def field_name_list(filename,name_list):
    from module.staff_list import staff_list_get
    staff_list = staff_list_get(filename)
    if name_list[0] == '*':
        field_get_name=staff_list[0].split(",")
    else:
        field_get_name=name_list[1].split(",")
    return field_get_name

# query_list = ['select', 'staff_id,name,age', 'from', 'staff_table', 'where', 'staff_id', '=', "'1'"]
# field_name = field_name_list("../config/table.txt",query_list)
# print(field_name)