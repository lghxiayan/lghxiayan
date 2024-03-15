import csv
import bs4
import requests

url = 'http://www.vegnet.com.cn/Price/List.html'
resp = requests.get(url)
resp.encoding = 'utf-8'
html = resp.text

page = bs4.BeautifulSoup(html, 'html.parser')
# print(type(page), page)  # <class 'bs4.BeautifulSoup'>

div = page.find('div', attrs={'class': 'pri_k'})
# print(type(table), table)  # <class 'bs4.element.Tag'>

p_s = div.find_all('p')
# print(type(p_s), p_s)  # <class 'bs4.element.ResultSet'>


with open('caijia.csv', mode='w+', newline='', encoding='utf-8') as f:
    csv_writer = csv.writer(f)

    for p in p_s:
        span_s = p.find_all('span')
        # print(type(span_s), span_s)  # <class 'bs4.element.ResultSet'>
        date = span_s[0].text
        pinzhong = span_s[1].text
        market = span_s[2].text
        low = span_s[3].text
        height = span_s[4].text
        avg = span_s[5].text
        danwei = span_s[6].text
        find = span_s[7].text
        csv_writer.writerow([date, pinzhong, market, low, height, avg, danwei, find])
