# -*- coding: UTF-8 -*-

import selectors
import socket
import os
import time
import json
import configparser
import sys
from my_ftp_server.modules import get_all_user_info
from my_ftp_server.modules import calculate_size
BasePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BasePath)
sys.path.insert(0, BasePath)
# print(sys.path)

config = configparser.ConfigParser()
config.read("{}/config/setting.ini".format(BasePath), encoding='utf-8')


class SelectorsServer(object):
    # 数据库位置
    db_path = os.sep.join([BasePath, 'db'])

    # 登入成功记录值
    auth_info = {
        'username': None,
        'user_home': None,
        'authentication': False
    }
    ftp_home = config.get('DEFAULT', 'ftp_dir')

    def __init__(self, sel_obj):
        self.sel_obj = sel_obj

    def accept(self, sock, mask):
        '''

        :param sock: 文件句柄
        :param mask: 事件类型
        :return:
        '''
        conn, addr = sock.accept()
        conn.setblocking(False)
        self.sel_obj.register(conn, selectors.EVENT_READ, self.read)

    def read(self, conn, mask):
        '''

        :param conn: 连接对象
        :param mask:
        :return:
        '''
        try:
            data = conn.recv(1024).strip()
            if data:
                cmd_dict = json.loads(data.decode())
                action = cmd_dict['action']
                if hasattr(self, action):
                    func = getattr(self, action)
                    func(conn, cmd_dict)
                else:
                    print('no such function.')
        except ConnectionResetError:
            print('断开连接', conn)
            self.sel_obj.unregister(conn)
            conn.close()

    def authenticate(self, *args):
        conn = args[0]
        # print(args)
        # 接受客户端发送的登入信息
        auth_dict = args[1]
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
        conn.send(json.dumps(send_msg).encode())

    def put(self, *args):
        conn = args[0]
        # 接受客户端文件
        cmd_dict = args[1]
        filename = cmd_dict['filename']
        dir_path = cmd_dict['work_dir']
        file_size = cmd_dict['size']
        # 验证服务端空间是否足够
        used_size = calculate_size.get_used_size(self.auth_info['user_home'])
        free_size = calculate_size.free_space(os.sep.join(
            [self.db_path, '{}.dat'.format(self.auth_info['username'])]), used_size)

        if free_size >= file_size:
            conn.send(b'200')
            if os.path.isfile(os.sep.join([dir_path, filename])):
                # 如果有相同名称的文件，重命名
                f = open(os.sep.join([dir_path, filename]) + '.new', 'wb')
            else:
                f = open(os.sep.join([dir_path, filename]), 'wb')
            received_size = 0
            while received_size < file_size:
                size = 1024
                if file_size - received_size > 1024:
                    try:
                        r_data = conn.recv(size)
                    except BlockingIOError:

                        continue
                else:
                    try:
                        r_data = conn.recv(file_size - received_size)
                    except BlockingIOError:

                        continue
                f.write(r_data)
                f.flush()
                received_size += len(r_data)
            else:

                f.close()

        else:
            # 500 服务端空间不够
            conn.send(b'500')

    def get(self, *args):
        conn = args[0]
        # 下载文件
        filename = args[1]['filename']
        dirname = args[1]['work_dir']
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
            conn.send(json.dumps(send_msg).encode())
            recv_data = ''
            while not recv_data:
                try:
                    recv_data = conn.recv(1024)
                except BlockingIOError:
                    time.sleep(0)
                    # continue
            recv_dict = json.loads(recv_data.decode())
            # seek_location == 0 新下载不续传，否则 续传文件
            seek_location = recv_dict['seek_location']
            try:
                f = open(file_path, 'rb')
                f.seek(seek_location)
                for line in f:
                    conn.send(line)
                else:
                    f.close()
            except KeyboardInterrupt as e:
                print(e)
        else:
            conn.send(b'800')

    def ls(self, *args):
        conn = args[0]
        # 显示目录内容
        dir_name = args[1]['word_path']
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
        conn.send(json.dumps(ls_msg).encode('utf-8'))

    def cd(self, *args):
        conn = args[0]
        # 切换目录
        dirname = args[1]['workspace']
        if os.path.exists(dirname):
            # 表示目录存在, 且在家目录中
            if len(dirname.split(os.sep)) >= 4:
                conn.send(b'200')
            else:
                conn.send(b'403')
        else:
            conn.send(b'700')

    def mkdir(self, *args):
        conn = args[0]
        # 创建文件夹
        make_dict = args[1]
        dir_path = make_dict['dir_path']
        os.makedirs(dir_path)
        if os.path.exists(dir_path):
            conn.send(b'200')
        else:
            conn.send(b'700')


def run():

    sel = selectors.DefaultSelector()
    server = socket.socket()
    server.bind(('localhost', 9999))
    server.listen()
    server.setblocking(False)
    sel_obj = SelectorsServer(sel)
    sel.register(server, selectors.EVENT_READ, sel_obj.accept)
    while True:
        events = sel.select()
        print(events)
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)