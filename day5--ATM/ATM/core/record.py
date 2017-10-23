# -*- coding: UTF-8 -*-
import time
# from ATM.conf import setting
from ATM.core import load_and_dump

# conn_params = setting.DATABASE
# record_path = "{}\{}".format(conn_params['path'], conn_params['transaction'])


# 将交易记录到json文件中
def atm_record(account_id, data_path, action_type, amount):
    record_dict = load_and_dump.load_data(data_path, account_id)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    month = current_time.split('-')[1][-1]
    try:
        record_dict[month].append(current_time + "    " + action_type + "    " + amount)
    except KeyError:
        record_dict[month] = [current_time + "    " + action_type + "    " + amount]

    load_and_dump.dump_data(data_path, account_id, record_dict)


# atm_record('62028888', record_path, 'withdraw', '3000')
