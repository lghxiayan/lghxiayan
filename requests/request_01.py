#!/usr/bin/conda python
# -*- coding: utf-8 -*-
# @Time : 2022/08/09 15:12
# @Author : xiayan
# @Email : lghxiayan@163.com

import requests

url = 'https://www.sogou.com/web?query=台湾'
dic = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/104.0.5112.81 Safari/537.36"}

resp = requests.get(url, headers=dic)

print(resp.text)


