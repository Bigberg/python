# -*- coding: UTF-8 -*-
from core.login import auth_login


def run():
    auth_result = auth_login()
    if auth_result:
        pass
