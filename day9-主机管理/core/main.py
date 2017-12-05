# -*- coding: UTF-8 -*-
from core.login import auth_login
from core.group_and_host_handle import group_and_host_choice
from core.sshclient import SSHConnection
import threading
import queue
# 队列接收输入
q = queue.Queue()


def ssh_function(cmd, host, ip, port, username, password):  # 多线程执行程序
    obj = SSHConnection(host)
    obj.connect(ip, port, username, password)
    obj.interactive(cmd)


def run():
    auth_result = auth_login()
    if auth_result:
        # 获取需要被处理的主机列表
        hosts_list = group_and_host_choice()
        if hosts_list:
            while True:
                cmd_line = input('>>:').strip()

                if len(cmd_line) == 0:
                    continue
                elif cmd_line == 'exit':
                    exit()
                else:
                    # 为每个主机执行的线程提供输入的信息
                    for j in range(len(hosts_list)):
                        q.put(cmd_line)

                    for i in range(len(hosts_list)):
                        t = threading.Thread(
                            target=ssh_function,
                            args=(q.get(), hosts_list[i][0],
                                  hosts_list[i][1], hosts_list[i][2], hosts_list[i][3], hosts_list[i][4]))
                        t.start()
