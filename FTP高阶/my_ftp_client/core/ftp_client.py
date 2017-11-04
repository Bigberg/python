# -*- coding: UTF-8 -*-
import socket
import os
import json
import hashlib


class FtpClient(object):

    def __init__(self):
        self.client = socket.socket()
        self.authentication = False  # 判断是否登入

    def help(self):   # 打印指令信息
        msg = '''
        ls
        pwd
        cd ../..
        get filename
        put filename
        '''
        print(msg)

    def connect(self, ip, port):
        self.client.connect((ip, port))

    def interactive(self):
        # if self.authenticate():  # 登入认证模块
        while True:
            cmd = input(">>:").strip()
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
            acc_response = self.client.recv(1024)
            if acc_response.decode() == 'ok':
                print('登入成功')
                self.authentication = True
                self.interactive()
            else:
                print('登入验证失败')
                continue

    def cmd_put(self, *args):
        # 上传文件
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            filename = cmd_split[1]
            if os.path.isfile(filename):
                file_size = os.stat(filename).st_size
                # 将文件名、大小等信息传给服务端，为了一些其他判断，可以预先使用json格式
                msg_dict = {
                    'filename': filename,
                    'size': file_size,
                    'overridden': False,
                    'action': 'put'
                }
                self.client.send(json.dumps(msg_dict).encode())
                # 防止粘包，等服务器确认
                server_response = self.client.recv(1024)
                # 通过response 接受服务端返回的一些配置或出错信息，比如剩余空间是否足够，文件已存在覆盖？
                #  要做处理
                f = open(filename, 'rb')
                for line in f:
                    self.client.send(line)
                else:
                    f.close()
                    print('file upload successfully')
            else:
                print(filename, 'is not exits')

        else:
            print('please input the filename.')

    def cmd_get(self):
        pass


if __name__ == '__main__':
    ftp_client = FtpClient()
    ftp_client.connect('localhost', 9999)
    ftp_client.authenticate()
