# -*- coding: utf-8 -*-
'''
抓取bilibili视频弹幕
制作词云
分析词频
'''
import requests
from bs4 import BeautifulSoup
import jieba
from wordcloud import WordCloud as wc
import pandas as pd

def get_data(url):
    '''
    抓取弹幕
    :param url:
    :return:
    '''
    barranges_list=[]
    r=requests.get(url,timeout=15)
    r.raise_for_status()
    r.encoding=r.apparent_encoding

    soup=BeautifulSoup(r.text,'lxml')
    barranges=soup.find_all('d')
    for barrange in barranges:
        barranges_list.append(barrange.text)

    with open('barranges.txt','w') as f:
        f.write('\n'.join(barranges_list))
    return barranges_list

def removal(barranges):
    '''
    弹幕去重操作
    results_list -- 去重后弹幕
    repeat_list -- 重复弹幕
    :param data:
    :return:
    '''
    results_list=[]
    repeat_list=[]

    for barrange in barranges:
        if barrange not in results_list:
            results_list.append(barrange)
        else:
            repeat_list.append(barrange)

    with open('results.txt','w') as results:
        results.write('\n'.join(results_list))
    with open('repeat.txt','w') as repeat:
        repeat.write('\n'.join(repeat_list))

    return results_list,repeat_list

def make_wordCould(barranges_list):
    #制作词云
    stop_words = ['【', '】', ',' , '，', '.', '?','？', '！','!', '。']
    words = []
    for barrange in barranges_list:
        for stop in stop_words:
            # 去除上面的停用词，再拼接成字符串
            barrange = ''.join(barrange.split(stop))
        words.append(barrange)
        # 列表拼接成字符串
    words = ''.join(words)
    words = jieba.cut(words)
    words = ' '.join(words)

    w = wc(font_path='‪C:/Windows/Fonts/SIMYOU.TTF', background_color='white', width=1600, height=1600, max_words=2000)
    w.generate(words)
    w.to_file('wordcould.jpg')

    return words

print('请输入想要爬取的弹幕链接')
url=input() or 'https://api.bilibili.com/x/v1/dm/list.so?oid=112467603'
barranges_list = get_data(url)
results_list,repeat_list = removal(barranges_list)
words=make_wordCould(barranges_list)
# 统计词频
words_list = words.split(' ')
words_num = pd.value_counts(words_list)

words_num_dict={'words_num':words_num.index,'num':words_num.values}
words_num_pd = pd.DataFrame(words_num_dict)
words_num_pd.to_csv('words_num.txt')

