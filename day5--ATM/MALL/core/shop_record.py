# -*- coding: UTF-8 -*-
import json
import time
# from MALL.config import setting
#
# setting_params = setting.DATABASE
# record_path = "{}\{}".format(setting_params['path'], setting_params['shop'])


def shop_record(data_path, username, action_type, shop_list, amount):
    with open("{}/record_of_{}.json".format(data_path, username), 'r', encoding='utf-8') as load_f:
        record_dict = json.load(load_f)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    month = current_time.split('-')[1][-1]
    commodities = ','.join(shop_list)
    try:
        record_dict[month].append(current_time + "    " + action_type + "    " + commodities + "   " + amount)
    except KeyError:
        record_dict[month] = [current_time + "    " + action_type + "    " + commodities + "   " + amount]

    with open("{}/record_of_{}.json".format(data_path, username), 'w', encoding='utf-8') as dump_f:
        json.dump(record_dict, dump_f)

# shop_record(record_path, "bigberg", "buy", ["iphone", "mac"], '18000')

