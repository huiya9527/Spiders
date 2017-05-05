# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import logging

class MyspiderPipeline(object):

    # def __init__(self, mysql_address, mysql_user, mysql_password, mysql_schema):
    #     self.address = mysql_address
    #     self.user = mysql_user
    #     self.password = mysql_password
    #     self.schema = mysql_schema

    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         mysql_address = crawler.settings.get('mysql_address'),
    #         mysql_user = crawler.settings.get('mysql_user'),
    #         mysql_password = crawler.settings.get('mysql_password'),
    #         mysql_schema = crawler.settings.get('mysql_schema')
    #     )
    #
    # def open_spider(self, spider):
    #     self.db = MySQLdb.connect(self.address, self.user, self.password, self.shema)

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()

    def __init__(self):
        logging.basicConfig(filename='D:\\GitHub\\OriginData\\MySpider\\pipeline_log.txt',level=logging.DEBUG)
        self.db = MySQLdb.connect(host="localhost",user="root",passwd="123456",db="myspider",charset='utf8')
        self.db.autocommit(1)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        sql = "insert into news (type, title, url, content, time, comments_num) values(\'" +\
                item['news_type'] + "\',\'" +\
                item['news_title'] + "\',\'" +\
                item['news_url'] + "\',\'" +\
                item['news_content'] + "\',\'" +\
                item['news_time'] + "\'," +\
                str(item['news_comments_num']) +")"
        try:
            self.cursor.execute(sql)
        except Exception, e:
            logging.warning(e)
        return None
