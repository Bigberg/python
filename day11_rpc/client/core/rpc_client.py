# -*- coding: UTF-8 -*-

import pika
import random
import re
import time


class HostRpcClient(object):
    # rpc 主机管理客户端

    # 保存命令返回的结果，以corr_id , value 形式
    task_result = {}

    def __init__(self, host):
        '''

        :param host: host address
        '''
        self.host = host
        # 初始化时创建连接
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.host))
        # 初始化建立管道
        self.channel = self.connection.channel()
        # 这里是客户端接收服务端的返回
        # 在此要声明一个queue,并且名称随机生成
        result = self.channel.queue_declare(exclusive=True)
        # 该callback_queue 指定了服务端返回时，用哪一个queue
        self.callback_queue = result.method.queue
        # 客户端处理服务端返回的消息，指定获取信息的队列queue 和 回调函数
        self.channel.basic_consume(self.on_response,
                                   no_ack=True,
                                   queue=self.callback_queue)

    @staticmethod
    def help(*args):
        msg = '''
        可以使用的方法
        run 'df -h' --host 192.168.0.2 execute command
        check_task ***   show results
        '''
        print(msg)

    def handle(self):

        while True:
            cmd = input('>>:').strip()
            cmd_str = cmd.split(' ')[0]
            if hasattr(self, cmd_str):
                func = getattr(self, cmd_str)
                func(cmd)
            else:
                self.help()

    # 客户端的回调函数，用来处理服务端返回的数据
    def on_response(self, ch, method, props, body):
        # 客户端回调函数对服务端返回数据的处理
        # 此correlation_id 为服务端返回的id, 用来确保处理的消息为同一条
        if self.corr_id == props.correlation_id:
            # 将返回的信息body 给 response
            self.response = body.decode('utf-8')
            self.task_result[self.corr_id].append(self.response)

    # run函数就是client 最初发送消息的地方
    def run(self, *args):
        # 获取ip
        severities = re.findall(r'(?<![\.\d])(?:25[0-5]\.|2[0-4]\d\.|[01]?\d\d?\.)'
                                r'{3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)(?![\.\d])', args[0])
        # print(severities)
        # 获取命令内容
        cmd_line = re.search('\".*\"', args[0]).group()
        cmd_str = cmd_line.split('\"')[1]
        # self.response = None
        self.corr_id = str(random.randint(1, 65535))
        self.task_result[self.corr_id] = []
        print('task_id:', self.corr_id)
        for severity in severities:
            self.response = None
            self.channel.basic_publish(exchange='rpc_topic',
                                       routing_key=severity,
                                       properties=pika.BasicProperties(
                                           # reply_to指定了服务端返回时使用的queue
                                           reply_to=self.callback_queue,
                                           correlation_id=self.corr_id,
                                       ),
                                       body=cmd_str.encode('utf-8'))

        # 客户端发送和接收消息的队列是不一样的
        # 所以需要对接收消息的队列不断查询
        # 如果有消息了就接收
            while self.response is None:
                # 当这里使用 channel.start_consumer() 为阻塞状态
                # 使用connection.process_data_events() 为非阻塞
                self.connection.process_data_events()
                # time.sleep(3)

    def check_task(self, *args):

        task_id = args[0].split(' ')[1]
        if self.task_result.get(task_id):
            for i in self.task_result[task_id]:
                print(i)
        else:
            print('没有该task_id')


def run():
    client_rpc = HostRpcClient('localhost')
    client_rpc.handle()
