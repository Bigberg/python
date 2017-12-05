# -*- coding: UTF-8 -*-
from core.itemlog import item_log
import configparser
config = configparser.ConfigParser()
config.read("../conf/setting.ini", encoding='utf-8')
error_log = item_log('error')

groups_dict = {}
for key in config['GROUPS']:
    groups_dict[key] = eval(config['GROUPS'][key])


def show_groups():
    # 获取组名
    g_list = []
    for k in groups_dict:
        g_list.append(k)
    return g_list


def show_hosts(group):
    # 显示组中host信息
    h_list = groups_dict[group]
    return h_list


def group_and_host_choice():
    group_list = show_groups()
    # 显示主机组信息
    for i in range(len(group_list)):
        print(i + 1, ' : ', group_list[i])
    # 选择主机组
    choice_group = input("请输入编号选择主机组:")
    while int(choice_group) not in range(1, len(group_list) + 1):
        print('您的输入有误，请确认后重新输入')
        error_log.error('选择主机组时，编号输入不正确')
        choice_group = input("请输入编号选择主机组:")
    else:
        # 显示主机信息
        host_list = show_hosts(group_list[int(choice_group) - 1])
        for i in range(len(host_list)):
            print(i + 1, ':', host_list[i][0] + '--->' + host_list[i][1])
        # 需要被执行的主机
        need_to_handle_list = []

        # 选择主机
        choice_host = input("请输入编号选择主机,0表示所有主机:")
        while int(choice_group) not in range(0, len(group_list) + 1):
            print('您的输入有误，请确认后重新输入')
            error_log.error('选择主机时，编号输入不正确')
            choice_group = input("请输入编号选择主机,0表示所有主机:")
        else:
            # 选择0 表示所有主机都需要处理
            if int(choice_host) == 0:
                need_to_handle_list = host_list
            else:
                # 选择其他编号表示只需处理单台主机
                need_to_handle_list.append(host_list[int(choice_host) - 1])

    return need_to_handle_list
