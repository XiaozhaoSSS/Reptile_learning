# -*- coding: utf-8 -*-
import scrapy
from proxy.items import ProxyItem

class KlispiderSpider(scrapy.Spider):
    name = 'klispider'
    allowed_domains = ['www.kuaidaili.com']
    start_urls = []
    for i in range(1,6):
        start_urls.append('http://kuaidaili.com/free/inha/'+str(i)+'/')
    
    def parse(self, response):
        item = ProxyItem()
        mian=response.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
        
        for li in mian:
            #找到ip地址
            ip = li.xpath('td/text()').extract()[0]
            #找到端口：
            port =li.xpath('td/text()').extract()[1]
            #将两者连接，并返回给item处理
            item['addr'] = ip+':'+port
            yield item