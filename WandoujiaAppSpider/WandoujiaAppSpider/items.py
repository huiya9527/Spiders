# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WandoujiaappspiderItem(scrapy.Item):
    name = scrapy.Field()
    package = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    comments = scrapy.Field()
    like_num = scrapy.Field()
    install_num = scrapy.Field()
    url = scrapy.Field()
    classification = scrapy.Field()
    tags = scrapy.Field()
    update_time = scrapy.Field()
    source = scrapy.Field()
