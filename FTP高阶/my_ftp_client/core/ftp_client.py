# -*- coding: UTF-8 -*-
import socket
import os
import json
import hashlib
import sys


class FtpClient(object):

    # 定义工作目录
    work_path = ''
    # print(work_path)

    def __init__(self):
        self.client = socket.socket()
        self.authentication = False  # 判断是否登入

    def help(self):   # 打印指令信息
        msg = '''
    ls  -  列出该目录下所有文件和文件夹
    pwd -  显示当前工作目录
    cd  -  cd .  当前工作目录
           cd .. 上一级工作目录
           cd dirname  切换到当前工作目录下的dirname目录

    get -  filename  下载文件
    put -  G:/ftp/home/***.txt  上传文件

    mkdir - mkdir dirname 创建目录
        '''
        print(msg)

    def connect(self, ip, port):
        self.client.connect((ip, port))

    def interactive(self):
        # 交换模块
        while True:
            cmd = input("[root@ftp_server %s]$:" % (self.work_path.split(os.sep)[-1])).strip()
            if len(cmd) == 0:
                continue
            cmd_str = cmd.split()[0]
            # 使用反射
            if hasattr(self, 'cmd_%s' % cmd_str):
                func = getattr(self, 'cmd_%s' % cmd_str)
                func(cmd)  # 执行命令

            else:
                self.help()

    def authenticate(self):
        # 登入认证
        while True:
            account_name = input('请输入用户名:').strip()
            account_passwd = input('请输入密码:').strip()
            account_m = hashlib.md5()
            account_m.update(account_passwd.encode('utf-8'))
            passwd_md5 = account_m.hexdigest()
            # print(passwd_md5)
            acc_msg = {
                'username': account_name,
                'password': passwd_md5,
                'action': 'authenticate'
            }
            # print(acc_msg)
            # 发送登入信息给服务端确认
            self.client.send(json.dumps(acc_msg).encode())
            # 接受服务端返回的认证结果
            acc_response = self.client.recv(1024).strip()
            recv_msg = json.loads(acc_response.decode())
            if recv_msg['status'] == 'ok':
                print('登入成功')
                self.authentication = True
                self.work_path = recv_msg['work_dir']
                self.interactive()
            else:
                print(recv_msg['status'])
                continue

    def cmd_put(self, *args):
        # 上传文件,文件路径为全路径，如： G:\test\test.txt
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            file_path = cmd_split[1]
            path_list = file_path.split(os.sep)
            # 判断文件目录是否存在
            dir_path = os.sep.join(path_list[:-1])
            if os.path.exists(dir_path):
                filename = path_list[-1]
                if os.path.isfile(file_path):
                    file_size = os.stat(file_path).st_size
                    # 将文件名、大小等信息传给服务端，为了一些其他判断，可以预先使用json格式
                    msg_dict = {
                        'filename': filename,
                        'size': file_size,
                        'work_dir': self.work_path,
                        'overridden': False,
                        'action': 'put'
                    }
                    self.client.send(json.dumps(msg_dict).encode())
                    # 防止粘包，等服务器确认
                    server_response = self.client.recv(1024).strip()
                    # print(server_response.decode())
                    # 如果返回的值是200,表示空间足够，500表示空间不足
                    if server_response.decode() == '200':
                        # 进度条标识
                        bar = '>'
                        send_size = 0
                        # md5
                        m_put = hashlib.md5()
                        f = open(file_path, 'rb')
                        for line in f:
                            self.client.send(line)
                            # md5
                            m_put.update(line)
                            # 上传进度条
                            send_size += len(line)
                            percent = int(float(send_size) / float(file_size) * 100)
                            # print(percent)
                            sys.stdout.write('\r' + '[' + bar * percent +
                                             ' ' * (100 - percent) + ']' + str(percent) + '%')
                            sys.stdout.flush()
                            if percent == 100:
                                sys.stdout.write('\n')

                        else:
                            f.close()
                            self.client.send(m_put.hexdigest().encode('utf-8'))
                            # 接收服务端发回的md5验证结果
                            md5_response = self.client.recv(1024).strip()
                            if md5_response.decode() == '200':
                                print('file upload successfully')
                            else:
                                print('md5 not match, retry transfer the file.')
                    else:
                        print('错误代码{}: space not enough'.format(server_response.decode()))
                else:
                    print(filename, 'is not exist')
            else:
                print('the directory is not exist')
        else:
            print('please input the filename.')

    def cmd_get(self, *args):
        # 下载文件
        cmd_list = args[0].split()
        if len(cmd_list) > 1:
            filename = cmd_list[1]
            get_msg = {
                'filename': filename,
                'work_dir': self.work_path,
                'action': 'get'
            }
            # 发送文件信息给服务端
            self.client.send(json.dumps(get_msg).encode())
            # 接受服务端返回的信息
            get_response = self.client.recv(1024)
            info_dict = json.loads(get_response.decode())
            if info_dict['status'] == '200':
                file_size = info_dict['file_size']
                # 选择存储文件的位置
                storage_dir = input('输入保存文件的位置:')
                while os.path.exists(storage_dir) is not True:
                    print('该文件夹不存在,请重新输入')
                    storage_dir = input('输入保存文件的位置:')
                else:
                    # 进度条
                    bar = '>'
                    # 文件接收,并判断是否续传, 存在文件则续传
                    file_path = os.sep.join([storage_dir, filename])
                    if os.path.isfile(file_path + '.temp'):
                        received_size = os.stat(file_path + '.temp').st_size
                    else:
                        received_size = 0
                    # 回复服务端信息,防止服务端粘包
                    response_msg = {
                        'seek_location': received_size,
                        'status': '200'
                    }
                    self.client.send(json.dumps(response_msg).encode())
                    try:
                        f = open(file_path + '.temp', 'wb')
                        while received_size < file_size:
                            if file_size - received_size > 1024:
                                r_data = self.client.recv(1024)
                            else:
                                r_data = self.client.recv(file_size - received_size)
                            received_size += len(r_data)
                            f.write(r_data)
                            f.flush()
                            percent = int(float(received_size) / float(file_size) * 100)
                            # print(percent)
                            sys.stdout.write('\r' + '[' + bar * percent +
                                             ' ' * (100 - percent) + ']' + str(percent) + '%')
                            sys.stdout.flush()
                            if percent == 100:
                                sys.stdout.write('\n')
                        else:
                            f.close()
                            # 重命名.temp 结尾的文件
                            os.rename(file_path + '.temp', file_path)

                    except KeyboardInterrupt as e:
                        print(e)

            else:
                print('错误代码{}: file not exist')
        else:
            print('please input the filename.')

    def cmd_ls(self, *args):
        # 显示目录下内容
        cmd_msg = {
            'word_path': self.work_path,
            'action': 'ls'
        }
        self.client.send(json.dumps(cmd_msg).encode('utf-8'))
        # 接受服务端返回的信息
        ls_response = self.client.recv(1024)
        recv_dict = json.loads(ls_response.decode())
        if recv_dict['status'] == '200':
            # 显示目录下的文件和文件夹信息
            for i in recv_dict['dir_info']:
                print(i)
        else:
            print('错误代码{}:{}'.format(recv_dict['status'], recv_dict['dir_info']))

    def cmd_cd(self, *args):
        # 切换目录
        # 记录现有目录位置，如果切换错误，就停留在原本目录
        original_path = self.work_path
        # print(original_path)
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            dir_name = cmd_split[1]
            # 判断切换的路径是否一直在用户家目录中
            dir_list = dir_name.split('/')
            # cd '.'的情况
            dot_num = dir_list.count('.')
            # cd '..'的情况
            double_dot_num = dir_list.count('..')
            # 目录名称的情况
            dirs_list = dir_list[dot_num + double_dot_num:]

            if dir_list[:] == '.':
                workspace = self.work_path
            elif double_dot_num > 0:
                workspace = os.sep.join(self.work_path.split(os.sep)[:-double_dot_num])
                if len(workspace.split(os.sep)) < 4:
                    print('403,禁止切换到家目录以外')
                else:
                    workspace = os.sep.join(self.work_path.split(os.sep)[:-double_dot_num] + dirs_list)
            else:
                work_path_list = self.work_path.split(os.sep)
                new_path_list = work_path_list + dirs_list
                workspace = os.sep.join(new_path_list)
            cd_msg = {
                'workspace': workspace,   # 目录路径
                'action': 'cd'
            }
            self.client.send(json.dumps(cd_msg).encode())
            # 服务端验证结果
            cd_response = self.client.recv(1024)

            if cd_response.decode() == '200':
                self.work_path = workspace
            elif cd_response.decode() == '403':
                self.work_path = original_path
                # print('错误代码{}: can not change directory out of ftp home'.format(cd_response.decode()))
            else:
                print('错误代码{}: directory not exits'.format(cd_response.decode()))

        else:
            print('please input the directory.')

    def cmd_pwd(self, *args):
        # 显示路径
        print(self.work_path)

    def cmd_mkdir(self, *args):
        # 创建文件夹, 支持 aaa/bbb 递归
        cmd_list = args[0].split()
        if len(cmd_list) > 1:
            dirs = cmd_list[1].split('/')
            work_path_list = self.work_path.split(os.sep)
            dir_path_list = work_path_list + dirs
            dir_path = os.sep.join(dir_path_list)
            # 传递给服务端
            make_msg = {
                'dir_path': dir_path,
                'action': 'mkdir'
            }
            self.client.send(json.dumps(make_msg).encode())
            recv_data = self.client.recv(1024)
            if recv_data.decode() == '200':
                print('makedir successfully.')
            else:
                print('makedir unsuccessfully')
        else:
            print('please input the directory name')

def run():
    ftp_client = FtpClient()
    ftp_client.connect('localhost', 9999)
    ftp_client.authenticate()
