# -*- coding: UTF-8 -*-
# import sys
# import hashlib
# a = '123123'
#
# m = hashlib.md5()
# m.update(b'a')
# print(m.hexdigest())

import os

dir_info = os.listdir(r'G:\ftp\home\bigberg')
print(dir_info)


KeyboardInterrupt

#
# #
# # def view_bar(num, mes):
#     """
#     进度条方法
#     :param num: 百分比数字
#     :param mes: 输出信息
#     :return:
#     """
# #     rate_num = num
# #     print(rate_num)
# #     number = int(rate_num / 4)
# #     print(number)
# #     hashes = '>' * number
# #     spaces = ' ' * (25 - number)
# #     r = "\r\033[31;0m%s\033[0m：[%s%s]\033[32;0m%d%%\033[0m" % (mes, hashes, spaces, rate_num,)
# #     sys.stdout.write(r)
# #     sys.stdout.flush()
# #
# # if __name__ == '__main__':
# #     view_bar(100, '上传进度')
import sys, time

# os.walk()的使用
# import os
#
#
# # 枚举dirPath目录下的所有文件
#
# def main(dirname):
#     # begin
#     for root, dirs, files in os.walk(dirname):
#         print(root)
#         print(dirs)
#         print(files)
#         for dir in dirs:
#             print(os.path.join(root, dir))
#         for file in files:
#             print(os.path.join(root, file))
#         print('----------------')
#
#
# if __name__ == '__main__':
#     main(r'G:\ftp\home\bigberg')
