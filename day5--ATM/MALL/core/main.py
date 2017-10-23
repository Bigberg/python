# -*- coding: UTF-8 -*-
import time
import json
from MALL.core import login
from MALL.config import setting
from MALL.core import show_goods
from MALL.core import get_balance_from_atm
from ATM.core import load_and_dump
from ATM.core import record
from MALL.core import shop_record
setting_params = setting.DATABASE
goods_path = "{}\{}".format(setting_params['path'], setting_params['goods'])

record_path = "{}\{}".format(setting_params['path'], setting_params['shop'])

cost = 0  # 消费的金钱
shopping_list = []   # 购买的物品
# 所有商品
commodity_list = show_goods.show_goods(goods_path, "commodities.json")
# print(commodity_list)

# 银行卡登入状态
card_condition = {
    'card_number': None,
    'card_balance': 0,
    'authentication': False
}

card_account = {}

user_condition = {
    'username': None,
    'authentication': False
}
# 设置一个balance2 用于记录购物完毕没有退出,继续购物时所用
balance2 = 0


def shopping():
    for i in range(len(commodity_list)):
        print(i+1, commodity_list[i][0], commodity_list[i][1])
    num_list = []
    for i in range(len(commodity_list)):
        num_list.append(str(1+i))
    # print(num_list)
    choice = input("输入商品编号,选择购买商品:").strip()
    if choice in num_list:
        shopping_list.append(commodity_list[int(choice) - 1][0])
        print(" ".join(shopping_list))
        global cost
        cost += commodity_list[int(choice) - 1][1]
        print(cost)
    else:
        print("没有该商品!")


def pay():

    global balance2

    commodity_dict = dict(commodity_list)
    # 购物时要输入银行卡号和密码，当本次结账后不退出程序,继续购买不需要再次输入银行卡账号和密码
    if card_condition['authentication'] is False:
        global card_account
        card_account = get_balance_from_atm.get_balance()
        card_condition['authentication'] = True
        card_condition['balance'] = card_account['balance']
        balance = card_condition['balance']
        print("您卡中的余额是{}".format(balance))
    else:
        balance = balance2
        print("您卡中的余额是{}".format(balance))
    global cost
    while cost > balance:
        print("您的余额不足!")
        for i in range(len(shopping_list)):
            print(i+1, shopping_list[i])
        num_list = []
        for i in range(len(shopping_list)):
            num_list.append(str(1 + i))
        choice = input("输入q退出,输入编号删除部分商品:")
        if choice.lower() == 'q':
            exit()
        elif choice in num_list:
            product = shopping_list.pop(int(choice) - 1)
            cost -= commodity_dict[product]
            if cost == 0:
                print("您现在没有购买任何商品!")
                break
        else:
            print("您的输入有误!")
    else:
        print("正在付款...")
        time.sleep(1)
        print("...")
        time.sleep(1)
        print("...")
        balance -= cost
        balance2 = balance
        card_account['balance'] = balance
        from ATM.conf import setting
        conn_params = setting.DATABASE
        db_path = "{}\{}".format(conn_params['path'], conn_params['username'])
        atm_record_path = "{}\{}".format(conn_params['path'], conn_params['transaction'])
        # 将卡的账号信息导入到银行卡中
        load_and_dump.dump_data(db_path, card_account['card_number'], card_account)
        # 将购买记录写入atm交易记录中
        record.atm_record(card_account['card_number'], atm_record_path, 'consume', str(cost))
        # 将购物记录写入mall交易记录中
        shop_record.shop_record(record_path, user_condition['username'], 'buy', shopping_list, str(cost))
        print("交易完成!")
        # 临时购物记录清零
        while len(shopping_list) > 0:
            shopping_list.pop()

        # 临时消费金额清零
        cost = 0


def refer():
    with open("{}/record_of_{}.json".format(record_path, user_condition['username']), 'r', encoding='utf-8') as load_f:
        record_dict = json.load(load_f)
    month = []
    for key in record_dict:
        month.append(key)
    month.sort()
    print("\033[32m您今年所能查询的月份是: \033[0m")
    for i in month:
        print(i, end="" + "\n")
    choice = input("选择查询的月份: ").strip()
    while choice not in month:
        choice = input("选择查询的月份: ").strip()
    else:
        trans_list = record_dict[choice]
        for i in range(len(trans_list)):
            print(trans_list[i])


def login_out():
    exit()


def shopping_action():
    menu = '''--- Welcome to Mall ---
        \033[32m 1. 购物
         2. 付款
         3. 购买记录
         4. 退出
\033[0m-----------------------'''
    menu_dict = {
        "1": shopping,
        "2": pay,
        "3": refer,
        "4": login_out
    }
    while True:
        print(menu)
        choice = input("输入编号选择您所需的功能:").strip()
        if choice in menu_dict:
            menu_dict[choice]()
        else:
            print("\033[31;1mOption does not exist!\033[0m")


def run():
    auth_result = login.login_auth()
    user_condition['username'] = auth_result
    user_condition['authentication'] = True
    if user_condition['authentication']:
        shopping_action()


