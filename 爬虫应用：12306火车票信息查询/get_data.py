# -*- coding: utf-8 -*-
'''
查询两站之间的火车票信息

输入参数： <date> <from> <to>

12306 api:
'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2017-07-18&leftTicketDTO.from_station=NJH&leftTicketDTO.to_station=SZH&purpose_codes=ADULT'

'''
import requests
from bs4 import BeautifulSoup
import urllib


def get_html(url):
    try:
        r=requests.get(url,timeout=15)
        r.raise_for_status()
        #r.encoding=r.apparent_encoding
    except:
        print("something wrong!")

    return r,text

def get_query_url(text):
    i=0
    while i==0:
        try:
            args=text.split(" ")
            from_station_name=args[0]
            to_station_name=args[1]
            data=args[2]
            from_station_code=station[from_station_name]
            to_station_code=station[to_station_name]
            i=1
        except:
            print("请检查输入的地点名称并重新输入:")
            text=input()
            i=0
    #url=('https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs={},{}'
    #     '&ts={},{}'
    #     '&date={}'
    #     '&flag=N,N,Y').format(urllib.parse.quote(from_station_name),from_station_code,urllib.parse.quote(to_station_name),to_station_code,data)
    url=('https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}'
         '&leftTicketDTO.from_station={}'
         '&leftTicketDTO.to_station={}'
         '&purpose_codes=ADULT').format(data,from_station_code,to_station_code)
    return url

def query_train_info(url,code_dict):
    info_lists=[]
    print(url)
    r=requests.get(url,timeout=15)

    trains=r.json()['data']['result']
    for train in trains:
        data_list=train.split('|')
        train_num =data_list[3]

        start_station_code = data_list[6]
        end_station_code = data_list[7]
        start_station_name = code_dict[start_station_code]
        end_station_name = code_dict[end_station_code]

        start_time = data_list[8]
        end_time = data_list[9]
        duration = data_list[10]

        super_seat = data_list[32] or '--'  # 商务/特等座
        first_seat = data_list[31] or '--'  # 一等座
        second_seat = data_list[30] or '--'  # 二等座
        soft_sleep = data_list[23] or '--'  # 软卧
        hard_sleep = data_list[28] or '--'  # 硬卧
        hard_seat = data_list[29] or '--'  # 硬座
        no_seat = data_list[26] or '--'  # 无座

        info_list = ('车次:{}\t出发站:{}\t目的地:{}\t出发时间:{}\t到达时间:{}\t历时:{}\n'
                     '商务座特等座:{}\t一等座:{}\t二等座:{}\t软卧:{}\t硬卧:{}\t硬座:{}\t无座:{}\n'
                     '-----------------------------------------------------------------------\n'
                     .format(train_num, start_station_name, end_station_name, start_time, end_time, duration,
                        super_seat, first_seat, second_seat, soft_sleep, hard_sleep, hard_seat, no_seat))
        print(info_list)
        info_lists.append(info_list)
        with open("query_infos.txt",'a+') as query_infos:
            query_infos.write(info_list)

# 关闭https证书验证警告
requests.packages.urllib3.disable_warnings()

# 城市名代码查询字典
# key：城市名 value：城市代码
f=open("station.txt","r")
station=eval(f.read())
f.close()
code_dict={v:k for k,v in station.items()}

print("请输入要查询的信息，示例："+'\n'+'北京 上海 2019-08-22')
text=input()

url=get_query_url(text)
query_train_info(url,code_dict)




'''
    soup=BeautifulSoup(r.text, 'lxml')

    tlist=soup.find('div',id='t-list')
    queryLeftTable=tlist.find('tbody',id='queryLeftTable')
    infos=queryLeftTable.find_all('tr')
    print('tlist是',tlist)
    print('queryLeftTable是',queryLeftTable)
    for info in infos:
        train=info.find('div',class_='train')
        train_num=train.find('a').text

        cdz=info.find('div',class_='cdz')
        start_station=cdz.find('strong',class_='start-s').text
        end_station=cdz.find('strong',class_='end-s').text

        cds=info.find('div',class_='cds')
        start_time=cds.find('strong',class_='start-t').text
        end_time=cdz.find('strong',class_='color999').text

        ls=info.find('div',class_='ls')
        duration=ls.find('strong').text+ls.find('span').text

        surplus=info.find_all('td')[1:-2]
        if len(surplus)!=10:
            print("something wrong!(2)")
        super_seat=surplus[0].text
        first_seat=surplus[1].text
        second_seat=surplus[2].text
        super_soft_sleep=surplus[3].text
        first_soft_sleep=surplus[4].text
        dong_soft_sleep=surplus[5].text
        second_hard_sleep=surplus[6].text
        soft_seat=surplus[7].text
        hard_seat=surplus[8].text
        no_seat=surplus[9].text

        info_list=('车次:{}\t出发站:{}\t目的地:{}\t出发时间:{}\t到达时间:{}\t历时:{}\n'
                   '商务座特等座:{}\t一等座:{}\t二等座:{}\t高级软卧:{}\t软卧一等卧:{}\t动卧:{}\t硬卧二等卧:{}\t软座:{}\t硬座:{}\t无座:{}\n'
                   '------------------------------------------------------------------'.format(train_num,start_station,end_station,start_time,end_time,duration,
                    super_seat,first_seat,second_seat,super_soft_sleep,first_soft_sleep,dong_soft_sleep,second_hard_sleep,soft_seat,hard_seat,no_seat))
'''
