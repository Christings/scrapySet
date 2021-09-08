# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from typing import Text
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from twisted.internet.defer import DeferredLock
import requests
import json
from model import IPProxyModel
import random

from fake_useragent import UserAgent


#随机UA
class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = UserAgent()
        request.headers['User-Agent'] = ua.random


class ProxyMiddlleWare(object):
    def __init__(self):
        # self.IP_URL_GET = r"http://127.0.0.1:8000/?types=0&count=5&country=国内"
        self.IP_URL_GET = r"http://127.0.0.1:8000"

        self.IP_URL_DELETE = r"http://127.0.0.1:8000/delete?ip="
        super(ProxyMiddlleWare, self).__init__()

    def process_request(self, request, spider):
        # 得到地址
        proxy = self.get_Random_Proxy()
        print(proxy + "**********")
        # 设置代理
        request.meta['proxy'] = "http://" + proxy

    #这个方法是从文档中读取id地址
    def get_Random_Proxy(self):
        response = requests.get(self.IP_URL_GET)
        result = json.loads(response.text)
        proxy = random.choice(result)
        proxy = proxy[0] + ":" + str(proxy[1])
        return proxy

    def process_response(self, request, response, spider):
        #如果该ip不能使用，更换下一个ip
        if response.status != 200:
            # ip=request.meta['proxy'].split("//")[1].split(":")[0]
            # requests.get(self.IP_URL_DELETE+str(ip))
            # print('删除ip' + ip)
            proxy = self.get_Random_Proxy()
            print('更换ip' + proxy)
            request.meta['proxy'] = "http://" + proxy
            return request
        return response


class IPProxyDownloaderMiddleware(object):
    '''
    IP代理 ，
    '''
    # 获取代理ip信息地址 例如芝麻代理、快代理等
    IP_URL = r'http://127.0.0.1:8000/?types=0&count=1&country=国内'

    def __init__(self):
        # super(IPProxyDownloaderMiddleware, self).__init__(self)
        super(IPProxyDownloaderMiddleware, self).__init__()

        self.current_proxy = None
        self.lock = DeferredLock()

    def process_request(self, request, spider):
        if 'proxy' not in request.meta or self.current_proxy.is_expire:
            self.updateProxy()

        request.meta['proxy'] = self.current_proxy.address

    def process_response(self, request, response, spider):
        if response.status != 200:
            # 如果来到这里，这个请求相当于被识别为爬虫了
            # 所以这个请求被废掉了
            # 如果不返回request,那么这个请求就是没有获取到数据
            # 返回了request，那么这个这个请求会被重新添加到调速器
            if not self.current_proxy.blacked:
                self.current_proxy.blacked = True
                print("被拉黑了")
            self.updateProxy()
            return request
        # 正常的情况下，返回response
        return response

    def updateProxy(self):
        '''
        获取新的代理ip
        :return:
        '''
        # 因为是异步请求，为了不同时向芝麻代理发送过多的请求这里在获取代理IP
        # 的时候，需要加锁
        self.lock.acquire()
        if not self.current_proxy or self.current_proxy.is_expire or self.current_proxy.blacked:
            response = requests.get(self.IP_URL)
            text = response.text

            # # 返回值 {"code":0,"success":true,"msg":"0","data":[{"ip":"49.70.152.188","port":4207,"expire_time":"2019-05-28 18:53:15"}]}
            # text=text.split(',')
            
            jsonString = json.loads(text)

            data = jsonString['data']
            if len(data) > 0:
                proxyModel = IPProxyModel(data=data[0])
                self.current_proxy = proxyModel
        self.lock.release()


class LaborSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LaborDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
