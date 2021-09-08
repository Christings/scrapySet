# -*- coding:utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
from labor.items import BaiduSpiderItem


# 全国农产品价格数据
class BaiduSpider(scrapy.Spider):
    name = 'BaiduSpider'
    # base_url = "https://www.baidu.com/s?wd=%E7%99%BE%E5%BA%A6%20%E5%85%B3%E9%94%AE%E5%AD%97%E7%88%AC%E8%99%AB&pn=40"
    base_url = "https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&ie=utf-8&word={}&pn={}"

    # start_urls = [
    #     'http://nc.mofcom.gov.cn/channel/gxdj/jghq/jg_list.shtml?craft_index=13196&par_craft_index=13080']

    # rules = [
    #     Rule(LinkExtractor(allow=('/')),
    #          callback='parse_item',
    #          follow=True)
    # ]

    def start_requests(self, keyword="拖欠工资"):
        #  可修改  这里设置爬取100页
        page_total = 250
        keyword = keyword
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'Referer': 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&word=%B0%D9%B6%C8%D0%C2%CE%C5&fr=zhidao'
        }
        for page in range(0, page_total, 10):
            #  按上面注释  可修改 这里"2509"代表"全部"类别的新闻
            yield Request(self.base_url.format(keyword, page),headers=headers,callback=self.parse)

    def parse(self, response):
        results = response.xpath('//div[@class="result-op c-container xpath-log new-pmd"]')
        for result in results:
            url = result.xpath("div/h3/a/@href").extract()[0]
            ori_url = result.xpath("div/h3/a/@href").extract()[0]
            title = result.xpath(".//h3/a")
            title = title.xpath("string(.)").extract()[0]
            keywords = result.xpath('.//span[@class="c-font-normal c-color-text"]')[0]
            keywords = keywords.xpath("string(.)").extract()[0]
            
            infos = result.xpath('.//div[@class="news-source_Xj4Dv"]')[0]
            media_name = infos.xpath(".//span[last()-1]/text()").extract()[0]
            ctime = infos.xpath(".//span[last()]/text()").extract()[0]
            
            item=BaiduSpiderItem()
            item["url"] = url
            item['ctime'] = ctime
            item['ori_url'] = ori_url
            item['title'] = title
            item['media_name'] = media_name
            item['keywords'] = keywords
            yield scrapy.Request(url=url, callback=self.parse_item,meta={"item":item})

    def parse_item(self, response):
        item =response.meta['item']
        content = response.text
        content = re.sub(r'[^\u4e00-\u9fa5]', '', content)
        content = re.sub(r'设为首页使用百度前必读意见反馈京证号京公网安备号后端数据', '', content)
        content = re.sub(r'百度首页', '', content)
        content = re.sub(r'登录', '', content)
        item["content"]=content
        yield item


        # for each in products:
        #     product_name = each.xpath('td[1]/text()').extract()[0]
        #     product_price = each.xpath('td[2]/text()').extract()[0]
        #     product_market = each.xpath('td[3]/a/text()').extract()[0]
        #     product_releasedate = each.xpath('td[4]/text()').extract()[0]

        #     print("product_name:", product_name)
        #     print("product_price:", product_price)
        #     print("product_market:", product_market)
        #     print("product_releasedate:", product_releasedate)
        #     item = AllProductsPriceItem(product_name=product_name, product_price=product_price,
        #                                 product_market=product_market, product_releasedate=product_releasedate)
        #     yield item
        # next_page_string = response.xpath('//div[@class="pmCon"]/script/text()').extract()
        # next_page_temp = re.findall(r"v_PageCount = (.*?);", str(next_page_string))
        # next_page = str(next_page_temp).replace('[', '').replace(']', '').replace('\'', '')
        # print("next_page:", next_page)
        # for i in range(2,int(next_page)):
        #     print(response.url)
        #     url = response.url + "&page=" + str(i)
        #     print("请求的url:", url)
        #     yield scrapy.Request(url=url, callback=self.parse_item)

    # 提取出全国所有农产品的url
    # def parse(self, response):
    #     urls = response.xpath('//div[@class="s_Lmain clearfix"]/script/text()').extract()
    #     for url in urls:
    #         url = url.split('|')
    #         for each in url:
    #             product_url_tmp1 = re.findall(r"href=(.*?)>", str(each))
    #             product_url2 = str(product_url_tmp1).replace('[', '').replace(']', '').replace('\'', '')
    #             # print(product_url)
    #             product_url = 'http://nc.mofcom.gov.cn' + product_url2
    #             if product_url or product_url != "":
    #                 yield scrapy.Request(url=product_url, callback=self.parse_item)

    # def parse_item(self, response):
    #     products = response.xpath('//div[@class="pmCon"]/table/tbody/tr')
    #     for each in products:
    #         product_name = each.xpath('td[1]/text()').extract()[0]
    #         product_price = each.xpath('td[2]/text()').extract()[0]
    #         product_market = each.xpath('td[3]/a/text()').extract()[0]
    #         product_releasedate = each.xpath('td[4]/text()').extract()[0]

    #         print("product_name:", product_name)
    #         print("product_price:", product_price)
    #         print("product_market:", product_market)
    #         print("product_releasedate:", product_releasedate)
    #         item = AllProductsPriceItem(product_name=product_name, product_price=product_price,
    #                                     product_market=product_market, product_releasedate=product_releasedate)
    #         yield item
    #     next_page_string = response.xpath('//div[@class="pmCon"]/script/text()').extract()
    #     next_page_temp = re.findall(r"v_PageCount = (.*?);", str(next_page_string))
    #     next_page = str(next_page_temp).replace('[', '').replace(']', '').replace('\'', '')
    #     print("next_page:", next_page)
    #     for i in range(2,int(next_page)):
    #         print(response.url)
    #         url = response.url + "&page=" + str(i)
    #         print("请求的url:", url)
    #         yield scrapy.Request(url=url, callback=self.parse_item)
