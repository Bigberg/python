# -*- coding: UTF-8 -*-
import paramiko
from core.itemlog import item_log
error_log = item_log('error')
access_log = item_log('access')


class SSHConnection(object):
    # 主机管理类

    def __init__(self, host):
        self.ssh = paramiko.SSHClient()
        self.host = host
        self.__transport = None

    def connect(self, ip, port, username, password):
        '''
        登入服务端
        :param ip: mod:`string` like '172.16.200.1'
        :param port: mod `int` like 22
        :param username: mod `string`
        :param password: mod `string`
        :return:
        '''
        # 允许连接不在know_hosts文件中的主机
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        transport = paramiko.Transport(ip, port)
        transport.connect(username=username, password=password)
        self.__transport = transport

    def interactive(self, cmd):
        '''
        验证命令是否存在，存在则执行
        :param cmd: mod `string`
        :return:
        '''

        command_str = cmd.split()[0]
        # 使用反射
        if hasattr(self, 'command_%s' % command_str):
            func = getattr(self, 'command_%s' % command_str)
            func(cmd)  # 执行命令
        else:
            print('command not found')
            error_log.error('command not fo'
                            'und')
        # cmd = input('>>:')

    def command_cmd(self, *args):
        '''
        执行输入的命令
        :param args: mod `tuple`
        :return:
        '''
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        # 执行命令
        command = args[0].split()[1:]
        command_line = ' '.join(command)
        stdin, stdout, stderr = ssh.exec_command(command_line)
        res, err = stdout.read(), stderr.read()
        result = res if res else err
        print('-----%s-----' % self.host)
        print(result.decode())

    def command_put(self, *args):
        '''
        上传文件
        :param args: mod `tuple`
        :return:
        '''
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        # 上传文件路径
        src_path = args[0].split()[1]
        print('-----%s-----' % self.host)
        print('需要上传的文件：%s' % src_path)
        # 存放文件路径
        dst_path = args[0].split()[2]
        print('存放文件的路径:%s' % dst_path)
        sftp.put(src_path, dst_path)
        print('上传完成!')
        access_log.info('上传文件至主机%s成功' % self.host)

    def command_get(self, *args):
        '''
        下载文件
        :param args: mod `tuple`
        :return:
        '''
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        # 下载的文件路径
        download_path = args[0].split()[1]
        print('-----%s-----' % self.host)
        print('下载的文件：%s' % download_path)
        # 存放文件的路径
        store_path = args[0].split()[2]
        print('存放文件的路径:%s' % store_path)
        sftp.get(download_path, store_path)
        print('下载完成!')
        access_log.info('从主机%s上下载文件成功' % self.host)
