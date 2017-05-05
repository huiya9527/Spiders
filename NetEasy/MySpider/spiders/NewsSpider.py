# -*- coding: utf-8 -*-

import scrapy
import re
import json
import logging
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib2 import urlopen
from MySpider.items import MyspiderItem

class NewsSpider(CrawlSpider):
    name = "news"
    allowed_domains = ["news.163.com","sports.163.com","ent.163.com","money.163.com","tech.163.com","digi.163.com"]
    start_urls = ['http://www.163.com/']
    rules=(
        Rule(LinkExtractor(allow=('/16/\d{4}/\d+/*',)),
        callback="parse_news",follow=True),

        Rule(LinkExtractor(deny=('/special/*')),follow=True)
    )

    logging.basicConfig(filename='D:\\GitHub\\OriginData\\MySpider\\spider_log.txt',level=logging.DEBUG)

    def parse_news(self,response):
        item = MyspiderItem()
        item['news_type'] = self.get_news_type(response)
        item['news_title'] = self.get_news_title(response)
        item['news_content'] = self.get_news_content(response)
        item['news_time'] = self.get_news_time(response)
        item['news_comments_num'] = self.get_news_comments_num(response)
        item['news_url'] = self.get_news_url(response)
        return item;

    def get_news_type(self, response):
        strs = response.url
        return strs.split('/')[2].split('.')[0]

    def get_news_title(self, response):
        title = response.xpath("/html/head/title/text()").extract()
        if title:
            return title[0]

    def get_news_url(self, response):
        return response.url

    def get_news_content(self, response):
        news_body = response.xpath("//div[@id='endText']/p/text() | //div[@id='endText']/p/a/text()").extract()
        content = ""
        if news_body:
            for s in news_body:
                content += s.strip()
        return content

    def get_news_comments_num(self, response):
        scriptBody = response.xpath('//*[@id="post_comment_area"]/script[3]/text()').extract()
        if scriptBody:
            try:
                scriptBody = scriptBody[0]
                productKey = re.search("\"productKey\" : \"\w*\"",scriptBody)
                docId = re.search("\"docId\" : \"\w*\"",scriptBody)
                productKey = productKey.group(0)[16:-1]
                docId = docId.group(0)[11:-1]
                url = 'http://comment.news.163.com/api/v1/products/'+productKey+'/threads/'+docId
                body = urlopen(url)
                # Convert bytes to string type and string type to dict
                strs = body.read().decode('utf-8')
                json_obj = json.loads(strs)
                return json_obj['cmtVote'] # prints the string with 'source_name' key
            except Exception,e:
                logging.warning(e)
        else :
            return 0

    def get_news_time(self, response):
        s = response.xpath("//div[@class='post_time_source']/text()").extract()
        if s:
            s = s[0].strip()
            s = s[:-4]
            return s
        s = response.xpath("//div[@class='ep-time-soure cDGray']/text()").extract()
        if s:
            s = s[0].strip()
            s = s[:-4]
            return s
        s = 'get time failure'
        return s
