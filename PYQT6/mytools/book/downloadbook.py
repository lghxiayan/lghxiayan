"""
用来从小说网站下载书籍用的。
"""

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
from tqdm import tqdm  # 引入tqdm库
from urllib.parse import urljoin, urlparse, urlunparse  # 引入urljoin和urlparse处理URL

session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retries)
session.mount('http://', adapter)
session.mount('https://', adapter)

# 这个是目录页
base_url = 'http://huomu.tingxs1.org/5/5009/'

# 传入目录列表的HTML代码片段
directory_html = '<div class="article_texttitleb">'
directory_soup = BeautifulSoup(directory_html, 'html.parser')
print(directory_soup)
print(directory_soup.name)
# print(directory_soup['class'][0])

# 获取目录页面
try:
    response = session.get(base_url, timeout=10)
    response.encoding = 'gb2312'
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到目录列表
    article_texttitleb = soup.find('div', class_='article_texttitleb')
    if not article_texttitleb:
        raise Exception("未找到目录列表")

    # 获取所有章节链接
    chapter_links = article_texttitleb.find_all('a')
    chapter_urls = [urljoin(base_url, a['href']) for a in chapter_links if 'href' in a.attrs]

    # 去重并规范化URL
    chapter_urls = [urlunparse(urlparse(url)) for url in chapter_urls]  # 规范化URL

    print(chapter_urls)

    if not chapter_urls:
        raise Exception("未找到任何章节链接")

    # 将所有章节内容保存为txt文件
    with open('book.txt', 'w', encoding='utf-8') as f:
        for url in tqdm(chapter_urls, desc="下载进度"):  # 使用tqdm包装chapter_urls
            try:
                response = session.get(url, timeout=10)  # 设置10秒超时
                response.encoding = 'gb2312'
                soup = BeautifulSoup(response.text, 'html.parser')

                # 获取标题
                title_tag = soup.find('h1')
                title = title_tag.get_text(strip=True) if title_tag else 'No Title'

                # 获取内容
                content_tag = soup.find('div', id='book_text')
                content = content_tag.get_text(strip=True) if content_tag else 'No Content'

                # 将标题和内容组合
                chapter_text = f"{title}\n{content}\n\n"

                # 写入文件
                f.write(chapter_text)
                f.flush()  # 确保内容立即写入文件

                # 每次请求后休眠1秒，减少请求频率
                time.sleep(1)

            except requests.exceptions.Timeout:
                print(f"请求超时: {url}")
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP错误: {http_err} - URL: {url}")
            except Exception as err:
                print(f"其他错误: {err} - URL: {url}")

except requests.exceptions.Timeout:
    print(f"请求超时: {base_url}")
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP错误: {http_err} - URL: {base_url}")
except Exception as err:
    print(f"其他错误: {err} - URL: {base_url}")
