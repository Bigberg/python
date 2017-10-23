# -*- coding: UTF-8 -*-
import json


# setting_params = setting.DATABASE
# goods_path = "{}\{}".format(setting_params['path'], setting_params['goods'])


def show_goods(path, file_of_goods):
    with open("{}\{}".format(path, file_of_goods), "r", encoding='utf-8') as loadfile:
        goods_list = json.load(loadfile)
    return goods_list

# show_goods(goods_path, "commodities.json")
