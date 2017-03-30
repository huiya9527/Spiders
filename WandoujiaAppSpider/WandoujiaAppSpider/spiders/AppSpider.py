# coding:utf-8

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from WandoujiaAppSpider.items import WandoujiaappspiderItem

class AppSpider(CrawlSpider):
    name = "wandoujia"
    allowed_domains = ["wandoujia.com"]
    start_urls = ['http://www.wandoujia.com']
    rules = (
        Rule(LinkExtractor(allow='^http://www.wandoujia.com/apps/.*',
                           deny='^http://www.wandoujia.com/apps/.*/comment\d*'),
             callback="parse_apps",
             follow=True),
        Rule(LinkExtractor(),
             follow=True)
    )

    def parse_apps(self, response):
        item = WandoujiaappspiderItem()
        item['name'] = self.get_common_message(response, xpath_str="//p[@class='app-name']/span/text()")
        item['package'] = response.url.split('/')[-1]
        item['category'] = self.get_common_message(response, xpath_str="//div[@class='second']/a/span/text()")
        item['description'] = self.get_common_message(response, xpath_str="//div[@class='desc-info']/div/text()")
        item['comments'] = self.get_common_message(response, xpath_str="//div[@class='editorComment']/div/text()")
        item['like_num'] = self.get_common_message(response, xpath_str="//span[@class='item love']/i/text()")
        item['install_num'] = self.get_common_message(response, xpath_str="//span[@class='item']/i/text()")
        item['url'] = response.url
        item['classification'] = self.get_multi_common_message(response, xpath_str="//dd[@class='tag-box']/a/text()")
        item['tags'] = self.get_multi_common_message(response, xpath_str="//div[@class='side-tags clearfix']/div[@class='tag-box']/a/text()")
        item['update_time'] = self.get_common_message(response, xpath_str="//time[@id='baidu_time']/text()")
        item['source'] = self.get_common_message(response, "//a[@class='dev-sites']/span/text()")
        return item

    def get_common_message(self, response, xpath_str):
        re_value = response.xpath(xpath_str).extract()
        if len(re_value) >= 1:
            return re_value[0]
        return ''

    def get_multi_common_message(self, response, xpath_str):
        mid_value_list = response.xpath(xpath_str).extract()
        re_value = ""
        for i in mid_value_list:
            s = i.strip()
            re_value += (s + '\3')
        return re_value.strip('\3')