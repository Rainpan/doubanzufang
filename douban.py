# -*- coding: utf-8 -*-
# encoding: utf-8

import time
import random
import requests
import re
import sqlite3
import hashlib
import sys
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

conn = sqlite3.connect('/home/panda/Downloads/test.db')
c = conn.cursor()


def insert(title, title_md5, href, type):
    sql = "insert or replace into douban(title,title_md5,href,type,update_time) values('{d_title}','{d_title_md5}','{d_href}',{type},'{time}')". \
        format(d_title=title, d_href=href, d_title_md5=title_md5, type=type, time=int(time.time()))
    print sql
    c.execute(sql)
    conn.commit()


def select(limit, offset):
    sql = "select id,title,href,update_time from douban where status=1 limit {limit} offset {offset}".format(
        limit=limit, offset=offset)
    return c.execute(sql)


def update(id, status, collection):
    sql = "update douban set " + (" status=" + status if status else "") + (
        " collection=" + collection if collection else "") + " where id=" + id
    c.execute(sql)


def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()


user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
ip_list = ['']
csv_file = open("body.html", 'w')
groups = open('groups.txt', 'r')
shelve = open('shelve.html', 'w')
fitCount = 1
shelveCount = 1
for group in groups.readlines():
    group = group.strip('\n')
    for i in range(15):  # 页码 爬取前30页信息
        # 需要爬取的网址，用同样的形式替换，复制的网址start=后面的数字掉即可
        url = group + str(i * 25)
        UA = random.choice(user_agent_list)
        headers = {'User-Agent': UA}
        random_ip = random.choice(ip_list)
        proxy = {'http': random_ip}
        try:
            rec = requests.get(url, headers=headers)
            # rec = requests.get(url, headers=headers,proxies=proxy)#需要ip的话打开这个
            Soup = BeautifulSoup(rec.text, 'lxml')
            a_list = Soup.find_all('a', class_="", title=True)
            for a in range(len(a_list)):
                title = a_list[a]['title']  # 取出a标签的href 属性
                title = title.encode('utf-8')
                href = a_list[a]['href']
                # 符合的条件
                reg1 = re.search(r'(西乡|坪洲|宝体|碧海湾|桃园)', title)
                # 去除的条件
                reg2 = re.search(r'(限女|女生|小姐姐|公寓|求.*[租|组]|已.*[租|转])', title)

                if reg2 is None:
                    if reg1 is not None:
                        insert(title, md5(title), href, 0)
                        # content = "<tr><td>" + str(
                        #     fitCount) + "</td><td><a href='" + href + "' target='_blank'>" + title + "</a></td></tr>\n"
                        # csv_file.write(content)
                        # csv_file.flush()
                        # fitCount += 1
                    else:
                        reg3 = re.search(r'(后瑞|福永|灵芝|固戍|洪浪北)', title)
                        if reg3 is None:
                            insert(title, md5(title), href, 1)
                            # content = "<tr><td>" + str(
                            #     shelveCount) + "</td><td><a href='" + href + "' target='_blank'>" + title + "</a></td></tr>\n"
                            # shelve.write(content)
                            # shelve.flush()
                            # shelveCount += 1

                time.sleep(0.8)  # 休息0.8s 如果出现链接失败，可以把间隔时间加长
        except Exception as e:
            print(e)
            random_ip = random.choice(ip_list)
csv_file.close()
groups.close()
shelve.close()
conn.close()
