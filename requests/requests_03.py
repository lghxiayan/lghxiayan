#!/usr/bin/conda python
# -*- coding: utf-8 -*-
# @Time : 2022/08/10 17:28
# @Author : xiayan
# @Email : lghxiayan@163.com
import requests
import json

url = "https://movie.douban.com/j/chart/top_list"

param = {
    'type': '24',
    'interval_id': '100:90',
    'action': '',
    'start': '0',
    'limit': '20'
}

dic = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/104.0.5112.81 Safari/537.36"}

resp = requests.get(url=url, params=param, headers=dic)
# new_url = resp.request.url
# print(new_url)
print(resp.json())
resp.close()

with open('movie.json', 'w+', encoding='utf-8') as f:
    # f.write(resp.json())
    json.dump(resp.json(), f)
