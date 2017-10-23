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

# mylogger = atm_log('error')
# mylogger.error("error2 information")
# mylogger.info("error3 information")
# mylogger.error("error4 information")
