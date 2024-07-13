# import requests
#
# url = 'https://etax99.hubei.chinatax.gov.cn:5100/'
# dic = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
#                      "Chrome/124.0.0.0 Safari/537.36"}
#
# resp = requests.get(url, headers=dic)
#
# print(resp.text)


import requests
from pyquery import PyQuery as pq

url = 'http://quotes.toscrape.com/js/'
response = requests.get(url)
doc = pq(response.text)
print('Quotes:', doc('.quote').length)
