import csv
import requests
from lxml import etree

url = 'https://beijing.zbj.com/search/service/?kw=saas&r=1'
resp = requests.get(url)
html = resp.text

data_list = []

tree = etree.HTML(html)
for i in range(1, 10):
    data = []
    result1 = ''.join(
        tree.xpath(f'//*[@id="__layout"]/div/div[3]/div/div[3]/div[4]/div[1]/div[{i}]/a/div[2]/div[1]/div/text()'))
    print(result1)
    result2 = ''.join(tree.xpath(f'//*[@id="__layout"]/div/div[3]/div/div[3]/div[4]/div[1]/div[{i}]/div[3]/a/text()'))
    print(result2)
    result3 = tree.xpath(f'//*[@id="__layout"]/div/div[3]/div/div[3]/div[4]/div[1]/div[{i}]/div[3]/div[2]/div[1]')[
        0].xpath(
        "string(.)")
    print(result3)
    result4 = tree.xpath(f'//*[@id="__layout"]/div/div[3]/div/div[3]/div[4]/div[1]/div[{i}]/div[3]/div[2]/div[2]')[
        0].xpath(
        "string(.)")
    print(result4)
    result5 = tree.xpath(f'//*[@id="__layout"]/div/div[3]/div/div[3]/div[4]/div[1]/div[{i}]/div[3]/div[1]')[0].xpath(
        "string(.)")
    print(result5)

    data.append(result1)
    data.append(result2)
    data.append(result3)
    data.append(result4)
    data.append(result5)

    print(data)
    data_list.append(data)

print(data_list)

with open('data4.csv', 'w+', newline='', encoding='utf-8') as f_out:
    csv_writer = csv.writer(f_out)
    csv_writer.writerows(data_list)
