# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YingyongbaoappspiderItem(scrapy.Item):
    name = scrapy.Field()
    package = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    download_num = scrapy.Field()
    developer = scrapy.Field()
    url = scrapy.Field()
    pic_url = scrapy.Field()
