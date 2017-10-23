# -*- coding: UTF-8 -*-
import json
from ATM.core import auth
from ATM.core import load_and_dump
from ATM.conf import setting
conn_params = setting.DATABASE
db_path = "{}\{}".format(conn_params['path'], conn_params['username'])

temp_data = {
    'account_id': None,
    'authentication': False
}


def get_balance():
    acc_data = auth.acc_login(temp_data)
    load_dict = load_and_dump.load_data(db_path, acc_data["account_id"])
    return load_dict

# balance = get_balance()
# print(balance)
