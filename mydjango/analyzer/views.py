from django.shortcuts import render
from django.http import HttpResponse
from .models import CrawlPage
# coding:utf-8
import Classifier
import os
import sqlite3

# Create your views here.
def home(request):
    return render(request, 'analyzer/home.html')

def result(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        # 抓取資料
        Classifier.crawl(keyword)
        # 匯入資料
        Classifier.dataImport("./test.csv", "./db.sqlite3", "CrawlPage")
        os.remove(r"./test.csv")
        # 切詞
        Classifier.get_segment()
        # 分類
        Classifier.pred()

    conn = sqlite3.connect("./db.sqlite3")
    cursor = conn.cursor()
    sql = "SELECT COUNT(*) FROM Crawlpage WHERE category = \'neutral\'"
    cursor.execute(sql)
    result = cursor.fetchone()
    total_count = result[0]

    sql = "SELECT host, COUNT() AS COUNT FROM Crawlpage WHERE category = \'neutral\' GROUP BY host ORDER BY COUNT DESC limit 3"
    cursor.execute(sql)
    row = cursor.fetchall()

    context = {
        'title': 'Result',
        'total_count': total_count,
    }
    if total_count > 0:
        context.update({'crawlPages': CrawlPage.objects.filter(category = 'neutral')})
    if len(row) > 0:
        context.update({'first': row[0][0]})
        context.update({'first_count': row[0][1]})
        context.update({'first_per': round(row[0][1] / total_count * 100)})
    if len(row) > 1:
        context.update({'second': row[1][0]})
        context.update({'second_count': row[1][1]})
        context.update({'second_per': round(row[1][1] / total_count * 100)})
    if len(row) > 2:
        context.update({'third': row[2][0]})
        context.update({'third_count': row[2][1]})
        context.update({'third_per': round(row[2][1] / total_count * 100)})

    conn.close()

    return render(request, 'analyzer/result-neu.html', context)

def positive(request):
    conn = sqlite3.connect("./db.sqlite3")
    cursor = conn.cursor()
    sql = "SELECT COUNT(*) FROM Crawlpage WHERE category = \'positive\'"
    cursor.execute(sql)
    result = cursor.fetchone()
    total_count = result[0]

    sql = "SELECT host, COUNT() AS COUNT FROM Crawlpage WHERE category = \'positive\' GROUP BY host ORDER BY COUNT DESC limit 3"
    cursor.execute(sql)
    row = cursor.fetchall()

    context = {
        'title': 'Result',
        'total_count': total_count,
    }
    if total_count > 0:
        context.update({'crawlPages': CrawlPage.objects.filter(category='positive')})
    if len(row) > 0:
        context.update({'first': row[0][0]})
        context.update({'first_count': row[0][1]})
        context.update({'first_per': round(row[0][1] / total_count * 100)})
    if len(row) > 1:
        context.update({'second': row[1][0]})
        context.update({'second_count': row[1][1]})
        context.update({'second_per': round(row[1][1] / total_count * 100)})
    if len(row) > 2:
        context.update({'third': row[2][0]})
        context.update({'third_count': row[2][1]})
        context.update({'third_per': round(row[2][1] / total_count * 100)})

    conn.close()

    return render(request, 'analyzer/result-pos.html', context)

def negative(request):
    conn = sqlite3.connect("./db.sqlite3")
    cursor = conn.cursor()
    sql = "SELECT COUNT(*) FROM Crawlpage WHERE category = \'negative\'"
    cursor.execute(sql)
    result = cursor.fetchone()
    total_count = result[0]

    sql = "SELECT host, COUNT() AS COUNT FROM Crawlpage WHERE category = \'negative\' GROUP BY host ORDER BY COUNT DESC limit 3"
    cursor.execute(sql)
    row = cursor.fetchall()

    context = {
        'title': 'Result',
        'total_count': total_count,
    }
    if total_count > 0:
        context.update({'crawlPages': CrawlPage.objects.filter(category='negative')})
    if len(row) > 0:
        context.update({'first': row[0][0]})
        context.update({'first_count': row[0][1]})
        context.update({'first_per': round(row[0][1] / total_count * 100)})
    if len(row) > 1:
        context.update({'second': row[1][0]})
        context.update({'second_count': row[1][1]})
        context.update({'second_per': round(row[1][1] / total_count * 100)})
    if len(row) > 2:
        context.update({'third': row[2][0]})
        context.update({'third_count': row[2][1]})
        context.update({'third_per': round(row[2][1] / total_count * 100)})

    conn.close()

    return render(request, 'analyzer/result-neg.html', context)

def about(request):
    return render(request, 'analyzer/about.html', {'title': 'About'})