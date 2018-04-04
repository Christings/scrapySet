# -*- coding:utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from ..items import FaoCountriesItem
import time


class FaoCountriesSpier(scrapy.Spider):
    name = "faocountries"
    start_urls = ["http://www.fao.org/countryprofiles/geographic-and-economic-groups/en/"]

    # def start_requests(self):
    #     yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        # 通过selenium打开chrome内核，从而获得网页加载后的源代码。
        print("1:", response.body)

        a = response.xpath('//div[@id="groups-list"]/div/h3/text()').extract()  # 最外层三个
        b = response.xpath('//div[@id="groups-list"]/div/div/h4/text()').extract()  # 中间层
        c = response.xpath('//div[@id="groups-list"]/div/div/ul/li/a/text()').extract()  # 最里层
        x = response.body
        soup = BeautifulSoup(x, 'lxml')
        secondtitles = soup.select("div.divgroup h4")

        item = FaoCountriesItem()
        for each in a:
            item["first"] = each
            print("first:", each)
            if each == a[0]:
                # print("第一个")
                for t in secondtitles:
                    if 'geo' in t.get("rel"):
                        ul_id = "ul_" + t.get("rel")
                        # print(ul_id)
                        item["second"] = t.string
                        print("second:" + item["second"])
                        content = soup.select("ul#" + ul_id + " li a")
                        for i in content:
                            item['third'] = i.string

                            yield item
            if each == a[1]:
                # print("第2个")
                for t in secondtitles:
                    if 'eco' in t.get("rel"):
                        ul_id = "ul_" + t.get("rel")
                        # print(ul_id)
                        item["second"] = t.string
                        print("second:" + item["second"])
                        content = soup.select("ul#" + ul_id + " li a")
                        for i in content:
                            item['third'] = i.string
                            print("third:", i.string)
                            yield item
            if each == a[2]:
                # print("第3个")
                for t in secondtitles:
                    if 'spe' in t.get("rel"):
                        ul_id = "ul_" + t.get("rel")
                        # print(ul_id)
                        item["second"] = t.string
                        print("this is secondtitle:" + item["second"])
                        content = soup.select("ul#" + ul_id + " li a")
                        for i in content:
                            item['third'] = i.string
                            print("third:", i.string)
                            yield item