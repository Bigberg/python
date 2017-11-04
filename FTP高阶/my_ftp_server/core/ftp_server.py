# -*- coding: UTF-8 -*-
import socketserver
import os
import json
import configparser
from my_ftp_server.modules import get_all_user_info

BasePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = configparser.ConfigParser()
config.read("{}/config/setting.ini".format(BasePath), encoding='utf-8')


class MyTCPHandler(socketserver.BaseRequestHandler):

    # 数据库位置
    db_path = os.sep.join([BasePath, 'db'])

    def put(self, *args):
        # 接受客户端文件
        cmd_dict = args[0]
        filename = cmd_dict['filename']
        file_size = cmd_dict['size']
        if os.path.isfile(filename):
            # 重命名
            f = open(filename + '.new', 'wb')
        else:
            f = open(filename, 'wb')

        self.request.send(b'200 ok')
        received_size = 0
        while received_size < file_size:
            r_data = self.request.recv(1024)
            f.write(r_data)
            received_size += len(r_data)

    def authenticate(self, *args):
        # 接受客户端发送的登入信息
        auth_dict = args[0]
        acc_name = auth_dict['username']
        # print(acc_name)
        acc_password = auth_dict['password']
        # print(acc_password)
        # 获取所有用户信息

        users_info_list = get_all_user_info.get_user_info(self.db_path)
        # print(users_info_list)
        names_list = []
        for i in range(len(users_info_list)):
            names_list.append(users_info_list[i]['username'])
        # print(names_list)
        if acc_name in names_list:
            user_index = names_list.index(acc_name)
            password = users_info_list[user_index]['password']
            if acc_password == password:
                self.request.send(b'ok')
            else:
                self.request.send(b'password is wrong')
        else:
            print('user not exits')
            self.request.send(b'user not exits')

    def handle(self):
        while True:
            # self.request is the TCP socket connected to the client
            self.data = self.request.recv(1024).strip()
            # print("{} wrote:".format(self.client_address[0]))
            # print(self.data)
            cmd_dict = json.loads(self.data.decode())
            action = cmd_dict['action']
            if hasattr(self, action):
                func = getattr(self, action)
                func(cmd_dict)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
