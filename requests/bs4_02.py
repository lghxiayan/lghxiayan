import requests
import bs4
from netAssist import time

url = 'https://www.umei.cc/bizhitupian/weimeibizhi/'
resp = requests.get(url)
resp.encoding = 'utf-8'
html = resp.text
main_page = bs4.BeautifulSoup(html, 'html.parser')
main_a = main_page.find('div', class_="swiper-wrapper after").find_all('a')
list_url = []
for a in main_a:
    href = 'https://www.umei.cc' + a.get('href')
    list_url.append(href)
    page_html = requests.get(href).text
    img_url = bs4.BeautifulSoup(page_html, 'html.parser').find \
        ('section', class_='img-content').find('img').get('src')
    img_resp = requests.get(img_url)
    img_name = img_url.split('/')[-1]
    with open('img/' + img_name, 'wb') as f:
        f.write(img_resp.content)
    print('done ', img_name)
    time.sleep(1)
