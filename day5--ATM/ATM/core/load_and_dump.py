# -*- coding: UTF-8 -*-
import json
# from ATM.conf import setting
# conn_params = setting.DATABASE
# db_path = "{}\{}".format(conn_params['path'], conn_params['username'])


def load_data(db_path, account_id):
    with open("{}\{}.json".format(db_path, account_id), 'r', encoding="utf-8") as f:
        account_dict = json.load(f)
    return account_dict


def dump_data(db_path, account_id, data):
    with open("{}\{}.json".format(db_path, account_id), 'w', encoding="utf-8") as f:
        json.dump(data, f)

# account_data = load_data('62028888')
# print(account_data)
