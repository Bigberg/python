# -*- coding: UTF-8 -*-
import socket
import os
import struct
from core import user
from modules import login_required
# authentication_data = user.account_data


# 定义一个FtpClien类
class FtpClient(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port

    # @login_required.login_required
    def client_upload(self, auth_data):

        # 声明协议类型,同时生成socket对象
        ftp_client = socket.socket()
        ftp_client.connect((self.host, self.port))
        # 切换文件目录路径
        print("输入文件目录路径")
        pwd = input(">>:").strip()
        while not os.path.exists(pwd):
            print("改目录不存在，请重新输入")
            pwd = input(">>:").strip()
        else:
            # 列出文件名称
            files_list = os.listdir('{}'.format(pwd))
            for i in files_list:
                print(i)

            file_name = input('输入上传的文件名:').strip()
            file_path = os.path.join(pwd, file_name)
            login_name = auth_data.get('account_name')
            if os.path.isfile(file_path):
                file_info = struct.calcsize('128s128s')  # 定义打包规则
                f_head = struct.pack('128s128s', file_name.encode('utf-8'), login_name.encode('utf-8'))
                ftp_client.send(f_head)
                fo = open(file_path, 'rb')
                while True:
                    file_data = fo.read(1024)
                    if not file_data:
                        break
                    ftp_client.send(file_data)
                fo.close()
                # 上传文件
                ftp_client.send(file_data)
            ftp_client.close()
            print('正在上传...')
            print('上传完成...')

    # 下载
    # @login_required.login_required
    def client_download(self, auth_data):
        # 声明协议类型,同时生成socket对象
        ftp_client = socket.socket()
        ftp_client.connect((self.host, self.port))
        login_name = auth_data.get('account_name')
        # print(login_name)
        ftp_client.send(login_name.encode('utf-8'))
        file_info = ftp_client.recv(1024)
        print('{}目录下现在的文件：'.format(login_name))
        print(file_info.decode())
        print("\n")
        file_download_name = input('输入你想下载的文件名称:').strip()
        # 判断文件是否存在
        file_list = file_info.decode().split('\n')
        while file_download_name not in file_list:
            print('该文件不存在,请确认后再输入')
            file_download_name = input('输入你想下载的文件名称:').strip()
        else:
            # print(file_download_name)
            ftp_client.send(file_download_name.encode('utf-8'))
            store_dir = input('输入你想存储文件的目录:')
            try:
                if not os.path.exists(store_dir):
                    os.makedirs(store_dir)
            except OSError as e:
                print('输入有误:{}', e)
            receive_data = ftp_client.recv(1024)
            file_download_path = os.path.join(store_dir, file_download_name)
            f_down_write = open(file_download_path, 'wb')
            f_down_write.write(receive_data)
        ftp_client.close()
        print('下载完成')

# client.close()
# if __name__ == '__main__':
#     u = user.User('db')
#     u.sign_in(authentication_data)
#     client = FtpClient('localhost', 8888)
#     # client.client_upload(authentication_data)
#     client.client_download(authentication_data)
