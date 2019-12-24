# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from fao.items import FaoCountriesItem
import json


class FaoPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, FaoCountriesItem):
            with open('fao.json', 'wb') as fp:
                json.dump(item, fp=fp, indent=4)
                return item
