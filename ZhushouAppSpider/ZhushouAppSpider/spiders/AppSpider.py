# coding:utf-8

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ZhushouAppSpider.items import ZhushouappspiderItem
import re


class AppSpider(CrawlSpider):
    name = "zhushou"
    allowed_domains = ["zhushou.360.cn"]
    start_urls = ['http://zhushou.360.cn']
    rules = (
        Rule(LinkExtractor(allow=('/detail/index/soft_id/\d+',)), callback="parse_apps", follow=True),
        Rule(LinkExtractor(), follow=True)
    )

    def parse_apps(self, response):
        item = ZhushouappspiderItem()
        item['name'] = self.get_common_message(response, xpath_str="//h2[@id='app-name']/span/text()")
        item['package'] = self.get_package(response)
        item['description'] = self.get_common_message(response, xpath_str="//div[@class='breif']/text()")
        item['comments'] = self.get_common_message(response, xpath_str="//dl[@class='clearfix']/dd/p/text()")
        item['download_num'] = self.get_common_message(response, xpath_str="//span[@class='s-3']/text()")
        item['tags'] = self.get_tags(response)
        item['url'] = response.url
        return item

    def get_common_message(self, response, xpath_str):
        re_value = response.xpath(xpath_str).extract()
        if len(re_value) >= 1:
            return re_value[0]
        return ''

    def get_package(self, response):
        content = response.xpath("//html").extract()[0]
        ss = re.search("pname.*", content)
        if ss and ss.group():
            package = ss.group(0)[9:-3]
            return package
        return ""

    def get_tags(self, response):
        tags = response.xpath("//div[@class='app-tags']/a/text()").extract()
        if len(tags) != 0:
            ss = "\3".join(tags)
            return ss
        return ""