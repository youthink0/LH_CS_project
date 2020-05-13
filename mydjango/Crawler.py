import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
import sys
from urllib.parse import quote
import csv

titletest = list()
hosttest = list()
urltest = list()
to_append = list()
dic = [
    "id",
    "標題",
    "category",
    "發布來源",
    "網址",
    "segment",
]

bad_host = ['中工网', '中国奥林匹克委员会', '星洲网', 'China Press', '手机网易网', '新浪网', '东方财富网', '千龙网', '搜狐'
    , '中国新闻网', '汉丰网', '京报网', '人民网', '中国侨网', '杭州网', '中华人民共和国外交部', '华体网', 'NTDTV', '新京报'
    , '联合国新闻', '自由亚洲电台', '法国国际广播电台', '多维新闻网', 'BBC 中文网', '青年日報', '联合早报', '新浪网']
df1 = pd.DataFrame(columns=dic)
TestIdCount = 0
for i in range(10):
    keyword = quote(input().encode('utf8'))
    # keyword1 = quote(input().encode('utf8'))
    # &as_sitesearch="+keyword1+
    re = requests.get(
        "https://www.google.com.tw/search?num=100&q=" + keyword + "&oq=" + keyword + "&dcr=0&tbm=nws&source=lnt&tbs=qdr:m")
    content = re.text

    # print(content)
    soup = BeautifulSoup(content, "html.parser")
    title_list = soup.find_all('div', {'class': 'BNeawe vvjwJb AP7Wnd'})
    host_list = soup.find_all('div', {'class': 'BNeawe UPmit AP7Wnd'})
    url_list = soup.find_all('div', {'class': 'kCrYT'})
    # print(title_list)
    # print(url_list)

    for url in url_list:
        # 擷取新聞網址
        url = str(url)
        url = url.split('<')
        url = url[2]
        url = url.split('=')
        if (len(url) > 2):
            url = url[2].split('&')
            url = url[0]
            if ((url not in urltest)):
                urltest.append(url)

    for ti in title_list:
        # 擷取新聞標題
        ti = str(ti)
        ti = ti.split('>')
        ti = ti[1]
        ti = ti.split('<')
        ti = ti[0]
        titletest.append(ti)

    for ho in host_list:
        # 擷取新聞網
        ho = str(ho)
        ho = ho.split('>')
        ho = ho[1]
        ho = ho.split('<')
        ho = ho[0]
        ho = ho.split(' ')
        ho = ho[0]
        hosttest.append(ho)

    count = TestIdCount
    for i in range(len(titletest)):
        if (hosttest not in bad_host):
            count = count + 1
            # print(titletest[i]+" "+hosttest[i]+" "+urltest[i])
            to_append = [int(count), titletest[i], "neutral", hosttest[i], urltest[i], ""]
            a_series = pd.Series(to_append, index=df1.columns)
            df1 = df1.append(a_series, ignore_index=True)
        to_append.clear()

    TestIdCount = TestIdCount + len(titletest)
    count = 0

    # print(to_append)
    titletest.clear()
    hosttest.clear()
    urltest.clear()

df1.to_csv('train.csv', index=False, encoding='UTF-8_sig')
print('done')