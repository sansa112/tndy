import time
import urllib.request as request
import urllib.error
from urllib import parse
import ssl
import json
import csv
import os.path

profile = []
bv = []
oids = []
file_con = []
k = 0
ssl._create_default_https_context = ssl._create_unverified_context
searchlink = "https://api.bilibili.com/x/web-interface/search/all/v2?context=&page=1&order=&keyword="
gamer = ["花少北", "靠脸吃饭的徐大王", "老番茄", "某幻君", "中国BOY超级大猩猩", "纯黑"]


def ask(url):
    head = {
        'Accept': 'application / json'
    }
    rq = urllib.request.Request(url=url, headers=head)
    link = ""
    try:
        req = request.urlopen(rq)
        link = req.read().decode('utf8', 'ignore')
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return link

# 搜索up主存资料

for item in gamer:
    cue = parse.quote(item)
    html = searchlink + cue
    time.sleep(2)
    url = ask(html)
    data = json.loads(url)
    unames = data['data']['result'][7]['data'][0]['uname']
    time.sleep(2)
    fans_no = data['data']['result'][7]['data'][0]['fans']
    mid = data['data']['result'][7]['data'][0]['mid']
    profile.append(mid)
    file_con.append({'Up主id': unames, '粉丝人数': fans_no})

print("finish phase 1")

with open('fans_count_gamer 1.csv', 'w', newline='') as csvfile:
    fieldnames = ('Up主id', '粉丝人数')
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for con in file_con:
        writer.writerow(con)


print("finish phase 2")

def ask2(url):
    head = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    }
    rq = urllib.request.Request(url=url, headers=head)
    link = ""
    try:
        req = request.urlopen(rq)
        link = req.read().decode('utf8', 'ignore')
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return link

# 打开主页收bv号
for ppl in profile:
    pplink = 'https://api.bilibili.com/x/space/arc/search?mid=' + str(ppl) + '&pn=1&ps=25&index=1&jsonp=jsonp'
    time.sleep(3)
    ppurl = ask(pplink)
    data2 = json.loads(ppurl)
    all_ppitems = data2['data']['list']['vlist']
    for item in all_ppitems:
        aid = item['aid']
        oids.append(aid)

print("finish phase 3")

# for vid_link in bv:
for oid in oids:
    comments = []
    for x in range(1, 6):
        comment_link = 'https://api.bilibili.com/x/v2/reply?%20&jsonp=jsonp%20&pn=' + str(x) + '&type=1%20&oid=' + str(
            oid) + '&sort=2'
        time.sleep(2)
        try:
            com_link = ask2(comment_link)
        except (http.client.IncompleteRead) as e:
            com_link = e.partial
        time.sleep(1)
        raw_com = json.loads(com_link)
        if raw_com['data']['replies']:
            for i in raw_com['data']['replies']:
                content = i['content']['message']
                comments.append(content)
    k += 1
    print(k)
    if not os.path.exists('/Users/wongrhuipoh/PycharmProjects/pythonProject13/comment_content' + str(oid) + '.txt'):
        with open('comment_content' + str(oid) + '.txt', 'w', encoding='utf8') as f:
            for comment in comments:
                f.write(comment + "\n")
        print("finished exporting")
