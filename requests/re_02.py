#!/usr/bin/conda python
# -*- coding: utf-8 -*-
# @Time : 2022/08/22 10:22
# @Author : xiayan
# @Email : lghxiayan@163.com

import csv
import re
import requests

domain = 'https://www.dytt89.com/'
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/104.0.5112.81 Safari/537.36"}
resp = requests.get(domain, headers=header)
resp.encoding = 'gb2312'
html = resp.text
# print(html)
first_obj = re.compile('2022必看热片.*?<ul>(?P<url>.*?)</ul>', re.S)
first_result = ''.join(first_obj.findall(html))
# print(type(first_result), first_result)
secend_obj = re.compile("<li><a href=\'(?P<secend_url>.*?)\' title=", re.S)
secend_result = secend_obj.findall(first_result)
# secend_result = 'https://www.dytt89.com/'.join(secend_obj.findall(first_result))
# print(secend_result)
for i in range(len(secend_result)):
    secend_result[i] = 'https://www.dytt89.com/' + secend_result[i]
# print(secend_result)
header_list = ['电影名称', '下载地址']

for url in secend_result:
    page_resp = requests.get(url)
    page_resp.encoding = 'gb2312'
    page_html = page_resp.text
    # print(page_html)
    page_obj = re.compile(r'<div class="title_all"><h1>(?P<movie_name>.*?)'
                          r'</h1>.*?<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(?P<download_url>.*?)</a></td>',
                          re.S)
    page_result = page_obj.finditer(page_html)

    with open('new_data_1.csv', 'a+', encoding='utf-8', newline='') as f_out:
        writer = csv.writer(f_out)
        for i in page_result:
            writer.writerow(i.groups('movie_name'))
