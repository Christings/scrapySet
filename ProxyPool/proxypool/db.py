#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @contact: voidqueens@hotmail.com
# @software: PyCharm
# @time: 2019/12/25 下午12:33
# @site: www.gongyanli.com
# @file: db.py
import redis
from random import choice
from ProxyPool.proxypool.error import PoolEmptyError
from ProxyPool.proxypool.setting import *
import re


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        '''
        初始化
        :param host: 地址
        :param port: 端口
        :param password: 密码
        '''
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        '''
        添加代理，设置分数为最高
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        '''

        # if not self.db.zscore(REDIS_KEY, proxy):
        #     return self.db.zadd(REDIS_KEY, score, proxy)
        # zadd方法变更修复
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            print('代理不符合规范', proxy, '丢弃')
            return
        if not self.db.zscore(REDIS_KEY, proxy):
            dic = {}
            dic[proxy] = score

            return self.db.zadd(REDIS_KEY, dic)


    def random(self):
        '''
        随机获取有效代理，首先尝试获取最高分数，如果不存在，按照排名获取，否则异常
        :return: 随机代理
        '''
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        '''
        代理值减一分，小于最小值则删除
        :param proxy: 代理
        :return: 修改后的代理分数
        '''
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            # return self.db.zincrby(REDIS_KEY,proxy,-1)
            # 更新为redis3.0+版本，解决redis3.0更新后的报错，如用旧版本还原上方代码
            return self.db.zincrby(REDIS_KEY, -1, proxy)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        '''
        判断是否存在
        :param proxy: 代理
        :return: 是否存在
        '''
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        '''
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        '''
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        # return self.db.zadd(REDIS_KEY,MAX_SCORE,proxy)
        # 更新为redis3.0+版本，解决redis3.0更新后的报错，如用旧版本还原上方代码
        return self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})

    def count(self):
        '''
        获取数量
        :return: 数量
        '''
        return self.db.zcard(REDIS_KEY)

    def all(self):
        '''
        获取全部代理
        :return: 全部代理列表
        '''
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        '''
        批量获取
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        '''
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)


if __name__ == '__main__':
    conn = RedisClient()
    conn.add('10.134.109.49:9090',100)
    result = conn.batch(680, 688)
    print(result)
