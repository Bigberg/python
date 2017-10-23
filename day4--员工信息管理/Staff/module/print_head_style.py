# -*- coding: UTF-8 -*-
'''
   print format of query result,make it looks like mysql output
   + - - - - - - -  + - - - - - - -  + - - - - - - - +
  |     name       |      age       |     phone     |
  + - - - - - - -  + - - - - - - -  + - - - - - - - +
'''
from module.print_css import style1
from module.print_css import style4
from module.print_css import style5
from module.print_css import style6
def head_style(length,list_name):
    if length == 1:
        style1()
        style4(list_name,length-1)
        style1()
    else:
        style5(length)
        style6(list_name,length)
        style5(length)