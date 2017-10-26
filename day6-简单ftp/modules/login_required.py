# -*- coding: UTF-8 -*-


# 装饰器认证是否通过认证
def login_required(func):
    def wrapper(*args, **kwargs):
        if args[0].get('authentication'):
            res = func(*args, **kwargs)
            return res
        else:
            exit("\033[31m你还没有登入，请先登入.\033[0m")

    return wrapper
