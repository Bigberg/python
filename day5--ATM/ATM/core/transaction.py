# -*- coding: UTF-8 -*-
from ATM.conf import setting
# conn_params = setting.DATABASE
# db_path = "{}\{}".format(conn_params['path'], conn_params['username'])
# trans_path = "{}\{}".format(conn_params['path'], conn_params['transaction'])


def transaction(t_log, amount, account_dict, action_type):
    interest = setting.TRANS_TYPE[action_type].get('interest')
    new_amount = amount + amount * interest
    old_balance = float(account_dict['balance'])
    new_balance = 0.0
    if action_type in setting.TRANS_TYPE:
        if setting.TRANS_TYPE[action_type].get('action') == 'plus':
            new_balance = old_balance + new_amount
        elif setting.TRANS_TYPE[action_type].get('action') == 'minus':
            new_balance = old_balance - new_amount
            if new_balance < 0:
                print("您的可用余额是{},但本次交易费用总共为{},余额不足!".format(old_balance, new_amount))
                exit()
        account_dict['balance'] = new_balance
        print("\033[32m本次交易完成,您的可用余额是{}\033[0m".format(new_balance))
        t_log.info("Account {} {} {}".format(account_dict['card_number'], action_type, amount))
    else:
        print("\033[31m没有该交易方式!\033[0m")

    return new_balance
