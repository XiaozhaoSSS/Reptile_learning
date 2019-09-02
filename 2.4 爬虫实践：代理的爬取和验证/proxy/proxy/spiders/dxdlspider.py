# -*- coding: utf-8 -*-
import scrapy
from proxy.items import ProxyItem

class DxdlspiderSpider(scrapy.Spider):
    name = 'dxdlspider'
    allowed_domains = ['www.xicidaili.com']
    start_urls = ['http://xicidaili.com/']

    def parse(self, response):
        item = ProxyItem()
        mian=response.xpath('//table[@id="ip_list"]/tbody/tr[@class="odd"]')
        #mian=response.xpath('//tr[@class="odd"]')
        for li in mian:
            #找到ip地址
            ip = li.xpath('td/text()').extract()[0]
            #找到端口：
            port =li.xpath('td/text()').extract()[1]
            #将两者连接，并返回给item处理
            item['addr'] = ip+':'+port
            yield item
            