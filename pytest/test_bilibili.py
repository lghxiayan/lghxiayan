from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def test_bilibili():
    service = Service(executable_path='D:\\google_chrome\\chromedriver-win64\\chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.get('https://www.bilibili.com/')
    title = driver.title
    url = driver.current_url
    text = driver.find_element(By.CSS_SELECTOR, 'a[href="//www.bilibili.com"]').text

    print(title, url, text)
    # button_text = driver.find_element(By.CSS_SELECTOR, 'nav-search-btn').accessible_name
    assert title == '哔哩哔哩 (゜-゜)つロ 干杯~-bilibili'
    assert url == 'https://www.bilibili.com/'
    assert text == '首页'
    # assert button_text == '搜索'
