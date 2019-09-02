# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ProxyPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'dxdlspider':
            open('dxdl_proxy.txt','a').write(item['addr']+'\n')   
        elif spider.name=='klispider':
            #我们直接将传来的addr写入文本
            open('kdl_proxy.txt','a').write(item['addr']+'\n')        
        return item
