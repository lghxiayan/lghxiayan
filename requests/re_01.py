import re
import requests
import csv

for i in range(0, 250, 25):
    url = f'https://movie.douban.com/top250?start={i}&filter='
    # url = 'https://movie.douban.com/top250'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0"}
    resp = requests.get(url=url, headers=headers)
    html = resp.text

    obj = re.compile(
        r'<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)</span>.*?<br>'
        r'(?P<year>.*?)&nbsp;/&nbsp;.*?<span class="rating_num" property="v:average">'
        r'(?P<point>.*?)</span>.*?<span property="v:best" content="10.0"></span>.*?<span>'
        r'(?P<commit>.*?)人评价</span>',
        re.S)

    result = obj.finditer(html)
    f = open('data1.csv', 'a+', encoding='utf-8', newline='')
    csvwriter = csv.writer(f)

    for i in result:
        print(i.group('name'))
        print(i.group('year').strip())
        print(i.group('point'))
        print(i.group('commit'))

        # dic = i.groupdict()
        # dic['year'] = dic['year'].strip()
        # csvwriter.writerow(dic.values())
        #
        # print(dic)
