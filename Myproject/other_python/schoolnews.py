import requests
from pyquery import PyQuery as pq
import re
import pymysql
import time
index = 'http://mech.ecust.edu.cn'

def getnews():
    url = "http://mech.ecust.edu.cn/Data/List/xyxw"
    allnewspage = pq((requests.get(url)).text)
    result = []
    for each in allnewspage(".data-list li").items():
        time = each("span").text()
        url = index + each('a').attr('href')
        if url in urlList: continue
        if "javascript" in url: continue
        content = FTCE(url)
        title = pq(content)('.view-title h1').text()
        news_content = pq(content)('.view-cnt').text()
        read_count = int(re.findall(r'\d+',pq(content)('.view-info span').eq(1).text())[0])
        result.append([title,time, url, news_content, read_count])
    return result

def FTCE(url):
    try:
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        content = response.text
    except:
        print('ConnectionError:')
        return
    else:
        return content

def putintomysql():
    db = pymysql.connect(host="localhost", user="root", password="133769", database="machinery", charset="utf8")
    cursor = db.cursor()
    for i in getnews():
        
        text = "INSERT INTO news_schoolnews(title,release_time,URL,news_content,read_count) VALUES ('%s', '%s', '%s', '%s', '%d')" % (
        i[0], i[1], i[2], i[3], i[4])
        cursor.execute(text)
    cursor.close()
    db.commit()
    db.close()


urlList = set()
db = pymysql.connect(host="localhost", user="root", password="133769", database="machinery", charset="utf8")
cur = db.cursor()
cur.execute("select URL from news_schoolnews")
tmp = cur.fetchall()
for t in tmp:
    urlList.add(t[0])
cur.close()
db.close()

putintomysql()
