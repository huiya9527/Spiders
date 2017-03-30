# coding:utf-8

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from YingyongbaoAppSpider.items import YingyongbaoappspiderItem

class AppSpider(CrawlSpider):
    name = "yingyongbao"
    allowed_domains = ["sj.qq.com"]
    start_urls = ['http://sj.qq.com/']
    rules = (
        Rule(LinkExtractor(allow=('/myapp/detail\.htm\?apkName=.*',),), callback="parse_apps", follow=True),
        Rule(LinkExtractor(), follow=True)
    )

    def parse_apps(self, response):
        item = YingyongbaoappspiderItem()
        item['name'] = self.get_common_message(response, xpath_str="//div[@class='det-name-int']/text()")
        item['package'] = response.url.split('=')[-1]
        item['category'] = self.get_common_message(response, xpath_str="//div[@class='det-type-box']/a/text()")
        item['description'] = self.get_common_message(response, xpath_str="//div[@class='det-app-data-info']/text()")
        item['download_num'] = self.get_common_message(response, xpath_str="//div[@class='det-ins-num']/text()")
        item['developer'] = self.get_developer(response)
        item['url'] = response.url
        item['pic_url'] = self.get_common_message(response, xpath_str="//div[@class='det-icon']/img/@src")
        return item

    def get_common_message(self, response, xpath_str):
        re_value = response.xpath(xpath_str).extract()
        if len(re_value) >= 1:
            return re_value[0]
        return ''

    # TODO:解析没搞懂
    def get_developer(self, response):
        like_num = response.xpath("//div[@class='det-othinfo-data']/text()").extract()
        if len(like_num) >= 2:
            return like_num[1].encode('utf-8')
        return ''
