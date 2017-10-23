# -*- coding: UTF-8 -*-
import json
from MALL.config import setting


setting_params = setting.DATABASE
name_path = "{}\{}".format(setting_params['path'], setting_params['username'])

user_names = []
with open("{}\{}".format(name_path, "name_login.json"), "r" , encoding='utf-8') as loadfile:
    name_data = json.load(loadfile)

for k in name_data:
    user_names.append(k)


def login_auth():
    retry_count = 0
    acc_name = input("请输入用户名:").strip()
    while acc_name not in user_names:
        print("\033[31m没有该账号,请确认输入是否正确!\033[0m")
        acc_name = input("请输入您的帐号:").strip()
    else:
        if name_data[acc_name]["status"] == 1:  # status 0 正常  1 locked
            print("\033[31m 您的账号已经被锁定,请尽快和商城联系!\033[0m")
            exit()
        else:
            password = input("请输入密码:").strip()
            while password != name_data[acc_name]['password'] and retry_count < 3:
                print("\033[31m输入的密码有误!\033[0m")
                password = input("请输入密码:").strip()
                retry_count += 1
                if retry_count == 2:
                    name_data[acc_name]["status"] = 1
                    with open("{}\{}".format(name_path, "name_login.json"), "w", encoding="utf-8") as dumpfile:
                        json.dump(name_data, dumpfile)
                    print("\033[31m您尝试输入的次数过多!\033[0m")
                    exit()
            else:
                print("Welcome!{}".format(acc_name))
                return acc_name


