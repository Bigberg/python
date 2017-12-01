# -*- coding: UTF-8 -*-
import logging
from ATM.conf import setting
# print(setting.Base_dir)


def atm_log(log_type):
    # create logger
    logger = logging.getLogger(log_type)
    logger.setLevel(setting.Log_lev)

    # FileHandler
    log_path = "{}/log".format(setting.Base_dir)
    fh = logging.FileHandler("{}/{}".format(log_path, setting.Log_type[log_type]), encoding='utf-8')

    # Formatter
    formatter = logging.Formatter("%(asctime)s %(filename)s-%(lineno)d %(levelname)s:%(message)s",
                                  datefmt='%Y/%m/%d %H:%M:%S')
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger

if __name__ == '__main__':

    mylog = atm_log('access')
    mylog2 = atm_log('error')
    mylog.info('success')
    mylog2.error('error info')