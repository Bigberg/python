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
            print(account_new_name)
            file_path = os.path.join(self.ftp_dir, account_new_name, file_new_name)
            print('start receiving...')
            fw = open(file_path, 'wb')
            r_data = conn.recv(1024)
            fw.write(r_data)
            fw.close()
            print('job finished...')

        ftp_server.close()

    def server_download(self):
        # 声明协议类型
        ftp_server = socket.socket()
        ftp_server.bind((self.host, self.port))
        ftp_server.listen()
        conn, address = ftp_server.accept()
        user_info = conn.recv(1024)
        print(user_info.decode())
        ftp_server.close()

if __name__ == '__main__':
    server = FtpServer('localhost', 8888)
    server.server_download()
