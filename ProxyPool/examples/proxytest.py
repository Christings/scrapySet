#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @contact: voidqueens@hotmail.com
# @software: PyCharm
# @time: 2019/12/26 下午8:19
# @site: www.gongyanli.com
# @file: proxytest.py
import requests
from ProxyPool.proxypool.setting import TEST_URL

proxy = '96.9.90.90:8080'

proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy,
}

print(TEST_URL)
response = requests.get(TEST_URL, proxies=proxies, verify=False)
if response.status_code == 200:
    print('Successfully')
    print(response.text)