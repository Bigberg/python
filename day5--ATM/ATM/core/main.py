# -*- coding: UTF-8 -*-
import json
from ATM.core import auth
from ATM.conf import setting
from ATM.core.auth import login_required
from ATM.core import atmlog
from ATM.core import load_and_dump
from ATM.core import transaction
from ATM.dbhandeer import cardsname
from ATM.core import record
conn_params = setting.DATABASE
db_path = "{}\{}".format(conn_params['path'], conn_params['username'])
record_path = "{}\{}".format(conn_params['path'], conn_params['transaction'])
# transaction.log
transaction_logger = atmlog.atm_log('transaction')
# 临时的认证数据
account_data = {
    'account_id': None,
    'authentication': False
}


@login_required
def info_account(acc_data):
    with open("{}/{}.json".format(db_path, acc_data['account_id']), 'r', encoding="utf-8") as read_f:
        read_dict = json.load(read_f)
    info = '''\033[35m------- 您的账号{_account}目前的信息 --------
          card_number: {_card_number},
          credit: {_credit},
          balance: {_balance},
          enroll_date: {_enroll_date},
          expire_date: {_expire_date},
          pay_day: {_pay_day},
          status: {_status}
--------------------------------------------\033[0m
            '''.format(_account=read_dict['card_number'], _card_number=read_dict['card_number'],
                       _credit=read_dict['credit'], _balance=read_dict['balance'],
                       _enroll_date=read_dict['enroll_date'], _expire_date=read_dict['expire_date'],
                       _pay_day=read_dict['pay_day'], _status=read_dict['status'])
    print(info)


@login_required
def repay(acc_data):  # 还款
    account_dict = load_and_dump.load_data(db_path, acc_data['account_id'])
    credit = account_dict['credit']
    balance = account_dict['balance']
    print("本期应还款金额是: {}".format(float(credit)-float(balance)))
    acc_amount = float(input("请输入还款金额: "))
    transaction.transaction(transaction_logger, acc_amount, account_dict, 'repay')
    load_and_dump.dump_data(db_path, account_dict['card_number'], account_dict)
    # 记录交易
    record.atm_record(acc_data['account_id'], record_path, 'repay', str(acc_amount))


@login_required
def withdraw(acc_data):  # 取现
    account_dict = load_and_dump.load_data(db_path, acc_data['account_id'])
    credit = account_dict['credit']
    balance = account_dict['balance']
    info = '''---- BALANCE INFO ----
    Credit:   {_credit}
    Balance:  {_balance}
'''.format(_credit=credit, _balance=balance)
    print(info)
    acc_amount = float(input("请输入您想提取的金额: "))
    transaction.transaction(transaction_logger, acc_amount, account_dict, 'withdraw')
    load_and_dump.dump_data(db_path, account_dict['card_number'], account_dict)
    # 记录交易
    record.atm_record(acc_data['account_id'], record_path, 'withdraw', str(acc_amount))


@login_required
def trans_account(acc_data):  # 转账
    card = input("请输入您想转账的卡号: ")
    cards_list = cardsname.card_names_list(db_path)
    while card not in cards_list:
        print("\033[31m没有该账号,请确认输入是否正确!\033[0m")
        card = input("请输入您想转账的卡号: ")
    else:
        account_dict = load_and_dump.load_data(db_path, acc_data['account_id'])
        acc_amount = float(input("请输入转账金额: "))
        transaction.transaction(transaction_logger, acc_amount, account_dict, 'transfer')
        load_and_dump.dump_data(db_path, account_dict['card_number'], account_dict)
        # 转入的账户增加金额
        transfer_dict = load_and_dump.load_data(db_path, card)
        transfer_dict['balance'] = float(transfer_dict['balance']) + acc_amount
        load_and_dump.dump_data(db_path, card, transfer_dict)
        transaction_logger.info("Account {} 收到 {} 转账金额 {}".format(card, acc_data['account_id'], acc_amount))
        # 记录交易
        record.atm_record(acc_data['account_id'], record_path, 'transfer', str(acc_amount))


@login_required
def bills(acc_data):  # 账单
    bills_dict = load_and_dump.load_data(record_path, acc_data['account_id'])
    month = []
    for key in bills_dict:
        month.append(key)
    month.sort()
    print("\033[32m您今年所能查询的月份是: \033[0m")
    for i in month:
        print(i, end="" + "\n")
    choice = input("选择查询的月份: ").strip()
    while choice not in month:
        choice = input("选择查询的月份: ").strip()
    else:
        trans_list = bills_dict[choice]
        for i in range(len(trans_list)):
            print(trans_list[i])


@login_required
def login_out(acc_data):  # 退出
    print("\033[32m尊敬的{}卡主,欢迎下次使用!\033[0m".format(acc_data['account_id']))
    exit()


def interactive(data):
    menu = '''--- Welcome to Bank ---
    \033[32m 1. 账号信息
     2. 还款
     3. 取款
     4. 转账
     5. 账单
     6. 退出
\033[0m-----------------------'''
    menu_dict = {
        "1": info_account,
        "2": repay,
        "3": withdraw,
        "4": trans_account,
        "5": bills,
        "6": login_out
    }
    while True:
        print(menu)
        choice = input("输入编号选择您所需的功能:").strip()
        if choice in menu_dict:
            menu_dict[choice](data)
        else:
            print("\033[31;1mOption does not exist!\033[0m")


def run():
    acc_data = auth.acc_login(account_data)
    if acc_data['authentication']:
        interactive(acc_data)
