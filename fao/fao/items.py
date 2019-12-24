# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# FAO数据
class FaoCountriesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # geo_country1 = scrapy.Field()
    # geo_country2 = scrapy.Field()
    # geo_country3 = scrapy.Field()
    #
    # eco_country1 = scrapy.Field()
    # eco_country2 = scrapy.Field()
    # eco_country3 = scrapy.Field()

    first = scrapy.Field()
    second = scrapy.Field()
    third = scrapy.Field()