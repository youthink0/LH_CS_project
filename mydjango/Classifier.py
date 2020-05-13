# coding:utf-8
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
#import time
#import sys
from urllib.parse import quote
import csv
#import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import jieba
#from jieba import analyse
import sqlite3
#from sklearn import metrics
from sklearn.svm import SVC
#import pickle

def crawl(keyword):
    titletest = list()
    hosttest = list()
    urltest = list()
    to_append = list()

    dic = ["id", "title", "category", "host", "url", "segment",]

    bad_host = ['中工网', '中国奥林匹克委员会', '星洲网', 'China Press', '手机网易网', '新浪网', '东方财富网', '千龙网', '搜狐',
                '中国新闻网', '汉丰网', '京报网', '人民网', '中国侨网', '杭州网', '中华人民共和国外交部', '华体网', 'NTDTV', '新京报',
                '联合国新闻', '自由亚洲电台', '法国国际广播电台', '多维新闻网', 'BBC 中文网', '青年日報', '联合早报', '秦楚网']
    df1 = pd.DataFrame(columns=dic)

    TestIdCount = 0

    keyword_fixed = quote(keyword.encode('utf8'))
    re = requests.get(
        "https://www.google.com.tw/search?num=100&q=" + keyword_fixed + "&oq=" + keyword_fixed + "&dcr=0&tbm=nws&source=lnt&tbs=qdr:m")
    content = re.text

    soup = BeautifulSoup(content, "html.parser")
    title_list = soup.find_all('div', {'class': 'BNeawe vvjwJb AP7Wnd'})
    host_list = soup.find_all('div', {'class': 'BNeawe UPmit AP7Wnd'})
    url_list = soup.find_all('div', {'class': 'kCrYT'})

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
            to_append = [int(count), titletest[i], "neutral", hosttest[i], urltest[i], ""]
            a_series = pd.Series(to_append, index=df1.columns)
            df1 = df1.append(a_series, ignore_index=True)
        to_append.clear()

    titletest.clear()
    hosttest.clear()
    urltest.clear()

    df1.to_csv('test.csv', index=False, encoding='UTF-8_sig')

def dataImport(csvpath, dbpath, tablename):
    reader = csv.DictReader(open(csvpath, "rt", encoding = "utf-8-sig"), delimiter = ',', quoting = csv.QUOTE_MINIMAL)
    conn = sqlite3.connect(dbpath)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("DROP TABLE " + tablename)
    create_sql = "CREATE TABLE "+tablename + "(id INT PRIMARY KEY NOT NULL, title NCHAR NOT NULL, category NCHAR, segment NCHAR, host NCHAR, url NCHAR)"
    c.execute(create_sql)

    for row in reader:
        to_db = [row['id'], row['title'], row['category'], row['segment'], row['host'], row['url']]
        c.execute("INSERT INTO "+tablename+ "(id, title, category, segment, host, url) VALUES (?, ?, ?, ?, ?, ?)", to_db)
    conn.commit()

    conn.close()

def get_segment():
    conn = sqlite3.connect("./db.sqlite3")
    cursor = conn.cursor()
    sql = "SELECT id, title FROM CrawlPage"
    cursor.execute(sql)

    for row in cursor.fetchall():
        # 對標題和內容切詞
        seg_list = jieba.cut(row[1])
        line = ""
        for str in seg_list:
            line = line + " " + str
        line = line.replace('\'', '')
        line = line.replace('【', '')
        line = line.replace('】', '')
        line = line.replace('《', '')
        line = line.replace('》', '')
        line = line.replace('|', '')
        line = line.replace('「', '')
        line = line.replace('」', '')
        line = line.replace('？', '')
        line = line.replace('：', '')
        line = line.replace('！', '')
        line = line.replace('，', '')
        line = line.replace('、', '')
        line = line.replace('／', '')
        line = line.replace('-', '')
        line = line.replace('(', '')
        line = line.replace(')', '')
        line = line.replace('/', '')
        line = line.replace('“', '')
        line = line.replace('”', '')
        # 把切詞按空格分隔並去特殊字元後重新寫到資料庫的segment欄位裡
        sql = "UPDATE CrawlPage SET segment = '%s' WHERE id = %d" % (line, row[0])
        cursor.execute(sql)
        conn.commit()

    conn.close()

def pred():
    conn = sqlite3.connect("./db.sqlite3")
    cursor = conn.cursor()

    # 一共分成2類，並且類別的標識定為0，1，2
    category_ids = range(0, 3)
    category = {}
    category[0] = "positive"
    category[1] = "neutral"
    category[2] = "negative"

    corpus = []
    for category_id in category_ids:
        # 找到這一類的所有已分類的文章並把所有切詞拼成一行，加到語料庫中
        sql = "SELECT segment FROM CrawledPage WHERE category = \'%s\'" % (category[category_id])
        cursor.execute(sql)
        line = ""
        for result in cursor.fetchall():
            segment = result[0]
            line = line + "" + segment
        corpus.append(line)

    # 把欲分類的文章追加到語料庫
    sql = "SELECT id, title, segment FROM CrawlPage"
    cursor.execute(sql)
    if cursor.fetchone():
        cursor.execute(sql)
        line = ""
        update_ids = []
        update_titles = []
        for result in cursor.fetchall():
            id = result[0]
            update_ids.append(id)
            title = result[1]
            update_titles.append(title)
            segment = result[2]
            corpus.append(segment)

        # 計算tf-idf
        vectorizer = CountVectorizer()
        csr_mat = vectorizer.fit_transform(corpus)
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(csr_mat)
        y = np.array(category_ids)

        # 用前2行已標分類的資料做模型訓練
        model = SVC()
        model.fit(tfidf[0:3], y)

        # 對未標註分類的資料做分類預測
        predicted = model.predict(tfidf[3:])

        # 把機器學習得出的分類資訊寫到資料庫
        for index in range(0, len(update_ids)):
            update_id = update_ids[index]
            predicted_category = category[predicted[index]]
            print("predict title: %s <==============> category: %s" % (update_titles[index], predicted_category))
            sql = "UPDATE CrawlPage SET category = \'%s\' WHERE id = %d" % (predicted_category, update_id)
            cursor.execute(sql)

    conn.commit()

    conn.close()

"""
if __name__ == '__main__':

    #抓取資料
    crawl()
    # 匯入資料
    dataImport("./test.csv", "./db.sqlite3", "CrawlPage")
    os.remove(r"./test.csv")
    # 切詞
    get_segment()
    # 分類
    pred()
"""


