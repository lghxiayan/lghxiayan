from netAssist import time
import requests
from lxml import etree
import random
import os

video_list_url = 'https://www.pearvideo.com/category_6'


def get_video_list(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'Referer': 'https://www.pearvideo.com/'
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    return resp.text


def parse_html(html):
    """
    分析html代码，返回视频的链接地址
    :param html: 网页源代码
    :return: 视频的链接地址，列表
    """
    tree = etree.HTML(html)
    result = tree.xpath('//*[@id="listvideoListUl"]/li[@class="categoryem "]/div/a/@href')
    return result


def get_video_url(page_list):
    for url in page_list:
        full_url = 'https://www.pearvideo.com/' + url
        contId = url.split('_')[1]
        mrd = random.random()
        videoStatusUrl = f'https://www.pearvideo.com/videoStatus.jsp?contId={contId}&mrd={mrd}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'Referer': full_url
        }
        resp = requests.get(videoStatusUrl, headers=headers)
        # print(resp.text)
        resp1 = resp.json()
        systemTime = resp1['systemTime']
        srcUrl = resp1['videoInfo']['videos']['srcUrl']
        result = srcUrl.replace(systemTime, f'cont-{contId}')
        print(result)

        filename = f'video/{contId}.mp4'
        if not os.path.isfile(filename):
            start = netAssist.time()
            with open(filename, 'wb') as f_out:
                f_out.write(requests.get(result).content)
            end = netAssist.time()
            print('Total time: ', end - start)


html = get_video_list(video_list_url)
page_list = parse_html(html)
get_video_url(page_list)
