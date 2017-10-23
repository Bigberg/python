# -*- coding: UTF-8 -*-
import time
import json
from ATM.conf import setting
from ATM.dbhandeer import cardsname
from ATM.core import atmlog
conn_params = setting.DATABASE
db_path = "{}\{}".format(conn_params['path'], conn_params['username'])
# access.log
access_logger = atmlog.atm_log('access')

# error.log
error_logger = atmlog.atm_log('error')


# 装饰器认证是否通过认证
def login_required(func):
    def wrapper(*args, **kwargs):
        if args[0].get('authentication'):
            res = func(*args, **kwargs)
            return res
        else:
            error_logger.error("account [{}] has not passed authentication.".format(args[0].get('account_id')))
            exit("account has not passed authentication.")
    return wrapper


# 验证用户名和密码
def acc_auth(account, password):
    cards_info = cardsname.card_name_passwd_dict(db_path)
    if password == cards_info[account]:
        with open("{}\{}.json".format(db_path, account), 'r', encoding="utf-8") as f:
            read_dict = json.load(f)
        expire_time_stamp = time.mktime(time.strptime(read_dict['expire_date'], "%Y-%m-%d"))
        if time.time() > expire_time_stamp:
            print("\033[31m 您的信用卡已经过期,请联系银行重新办理!\033[0m")
            exit()
        else:
            access_logger.info("account [%s] passed authentication." % account)
            return True
    else:
        print("\033[31m密码错误\033[0m")
        error_logger.error("account [%s] password is wrong." % account)


# 登入认证
def acc_login(account_data):
    retry_count = 0
    account = input("请输入您的卡号:").strip()
    account_names = cardsname.card_names_list(db_path)
    while account not in account_names:
        print("\033[31m没有该账号,请确认您的输入是否正确!\033[0m")
        account = input("请输入您的卡号:").strip()
    else:
        while account_data['authentication'] is not True and retry_count < 3:
            password = input("请输入您的密码:").strip()
            auth_data = acc_auth(account, password)
            if auth_data:  # 有返回值就为真
                account_data['account_id'] = account
                account_data['authentication'] = True
                return account_data
            retry_count += 1
        else:
            print("\033[31m您尝试登入的次数过多!\033[0m")
            error_logger.error("account [%s] tries too many login attempts." % account)
            exit()
