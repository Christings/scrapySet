#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @contact: voidqueens@hotmail.com
# @software: PyCharm
# @time: 2019/12/26 下午7:34
# @site: www.gongyanli.com
# @file: importer.py
from ProxyPool.proxypool.db import RedisClient

conn = RedisClient()


def set(proxy):
    result = conn.add(proxy)
    print('录入成功' if result else '录入失败')


def scan():
    print('请输入代理，输入exit退出读取')
    while True:
        proxy = input()
        if proxy == 'exit':
            break
        set(proxy)


if __name__ == '__main__':
    scan()
