#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @contact: voidqueens@hotmail.com
# @software: PyCharm
# @time: 2019/12/24 下午2:48
# @site: www.gongyanli.com
# @file: api.py
import json
from flask import Flask, g
from cookiespool.config import *
from cookiespool.db import *

__all__ = ['app']

app = Flask(__name__)

@app.route('/')
def index():
    return '<h2>Welcome to Cookie Pool System</h2>'


def get_conn():
    '''
    获取
    :return:
    '''
    for website in GENERATOR_MAP:
        print(website)
        if not hasattr(g, website):
            setattr(g, website + '_cookies', eval('RedisClient' + '("cookies","' + website + '")'))
            setattr(g, website + '_accounts', eval('RedisClient' + '("accounts","' + website + '")'))
    return g


@app.route('/<website>/random')
def random(website):
    '''
    获取随机的 Cookie,访问地址如 /weibo/random
    :param website:
    :return: 随机 Cookie
    '''
    g = get_conn()
    cookies = getattr(g, website + '_cookies').random()
    return cookies


@app.route('/<website>/add/<username>/<password>')
def add(website, username, password):
    '''
    添加用户，访问地址如 /weibo/add/user/password
    :param website: 站点
    :param username: 用户名
    :param password: 密码
    :return:
    '''
    g = get_conn()
    print(username, password)
    getattr(g, website + '_accounts').set(username, password)
    return json.dumps({'status': '1'})


@app.route('/<website>/count')
def count(website):
    '''
    获取 Cookies 总数
    :param website:
    :return:
    '''
    g = get_conn()
    count = getattr(g, website + '_cookies').count()
    return json.dumps({'status': '1', 'count': count})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
