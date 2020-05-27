import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
import sys
from urllib.parse import quote
import csv
import datetime

now = datetime.date.today() + datetime.timedelta(hours = 8)
titletest = list()
hosttest = list()
urltest = list()
timetest = list()
to_append = list()
dic = [
    "id", 
    "標題", 
    "category",
    "發布來源",
    "網址",
    "發布時間",
    "segment",
]
 
    
bad_host = ['中工网','中国奥林匹克委员会','星洲网','China Press','手机网易网','新浪网','东方财富网','千龙网','搜狐'
           ,'中国新闻网','汉丰网','京报网','人民网','中国侨网','杭州网','中华人民共和国外交部','华体网','NTDTV','新京报'
           ,'联合国新闻','自由亚洲电台','法国国际广播电台','多维新闻网','BBC 中文网','青年日報','联合早报','新浪网']
df1 = pd.DataFrame(columns=dic)
TestIdCount = 0
for i in range(1):
    IgnoreDateFlag = 0
    keyword = input()
    
    StartNums = input('原初的日期，數字之間加入/：')

    if StartNums is '':
        IgnoreDateFlag = 1
        print('no limit')
    else:
        nums_tmp = StartNums.split('/')
        snums = []
        for n in nums_tmp:
            if n.isdigit():
                snums += [int(n)]

            if len(snums) == 3:
                break;
        if len(snums) != 3:
            IgnoreDateFlag = 2
            print('wrong date form')
            break;
        print(snums[0],snums[1],snums[2])
    
    EndNums = input('終結的日期，數字之間加入/：')

    if EndNums is '':
        IgnoreDateFlag = 1
        print('no limit')
    else:
        nums_tmp = EndNums.split('/')
        enums = []
        for n in nums_tmp:
            if n.isdigit():
                enums += [int(n)]

            if len(enums) == 3:
                break;
        if len(enums) != 3:
            IgnoreDateFlag = 2
            print('wrong date form')
            break;
        print(enums[0],enums[1],enums[2])
    
    headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    }
    if IgnoreDateFlag is 1:
         payload = {'q': str(keyword), 'tbm':'nws', 'lr':'lang_zh-TW', 'num':'100', 'tbs':'qdr:y'}
        
    elif IgnoreDateFlag is 0:
        payload = {'q': str(keyword), 'tbm':'nws', 'lr':'lang_zh-TW', 'num':'100', 'tbs':'cdr:1,cd_min:' \
                   +str(snums[1])+'/'+str(snums[2])+'/'+str(snums[0]) \
                   +',cd_max:'+str(enums[1])+'/'+str(enums[2])+'/'+str(enums[0])}
        
    s = requests.Session()
    re = s.get("https://www.google.com.tw/search",params = payload, headers = headers)
    print(re.url)

    '''
    print("https://www.google.com.tw/search?num=30&q="+keyword+"&oq="+keyword+ \
    "&dcr=0&tbm=nws&source=lnt&tbs=cdr:1,cd_min:"+nums_str+ \
    ",cd_max:"+nums_str)
    '''
        
    content = re.text
    #print(content)
    soup = BeautifulSoup(content,"html.parser")
    title_list = soup.find_all('div',{'class':'gG0TJc'})
    host_list = soup.find_all('div',{'class':'gG0TJc'})
    url_list = soup.find_all('div',{'class':'gG0TJc'})
    time_list = soup.find_all('div',{'class':'gG0TJc'})
    #print(soup)
    #print(title_list)
    #print(url_list)
    for ti in title_list:
        #擷取新聞標題
        a = ti.find_all('a')[0].text
        titletest.append(a)
        #print(a)
        
    #print('==============================')
    for ho in host_list:
        #擷取新聞網
        a = ho.find_all('span',{'class':'xQ82C e8fRJf'})[0].text
        a = a.split(' ')[0]
        hosttest.append(a)
        #print(a)
        
    #print('==============================')
    for url in url_list:
        #擷取新聞網址
        a = url.find_all('a')[0]['href']
        urltest.append(a)
        #print(a)
        
    #print('==============================')
    for time in time_list:
        #擷取新聞發布時間
        a = time.find_all('span',{'class':'f nsa fwzPFf'})[0].text
        timetest.append(a)
        #print(a)
        
    #print('==============================')
    
    count = TestIdCount
    for i in range(len(titletest)):
        dateflag = 0
        if(hosttest not in bad_host):
            count = count + 1
            if IgnoreDateFlag is not 2:
                to_append = [int(count),titletest[i],"neutral",hosttest[i],urltest[i],timetest[i],""]
                a_series = pd.Series(to_append, index = df1.columns)
                df1 = df1.append(a_series, ignore_index=True)

                print('======[',i,']=========')
                print(titletest[i])
                print(urltest[i])
                print(hosttest[i])
                print(timetest[i])
                print(" ")
            
        to_append.clear()
        
    TestIdCount = TestIdCount + len(titletest)
    count = 0
    
    #print(to_append)
    titletest.clear()
    hosttest.clear()
    urltest.clear()
'''
if IgnoreDateFlag is not 2:
    df1.to_csv('train.csv',index=False,encoding='UTF-8_sig')
    print('done')
'''