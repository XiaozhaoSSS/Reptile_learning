# -*- coding: utf-8 -*-
import scrapy
from weather.items import WeatherItem

class TianqiSpider(scrapy.Spider):
    name = 'tianqi'
    allowed_domains = ['www.tianqi.com']
    start_urls = []
    citys=['nanjing', 'suzhou', 'shanghai']
    for city in citys:
        start_urls.append('http://tianqi.com/'+city+'/')
    def parse(self, response):
        item = WeatherItem()
        '''
        
        item['date']=[]
        item['week']=[]
        item['img']=[]
        item['temperature']=[]
        item['weather']=[]
        item['wind']=[]
        '''
        dates=response.xpath('//div[@class="day7"]/ul[@class="week"]/li')
        weas=response.xpath('//div[@class="day7"]/ul[@class="txt txt2"]/li')
        winds=response.xpath('//div[@class="day7"]/ul[@class="txt"]/li')
        tems=response.xpath('//div[@class="day7"]/div[@class="zxt_shuju"]/ul/li')
        for date,wea,wind,tem in zip(dates,weas,winds,tems):
            item['date']=date.xpath('b/text()').extract()[0]
            item['week']=date.xpath('span/text()').extract()[0]
            item['img']=date.xpath('img/@src').extract()[0]
            item['weather']=wea.xpath('text()').extract()[0]
            item['wind']=wind.xpath('text()').extract()[0]
            high_tem=tem.xpath('span/text()').extract()[0]
            low_tem=tem.xpath('b/text()').extract()[0]
            item['temperature']=(str(low_tem)+'-'+str(high_tem))
            yield item
