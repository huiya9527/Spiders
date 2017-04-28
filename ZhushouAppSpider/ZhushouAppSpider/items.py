# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhushouappspiderItem(scrapy.Item):
    name = scrapy.Field()
    package = scrapy.Field()
    description = scrapy.Field()
    comments = scrapy.Field()
    tags = scrapy.Field()
    download_num = scrapy.Field()
    url = scrapy.Field()
