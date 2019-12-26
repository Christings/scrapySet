#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @contact: voidqueens@hotmail.com
# @software: PyCharm
# @time: 2019/12/26 下午6:08
# @site: www.gongyanli.com
# @file: scheduler.py
import time
from multiprocessing import Process
from ProxyPool.proxypool.api import app
from ProxyPool.proxypool.getter import Getter
from ProxyPool.proxypool.tester import Tester
from ProxyPool.proxypool.db import RedisClient
from ProxyPool.proxypool.setting import *

TESTER_CYCLE = 20
GETTER_CYCLE = 20
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True


class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):
        test = Tester()
        while True:
            print('测试器开始运行')
            test.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        '''
        定时获取代理
        :param cycle:
        :return:
        '''
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        '''
        开启API
        :return:
        '''
        app.run(API_HOST, API_PORT)

    def run(self):
        print('代理池开始运行')
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()
