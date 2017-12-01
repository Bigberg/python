# -*- coding: UTF-8 -*-
import os
import logging
from logging import handlers
import configparser

# 路径
BasePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BasePath)


class FTPLog(object):
    # 读取配置文件信息
    config = configparser.ConfigParser()
    config.read("{}/config/setting.ini".format(BasePath), encoding='utf-8')

    # 定义一个log 类
    def __init__(self, log_dir):
        self.log_dir = log_dir

    # 定义log方法
    def ftp_log(self):
        logger = logging.getLogger('ftp-log')
        log_level = self.config['DEFAULT']['LogLevel']
        # print(log_level)
        logger.setLevel(log_level)

        # FileHandler
        # 日志保存路径
        log_file = os.path.join(BasePath, self.log_dir, 'ftp.log')

        fh = handlers.TimedRotatingFileHandler(filename=log_file, when="midnight", interval=1, backupCount=3, encoding="utf-8")
        fh.setLevel(log_level)

        # Formatter
        formatter = logging.Formatter("%(asctime)s %(filename)s-%(lineno)d %(levelname)s:%(message)s",
                                      datefmt='%Y/%m/%d %H:%M:%S')
        fh.setFormatter(formatter)

        logger.addHandler(fh)
        return logger


if __name__ == '__main__':
    f = FTPLog('logs')
    my_log = f.ftp_log()
    my_log.info("success")
