# -*- coding: UTF-8 -*-
import sys
import os
import pika
import subprocess
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)
from modules.get_ip import get_ip
sys_code = sys.getfilesystemencoding()


class HostRpcServer(object):

    host_addr = get_ip('eth0')
    credentials = pika.PlainCredentials('bigberg', '111111')

    def __init__(self, host, port):
        '''

        :param host: host addresss
        :param port: rabbitmq port
        '''
        self.host = host
        self.port = port
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            self.host, self.port, '/', self.credentials))

        self.channel = self.connection.channel()

        # 这个是客户端最初发送消息时使用的队列 rpc_queue
        self.channel.exchange_declare(exchange='rpc_topic',
                                      exchange_type='topic')
        result = self.channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        self.channel.queue_bind(exchange='rpc_topic',
                                queue=queue_name,
                                routing_key=self.host_addr)

        self.channel.basic_consume(self.on_request,
                                   queue=queue_name)

    def main(self):
        print(" [x] Awaiting RPC requests")
        self.channel.start_consuming()

    # 回调函数
    def on_request(self, ch, method, props, body):

        command = body.decode('utf-8')
        print('Received:', command)
        res = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = res.communicate()
        res_con = err.decode(sys_code) if err.decode(sys_code) else out.decode(sys_code)
        res = 'from host ' + self.host_addr + '\n' + res_con
        # print(res_con.decode('GBK'))

        ch.basic_publish(exchange='',
                         # 这个routing_key 定义了返回的队列是哪一个
                         # 就是客户端定义的 reply_to
                         routing_key=props.reply_to,
                         # correlation_id 就是客户端生成的corr_id
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id),
                         body=res.encode('utf-8'))
        # 消息处理完毕后，主动告知rabbitmq
        ch.basic_ack(delivery_tag=method.delivery_tag)


def run():
    host = '172.16.200.109'
    port = 5672
    server_rpc = HostRpcServer(host, port)
    server_rpc.main()

