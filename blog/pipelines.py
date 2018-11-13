# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import MySQLdb
from scrapy.conf import settings

class BlogPipeline(object):
    def __init__(self):

        self.conn = MySQLdb.connect(host="127.0.0.1",user="root",passwd="richardtt",db="blog",charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # postItem = dict(item)  
        # self.coll.insert(postItem) 
        # return item  
        sql = "INSERT INTO `blog`.`article` (`artid`, `author`, `tiitle`, `content`, `atime`, `views`, `like`, `arturl`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s);"
        params = (item['name'], item['title'], item['content'], item['time'], item['view'], item['like'], item['arturl'])
        self.cursor.execute(sql,params)
        self.conn.commit()

