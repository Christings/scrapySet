# -*- coding:utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
from labor.items import SinaSpiderItem


# 全国农产品价格数据
class SinaSpider(scrapy.Spider):
    name = 'SinaSpider'
    # allowed_domains = ['nc.mofcom.gov.cn/channel/']
    base_url = "https://search.sina.com.cn/news?q={}&c=news&range=title&size=20&dpc=0&ps=0&pf=0&page={}"
    # base_url = "https://search.sina.com.cn/news?q={}c=news&size=20&page={}"

    # start_urls = [
    #     'http://nc.mofcom.gov.cn/channel/gxdj/jghq/jg_list.shtml?craft_index=13196&par_craft_index=13080']

    # rules = [
    #     Rule(LinkExtractor(allow=('/')),
    #          callback='parse_item',
    #          follow=True)
    # ]

    def start_requests(self, keyword="劳动合同纠纷"):
        #  可修改  这里设置爬取100页
        page_total = 8
        keyword = keyword
        for page in range(1, page_total + 1):
            #  按上面注释  可修改 这里"2509"代表"全部"类别的新闻
            yield Request(self.base_url.format(keyword, page),callback=self.parse)

    def parse(self, response):
        # result = json.loads(response.text)
        urls = response.xpath('//div[@class="box-result clearfix"]/h2/a/@href').extract()
        for url in urls:
            item=SinaSpiderItem()
            item["url"]=url
            yield scrapy.Request(url=url, callback=self.parse_item,meta={"item":item})

    def parse_item(self, response):
        item =response.meta['item']

        title = response.xpath('//h1[@class="main-title"]/text()').extract()

        ctime = response.xpath('//div[@class="date-source"]/span/text()').extract()
        media_name = response.xpath('//div[@class="date-source"]/a/text()').extract()
        ori_url=response.xpath('//div[@class="date-source"]/a/@href').extract()
        keywords = response.xpath('//div[@class="keywords"]/a/text()').extract()

        # content = ''.join(response.xpath('//*[@id="artibody" or @id="article"]//p/text()').extract())

        content = response.xpath('//*[@id="artibody" or @id="article"]//p')
        content = ''.join(content.xpath("string(.)").extract())
        content = re.sub(r'\u3000', '', content)
        content = re.sub(r'[ \xa0?]+', ' ', content)
        content = re.sub(r'\s*\n\s*', '\n', content)
        content = re.sub(r'\s*(\s)', r'\1', content)
        content = ''.join([x.strip() for x in content])

        item['ctime'] = ctime
        item['ori_url'] = ori_url
        item['title'] = title
        item['media_name'] = media_name
        item['keywords'] = keywords
        item['content'] = content

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
