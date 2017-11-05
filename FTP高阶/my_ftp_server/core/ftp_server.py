# -*- coding: UTF-8 -*-
import socketserver
import os
import hashlib
import json
import configparser
from my_ftp_server.modules import get_all_user_info
from my_ftp_server.modules import calculate_size

BasePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = configparser.ConfigParser()
config.read("{}/config/setting.ini".format(BasePath), encoding='utf-8')


class MyTCPHandler(socketserver.BaseRequestHandler):

    # 数据库位置
    db_path = os.sep.join([BasePath, 'db'])

    # 登入成功记录值
    auth_info = {
        'username': None,
        'user_home': None,
        'authentication': False
    }
    ftp_home = config.get('DEFAULT', 'ftp_dir')

    def put(self, *args):
        # 接受客户端文件
        cmd_dict = args[0]
        filename = cmd_dict['filename']
        dir_path = cmd_dict['work_dir']
        file_size = cmd_dict['size']
        # 验证服务端空间是否足够
        used_size = calculate_size.get_used_size(self.auth_info['user_home'])
        free_size = calculate_size.free_space(os.sep.join(
            [self.db_path, '{}.dat'.format(self.auth_info['username'])]), used_size)
        # md5
        m_server_put = hashlib.md5()
        if free_size >= file_size:
            self.request.send(b'200')
            if os.path.isfile(os.sep.join([dir_path, filename])):
                # 如果有相同名称的文件，重命名
                f = open(os.sep.join([dir_path, filename]) + '.new', 'wb')
            else:
                f = open(os.sep.join([dir_path, filename]), 'wb')
            received_size = 0
            while received_size < file_size:
                size = 1024
                if file_size - received_size > 1024:
                    r_data = self.request.recv(size)
                else:
                    r_data = self.request.recv(file_size - received_size)
                m_server_put.update(r_data)
                f.write(r_data)
                received_size += len(r_data)
            else:
                # md5 验证
                client_md5 = self.request.recv(1024)
                if m_server_put.hexdigest() == client_md5.decode():
                    self.request.send(b'200')
                    f.close()
                else:
                    # 600 md5 not match
                    self.request.send(b'600')
                    os.remove(os.sep.join([self.auth_info['user_home'], filename]))

        else:
            # 500 服务端空间不够
            self.request.send(b'500')

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
        send_msg = {
            'status': None,
            'work_dir': None
        }
        if acc_name in names_list:
            user_index = names_list.index(acc_name)
            password = users_info_list[user_index]['password']
            if acc_password == password:
                send_msg['status'] = 'ok'
                send_msg['work_dir'] = os.sep.join([self.ftp_home, acc_name])
                # 登入后用户相关信息保存到auth_info
                self.auth_info['username'] = acc_name
                self.auth_info['user_home'] = send_msg['work_dir']
                self.auth_info['authentication'] = True
            else:
                send_msg['status'] = 'password is failure'
        else:
            send_msg['status'] = 'user not exits'
        # 回复信息
        self.request.send(json.dumps(send_msg).encode())

    def ls(self, *args):
        # 显示目录内容
        dir_name = args[0]['word_path']
        # print(dir_name)
        # 判断目录是否存在
        if os.path.exists(dir_name):
            dir_list = os.listdir(dir_name)
            ls_msg = {
                'dir_info': dir_list,
                'status': '200'
            }
        else:
            ls_msg = {
                'dir_info': 'directory not exits',
                'status': '700'
            }
        self.request.send(json.dumps(ls_msg).encode('utf-8'))

    def cd(self, *args):
        # 切换目录
        dirname = args[0]['workspace']
        if os.path.exists(dirname):
            # 表示目录存在, 且在家目录中
            if len(dirname.split(os.sep)) >= 4:
                self.request.send(b'200')
            else:
                self.request.send(b'403')
        else:
            self.request.send(b'700')

    def get(self, *args):
        # 下载文件
        filename = args[0]['filename']
        dirname = args[0]['work_dir']
        # 判断文件是否存在
        file_path = os.sep.join([dirname, filename])
        if os.path.isfile(file_path):
            # 获取文件大小
            file_size = os.stat(file_path).st_size
            # 发送给客户端文件大小
            send_msg = {
                'status': '200',
                'file_size': file_size
            }
            self.request.send(json.dumps(send_msg).encode())
            recv_data = self.request.recv(1024)
            recv_dict = json.loads(recv_data.decode())
            # seek_location == 0 新下载不续传，否则 续传文件
            seek_location = recv_dict['seek_location']
            try:
                f = open(file_path, 'rb')
                f.seek(seek_location)
                for line in f:
                    self.request.send(line)
                else:
                    f.close()
            except KeyboardInterrupt as e:
                print(e)
        else:
            self.request.send(b'800')

    def mkdir(self, *args):
        make_dict = args[0]
        dir_path = make_dict['dir_path']
        os.makedirs(dir_path)
        if os.path.exists(dir_path):
            self.request.send(b'200')
        else:
            self.request.send(b'700')

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
