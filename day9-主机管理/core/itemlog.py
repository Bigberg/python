# -*- coding: UTF-8 -*-
import logging
from logging import handlers
import configparser
import os

config = configparser.ConfigParser()
config.read("../conf/setting.ini", encoding='utf-8')
log_level = config['BASE']['log_level']


def item_log(log_type):
    # create logger
    logger = logging.getLogger(log_type)
    logger.setLevel(log_level)

    # FileHandler
    log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config['BASE']['log_path'])
    log_file = "{}/{}.log".format(log_path, log_type)
    fh = handlers.TimedRotatingFileHandler(filename=log_file, when='midnight', interval=1, backupCount=7,
                                           encoding='utf-8')
    fh.setLevel(log_level)
    # Formatter
    formatter = logging.Formatter("%(asctime)s %(filename)s-%(lineno)d %(levelname)s:%(message)s",
                                  datefmt='%Y/%m/%d %H:%M:%S')
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger

if __name__ == '__main__':

    mylog = item_log('access')
    mylog2 = item_log('error')
    mylog.info('success')
    mylog2.error('error info')
