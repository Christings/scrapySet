# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from spider_51testing.db.Mysql import Mysql
from spider_51testing.items import Spider51TestingItem
import pymysql

import logging

logger = logging.getLogger(__name__)

def update_errorlog(log):
    log = log.replace("'", "\\'")
    db = pymysql.connect(database_host,database_user,database_pass,database)
    cursor = db.cursor()
    sql = "UPDATE %s set errorlog=CONCAT(errorlog, '%s') where id=%d;" % ('fanyi_interfaceeval', log, task_id)
    cursor.execute(sql)
    data = cursor.fetchone()
    logstr.log_info(str(task_id)+"\t"+log)
    try:
        db.commit()
    except:
        logstr.log_debug("error")


class Spider51TestingPipeline(object):
    def process_item(self, item, spider):
        print(logging.log(logging.WARNING,'111111'))
        print('1111:',logging.warning(item))

        if isinstance(item, Spider51TestingItem):
            print(logging.log(logging.WARNING, '2222'))
            print('2222:', logging.warning(Spider51TestingItem))
            mysql = Mysql(host='10.134.110.163', user='root', pwd='Websearch@qa66', db='51testing')
            if len(item['title']) == 0:
                print('insert failed')
            else:
                newsql = "insert into article_copy2(title,date_time,author,source,tag,content,url)VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (
                    item['title'], item['date_time'], item['author'], item['source'], item['tag'], pymysql.escape_string(item['content']),item['url']
                )
                print('insert success')
                mysql.ExecNoQuery(newsql.encode('utf-8'))
        else:
            pass
        return item
