# -*- coding: UTF-8 -*-

import configparser
config = configparser.ConfigParser()
config.read("../conf/setting.ini", encoding='utf-8')

groups_dict = {}
for key in config['GROUPS']:
    groups_dict[key] = eval(config['GROUPS'][key])


def show_groups():

    group_list = []
    for k in groups_dict:
        group_list.append(k)
    return group_list


def show_hosts(group):
    hosts_dict = groups_dict[group]
    host_list = []
    for k in hosts_dict:
        host_list.append(k)
    return host_list

if __name__ == '__main__':
    g_list = show_groups()
    for i in range(len(g_list)):
        print(i+1, ': ', g_list[i])

    print('输入编号，选择主机组')
    g_choice = input('>>: ')
    while int(g_choice) not in range(1, len(g_list)+1):
        print('您的选择有误，请重新输入')
        g_choice = input('>>:').strip()
    else:
        h_list = show_hosts(g_list[int(g_choice)-1])
        for i in range(len(h_list)):
            print(groups_dict[g_list[int(g_choice)-1]][h_list[i]]['ip'])
