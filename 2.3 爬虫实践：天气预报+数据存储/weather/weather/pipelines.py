# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests



class WeatherPipeline(object):
    def process_item(self, item, spider):
        # 获取当前工作目录
        base_dir = os.getcwd()
        # 文件存在data目录下的weather.txt文件内
        fiename =  r"/".join(base_dir.split("\\")) + '/data/weather.txt'

        # 从内存以追加的方式打开文件，并写入对应的数据
        with open('data/weather.txt', 'a') as f:
            
            f.write(item['date'] + '\n')
            f.write(item['week'] + '\n')
            f.write(item['temperature'] + '\n')
            f.write(item['weather'] + '\n')
            f.write(item['wind'] + '\n\n')

        # 下载图片
        with open( 'data/' + item['date'] + '.png', 'wb') as f:
            f.write(requests.get(item['img'],stream=True).content)
        return item
