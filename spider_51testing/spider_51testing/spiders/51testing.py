# -*- coding:utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from spider_51testing.items import Spider51TestingItem
from scrapy.selector import Selector
import re


class Spider51Testing(CrawlSpider):
    name = 'Spider51Testing'
    allowed_domains = ['51testing.com']
    start_urls = [
        # 'http://www.51testing.com/?action-viewnews-itemid-4422050']
        'http://www.51testing.com/?action-viewnews-itemid-0000001']

    # start_urls = [
    #     'http://nc.mofcom.gov.cn/channel/gxdj/jghq/jg_list.shtml?craft_index=13196&par_craft_index=13080']

    rules = [
        Rule(LinkExtractor(allow=('/?action-viewnews-itemid-\d{1,}')),
             callback='parse_item',
             follow=True)
    ]

    def parse_item(self, response):
        item = Spider51TestingItem()
        print("-----------:", response.url)
        if response.url != 'http://www.51testing.com/html/index.html':
            if response.xpath('//div[@class="column_jtwz"]/h3/text()').extract() != '':
                title = response.xpath('//div[@class="column_jtwz"]/h3/text()').extract()[0]
                info = response.xpath('//div[@class="column_jtwz"]/p[@class="fabiao"]/text()').extract()
                tag = response.xpath('//div[@class="column_jtwz"]/p[@class="ziti"]/span/a/text()').extract()
                content = response.xpath('//div[@class="column_jtwz"]/div[@id="articlebody"]')
                content = content.xpath('string(.)').extract()[0].strip().replace('\r\n', '')

                infos = ''.join(info).split('\xa0')

                item['title'] = title
                item['date_time'] = infos[0]
                item['author'] = infos[1]
                item['source'] = infos[2]
                item['tag'] = ' '.join(tag)
                item['content'] = content
                item['url'] = response.url

                yield item
