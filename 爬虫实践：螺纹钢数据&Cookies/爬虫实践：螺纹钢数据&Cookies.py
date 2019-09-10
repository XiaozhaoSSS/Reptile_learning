# -*- coding: utf-8 -*-
# hello.py
'''
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'<h1>Hello, web!</h1>']
'''
'''
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    body = '<h1>Hello, %s!</h1>' % (environ['PATH_INFO'][1:] or 'web')
    return [body.encode('utf-8')]
'''
import requests
from bs4 import BeautifulSoup
import re


def get_html(url, cookies):
    try:
        r = requests.get(url, cookies=cookies, timeout=30)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "Someting Wrong！"


def get_url():
    urls = []

    for i in range(1, 50):
        nextpage = 'https://list1.mysteel.com/market/p-221-0----0101-0--------' + str(i) + '.html'
        html = requests.get(nextpage, timeout=15)
        soup = BeautifulSoup(html.text, 'lxml')

        nlist = soup.find('ul', class_='nlist')

        data_vals = nlist.find_all('li')

        for data_val in data_vals:
            # print(data_val)
            try:
                url = 'http:' + data_val.find('a')['href']
                urls.append(url)
            except TypeError:
                pass

    return urls


def get_one_data(url, cookies, days, prices, nums):
    print(url)

    r = get_html(url, cookies)
    soup = BeautifulSoup(r, 'lxml')

    # text1=soup.find('div',class_='text')
    # text=text1.find('div',class_='text')

    # print(text)
    try:
        text = soup.find('div', id='text22222')
        ctrs = text.find_all('tr')
    except AttributeError:
        try:
            text = soup.find('div', id='text')
            ctrs = text.find_all('tr')
        except AttributeError:
            print('这个链接有点问题')
    price = 0
    num = 0
    for ctr in ctrs[2:]:
        tds = ctr.find_all('td')
        try:
            print('tds[0]是', tds[0])
            # print(tds[0].text)
            if tds[0].text.strip() == '螺纹钢':
                print('tds[4]是',tds[4])
                price += int(tds[4].text.strip())

                num += 1
        except IndexError:
            pass
        except ValueError:
            print('无权限：',tds[4])
    title = soup.title.string
    day = re.findall(r'\d+', title)[0]

    if day in days:
        prices[days.index(day)] = prices[days.index(day)] + price
        nums[days.index(day)] = nums[days.index(day)] + num
    else:
        days.append(day)
        prices.append(price)
        nums.append(num)


if __name__ == '__main__':

    # 获取登录cookies
    #raw_cookies = 'JSESSIONID=F8BBBA42CD0BBB6EF1E513CF6599FFCC; Hm_lvt_1c4432afacfa2301369a5625795031b8=1496309242; Hm_lpvt_1c4432afacfa2301369a5625795031b8=1496324582; _login_token=a429e808d499f09a57581e7c5690dd67; _login_uid=2069975; _login_mid=2890196; _last_loginuname=skyppe; a429e808d499f09a57581e7c5690dd67=17%3D5%2635%3D5%2636%3D5%2633%3D5%2634%3D5%2613%3D5%2637%3D5%2611%3D5%2638%3D5%262%3D5%261%3D5%2642%3D5%2632%3D5%2641%3D5%2631%3D5%264%3D5%2640%3D5%26catalog%3D010205%2C010202%2C0222%2C0223%2C0205'
    raw_cookies ='_last_loginuname=mysteel814; _rememberStatus=false; 531a8d2f539c7bc2a219ae3764d0a8a3=35%3D5%2622%3D15%2636%3D5%2633%3D5%2634%3D5%2613%3D5%2637%3D5%2611%3D5%2638%3D5%262%3D5%261%3D5%2642%3D5%2632%3D5%2641%3D5%2631%3D5%2640%3D5%264%3D10%26catalog%3D0204%2C1006%2C0203%2C0222%2C0223%2C0205%2C0202%2C0213%2C0223%2C0205%2C0222%2C010205%2C010202%2C0220%2C1001%2C020105%2C020206%2C0209%2C0201%2C02%2C1002; href=https%3A%2F%2Fwww.mysteel.com%2Ffooter_iframe.html; Hm_lvt_1c4432afacfa2301369a5625795031b8=1566124751,1566208807,1566209673,1566368262; accessId=5d36a9e0-919c-11e9-903c-ab24dbab411b; _login_token=6fe7bed88e709a827ae7a2f984fdf511; _login_uid=4381274; _login_mid=5404268; _login_ip=202.118.75.146; 6fe7bed88e709a827ae7a2f984fdf511=1%3D5; pageViewNum=5; Hm_lpvt_1c4432afacfa2301369a5625795031b8=1566375111; _last_ch_r_t=1566375032314'
    cookies = {}
    for line in raw_cookies.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value

    # 获取所有数据的详情的url页面
    urls = get_url()

    days = []
    prices = []
    nums = []

    # 写入数据
    for url in urls:
        get_one_data(url, cookies, days, prices, nums)
    #get_one_data('http://export.mysteel.com/m/19/0821/15/S5365753400B57340.html', cookies, days, prices, nums)
    with open('螺纹钢.txt', 'a+') as f:
        for i in range(len(days)):
            f.write(days[i] + '\t' + str(prices[i]) +  '\t' + str(nums[i]) + '\n')

    print('所有数据写入完毕')