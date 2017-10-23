# -*- coding: UTF-8 -*-
import json
import os
import os.path
from ATM.conf import setting

conn_params = setting.DATABASE
db_path = "{}\{}".format(conn_params['path'], conn_params['username'])
# 遍历db\account下面的json文件,获取用户名,__init__.py除外


def file_dir(path):
    for home, dirs, files in os.walk(path):
        for filename in files:
            yield os.path.join(home, filename)


def card_name_passwd_dict(path):
    names_list = []
    password_list = []
    for fullname in file_dir(path):
        if fullname.split(".")[1] == "json":
            with open(fullname, 'r', encoding="utf-8") as f:
                acc_dict = json.load(f)
                names_list.append(acc_dict['card_number'])
                password_list.append(acc_dict['password'])
        else:
            continue
    card_dict = dict(zip(names_list, password_list))
    return card_dict
# print(card_info_dict(db_path))


def card_names_list(path):
    cc = card_name_passwd_dict(path)
    names_of_card = []
    for k in cc.keys():
        names_of_card.append(k)
    return names_of_card
