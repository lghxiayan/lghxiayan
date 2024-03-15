import requests
from lxml import etree

url = 'https://www.biedoul.com/wenzi/1/'
resp = requests.get(url)
html = resp.text

tree = etree.HTML(html)
# result = tree.xpath('//dl[@id="xh_180839"]/dd//p//text()')
result = tree.xpath('//dl[@id="xh_180839"]/dd')[0].xpath("string(.)")

print(result)
