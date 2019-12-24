#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @contact: voidqueens@hotmail.com
# @software: PyCharm
# @time: 2019/12/20 下午5:27
# @site: www.gongyanli.com
# @file: importer.py
import requests

from CookiesPool.cookiespool.db import RedisClient

conn = RedisClient('account', 'weibo')

def set(account, sep='----'):
    username, password = account.split(sep)
    result = conn.set(username, password)
    print('账号', username, '密码', password)
    print('录入成功' if result else '录入失败')


def scan():
    print('请输入账号密码组, 输入exit退出读入')
    while True:
        account = input()
        if account == 'exit':
            break
        set(account)


if __name__ == '__main__':
    scan()
