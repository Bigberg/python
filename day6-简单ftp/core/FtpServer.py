# -*- coding: UTF-8 -*-
import struct
import socket
import configparser
import os

# 路径
BasePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = configparser.ConfigParser()
config.read("{}/config/setting.ini".format(BasePath), encoding='utf-8')


class FtpServer(object):
    ftp_dir = config.get('DEFAULT', 'FtpHomeDir')

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def server_upload(self):
        # 声明协议类型
        ftp_server = socket.socket()
        ftp_server.bind((self.host, self.port))
        ftp_server.listen()
        conn, address = ftp_server.accept()
        file_info = struct.calcsize('128s128s')

        buf = conn.recv(file_info)

        if buf:
            file_name, account_name = struct.unpack('128s128s', buf)
            # 使用strip()删除打包时附加的多余空字符
            file_new_name = file_name.decode().strip('\00')
            account_new_name = account_name.decode().strip('\00')
            # print(account_new_name)
            file_path = os.path.join(self.ftp_dir, account_new_name, file_new_name)
            print('开始接收文件...')
            fw = open(file_path, 'wb')
            r_data = conn.recv(1024)
            fw.write(r_data)
            fw.close()
            print('文件接收完成...')

        ftp_server.close()

    def server_download(self):
        # 声明协议类型
        ftp_server = socket.socket()
        ftp_server.bind((self.host, self.port))
        ftp_server.listen()
        conn, address = ftp_server.accept()
        user_info = conn.recv(1024)
        # print(user_info.decode())
        # 列出用户目录下的文件
        file_list = os.listdir(os.path.join(self.ftp_dir, user_info.decode()))
        # 把文件名都传到客户端显示
        file_names = ''
        for i in file_list:
            file_names += i+'\n'
        conn.send(file_names.encode('utf-8'))
        # ftp_server.send(file_info)
        # 传输下载的文件
        file_download_name = conn.recv(1024)
        file_path = os.path.join(self.ftp_dir, user_info.decode(), file_download_name.decode())
        # print(file_path)
        f_down = open(file_path, 'rb')
        file_data = f_down.read(1024)
        conn.send(file_data)
        ftp_server.close()

if __name__ == '__main__':
    server = FtpServer('localhost', 8888)
    # server.server_upload()
    server.server_download()

