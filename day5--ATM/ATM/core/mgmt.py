# -*- coding: UTF-8 -*-
import json
from ATM.conf import setting
from ATM.dbhandeer import cardsname
conn_params = setting.DATABASE
db_path = "{}\{}".format(conn_params['path'], conn_params['username'])
record_path = "{}\{}".format(conn_params['path'], conn_params['transaction'])

names_of_cards = []


def add_account():
    # 根据db下的account_sample格式来增加账号
    account_dict = {}
    card_number = input("like 62021234:")
    password = input("password:")
    credit = input("credit:")
    balance = input("balance:")
    enroll_date = input("enroll_date:")
    expire_date = input("expire_date:")
    pay_day = input("pay_day:")
    status = input("status:")
    account_dict["card_number"] = card_number
    account_dict["password"] = password
    account_dict["credit"] = credit
    account_dict["balance"] = balance
    account_dict["enroll_date"] = enroll_date
    account_dict["expire_date"] = expire_date
    account_dict["pay_day"] = pay_day
    account_dict["status"] = status
    with open("{}/{}.json".format(db_path, card_number), 'w', encoding="utf-8") as f:
        f.write(json.dumps(account_dict))
    # 初始化交易记录数据表
    with open("{}/{}.json".format(record_path, card_number), 'w', encoding="utf-8") as record_f:
        record_dict = {}
        record_f.write(json.dumps(record_dict))


def increase_credit():
    # 提升额度,并设定提升的额度不能低于原本的额度
    card_number = input("请输入您想要更改的卡号:")
    if card_number not in names_of_cards:
        print("\033[31m没有该账号,请确认后重新输入!\033[0m")
    else:
        with open("{}/{}.json".format(db_path, card_number), 'r', encoding="utf-8") as read_f:
            read_dict = json.load(read_f)
        old_credit = read_dict['credit']
        print("目前的额度为: {}".format(old_credit))
        new_credit = input("请输入新的额度:")
        if int(old_credit) >= int(new_credit):
            print("\033[31m提升后的额度需要大于原来的额度,请确认后重新输入!\033[0m")
        else:
            read_dict["credit"] = new_credit
            with open("{}/{}.json".format(db_path, card_number), 'w', encoding="utf-8") as write_f:
                json.dump(read_dict, write_f)
            print("\033[32m额度提升完成!\033[0m")


def change_status():
    card_number = input("请输入您想要更改状态的卡号:")
    if card_number not in names_of_cards:
        print("\033[31m没有该账号,请确认后重新输入!\033[0m")
    else:
        with open("{}/{}.json".format(db_path, card_number), 'r', encoding="utf-8") as read_f:
            read_dict = json.load(read_f)
        old_status = read_dict['status']
        info = '''    0 : 正常,
    1 : 锁定,
    2 : 过期'''
        print(info)
        print("目前该卡号的状态为： {}".format(old_status))
        new_status = input("请输入您想要更改的状态的编号: ")
        while new_status not in ["0", "1", "2"]:
            print("您的输入有误!请输入[0-2]中的值!")
            new_status = input("请输入您想要更改的状态的编号: ")
        else:
            read_dict['status'] = new_status
            with open("{}/{}.json".format(db_path, card_number), 'w', encoding="utf-8") as write_f:
                json.dump(read_dict, write_f)
            print("\033[32m该卡的状态修改完成!\033[0m")


def view():
    card_number = input("请输入您想要查询的卡号:")
    if card_number not in names_of_cards:
        print("\033[31m没有该账号,请确认后重新输入!\033[0m")
    else:
        with open("{}/{}.json".format(db_path, card_number), 'r', encoding="utf-8") as read_f:
            read_dict = json.load(read_f)
        info = '''\033[35m----------- {_account} info ------------
        card_number: {_card_number},
        credit: {_credit},
        balance: {_balance},
        enroll_date: {_enroll_date},
        expire_date: {_expire_date},
        pay_day: {_pay_day},
        status: {_status}
--------------------------------------\033[0m
        '''.format(_account=read_dict['card_number'], _card_number=read_dict['card_number'],
                   _credit=read_dict['credit'], _balance=read_dict['balance'],
                   _enroll_date=read_dict['enroll_date'], _expire_date=read_dict['expire_date'],
                   _pay_day=read_dict['pay_day'], _status=read_dict['status'])
        print(info)


def logout():
    exit()


def interactive():
    menu = '''--- Welcome to Manage Page ---
    \033[32m 1. 添加账户
     2. 提升额度
     3. 修改状态
     4. 查看账户
     5. 退出
\033[0m-------------------------------'''
    menu_dict = {
        "1": add_account,
        "2": increase_credit,
        "3": change_status,
        "4": view,
        "5": logout
    }
    while True:
        # 获取卡号
        global names_of_cards
        names_of_cards = cardsname.card_names_list(db_path)
        print(menu)
        choice = input("输入编号选择您所需的功能:")
        if not choice.isdigit():
            print("请输入1-5中的数字!")
            continue
        else:
            if int(choice) < 1 or int(choice) > 6:
                print("The input must be in 1-3.")
                continue
        action = menu_dict[choice]
        action()


def run():
    interactive()
