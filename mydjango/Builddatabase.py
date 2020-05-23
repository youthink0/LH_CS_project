# coding:utf-8
import csv
import sqlite3
import jieba


def dataImport(csvpath, dbpath, tablename):
    reader = csv.DictReader(open(csvpath, "rt"), delimiter = ',', quoting = csv.QUOTE_MINIMAL)
    conn = sqlite3.connect(dbpath)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("DROP TABLE " + tablename)
    create_sql = "CREATE TABLE "+tablename + "(id INT PRIMARY KEY NOT NULL, title NCHAR, category NCHAR, segment NCHAR, host NCHAR, url NCHAR, time INT)"
    c.execute(create_sql)

    for row in reader:
        to_db = [row['id'], row['title'], row['category'], row['segment'], row['host'], row['url'], time['INT']]
        c.execute("INSERT INTO "+tablename+ "(id, title, category, segment, host, url, time) VALUES (?, ?, ?, ?, ?, ?, ?)", to_db)
    conn.commit()

    conn.close()

def get_segment():
    conn = sqlite3.connect("./db.sqlite3")
    cursor = conn.cursor()
    sql = "SELECT id, title FROM CrawledPage"
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
        sql = "UPDATE CrawledPage SET segment = '%s' WHERE id = %d" % (line, row[0])
        cursor.execute(sql)
        conn.commit()

    conn.close()

# 匯入資料
dataImport("./train.csv", "./db.sqlite3", "CrawledPage")
# 切詞
get_segment()