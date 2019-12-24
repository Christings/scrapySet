#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @contact: voidqueens@hotmail.com
# @software: PyCharm
# @time: 2019/12/20 下午6:36
# @site: www.gongyanli.com
# @file: tester.py
import json
import requests
from requests.exceptions import ConnectionError
from cookiespool.db import *


class ValidTester(object):
    def __init__(self, website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)

    def test(self, username, cookies):
        raise NotImplementedError

    def run(self):
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups.items():
            self.test(username, cookies)


class WeiboValidTester(ValidTester):
    def __init__(self, website='weibo'):
        ValidTester.__init__(self,website)

    def test(self, username, cookies):
        print('正在测试 Cookies ,', '用户名', username)

        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('Cookies 不合法', username)
            self.cookies_db.delete(username)
            print('删除 Cookies', username)
            return
        try:
            test_url = TEST_URL_MAP[self.website]
            response = requests.get(test_url, cookies=cookies, timeout=5, allow_redirects=False)
            if response.status_code == 200:
                print('Cookies 有效', username)
            else:
                print(response.status_code, response.headers)
                print('Cookies 失效', username)
                self.cookies_db.delete(username)
                print('删除 Cookies', username)
        except ConnectionError as e:
            print('发生异常', e.args)


if __name__ == '__main__':
    WeiboValidTester().run()
