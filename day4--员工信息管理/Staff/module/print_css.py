# -*- coding: UTF-8 -*-
'''
   create the style of output,make it look like mysql
   + - - - - - - -  + - - - - - - -  + - - - - - - - +
   |     name       |      age       |     phone     |
  + - - - - - - -  + - - - - - - -  + - - - - - - - +

'''
def style1():
    print("+ - - - - - - - +")

def style2():
    print("+ - - - - - - - ", end=" ")

def style3(list_name,index):
    print("|{: ^15}".format(list_name[index]), end=" ")

def style4(list_name,index):
    print("|{: ^15}|".format(list_name[index]))

'''
  style5 实现的功能
+ - - - - - - -  + - - - - - - -  + - - - - - - -  +
'''
def style5(length):
    for i in range(length):
        style2()
        if i == length - 2:
            style1()
            break

'''
  style6 实现功能:按照mysql的格式打印数据信息
  |       1        |    Alex Li     |      22        |  13651054688   |      IT        |  2013-04-01   |
'''
def style6(list_name,length):
    for i in range(length):
        style3(list_name, i)
        if i == length - 2:
            style4(list_name, length - 1)
            break
