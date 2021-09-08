# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class SinaSpiderItem(scrapy.Item):
    # define the fields for your item here like:

    collection = 'sina'

    ctime = Field()  # 发布时间
    url = Field()
    ori_url = Field()
    title = Field()  # 新闻标题
    media_name = Field()  # 发发布的媒体
    keywords = Field()  #  关键词
    content = Field()  #  新闻内容

class BaiduSpiderItem(scrapy.Item):
    # define the fields for your item here like:

    collection = 'sina'

    ctime = Field()  # 发布时间
    url = Field()
    ori_url = Field()
    title = Field()  # 新闻标题
    media_name = Field()  # 发发布的媒体
    keywords = Field()  #  关键词
    content = Field()  #  新闻内容

