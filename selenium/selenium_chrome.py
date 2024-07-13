from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import sys

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 启动无头模式
options.add_argument('--disable-gpu')  # 配合无头模式使用，某些系统可能需要
options.add_argument('--window-size=1920,1080')  # 设置视窗大小，模拟桌面浏览器
options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/124.0.6367.61 Safari/537.3"')
options.add_argument('--disable-extensions')

options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--incognito")  # 无痕模式
options.add_argument("start-maximized")  # 最大化窗口

# 确保Chrome浏览器已安装且添加到系统PATH，或者直接指定其完整路径
chrome_binary_path = "D:\\google_chrome\\chrome-win64\\chrome.exe"

options = webdriver.ChromeOptions()
options.binary_location = chrome_binary_path

# 使用环境变量或配置文件来管理ChromeDriver路径
chromedriver_path = os.getenv('CHROMEDRIVER_PATH', 'D:\\google_chrome\\chrome-win64\\chromedriver.exe')
service = ChromeService(executable_path=chromedriver_path)

# 添加异常处理和确保资源正确释放
try:
    browser = webdriver.Chrome(service=service, options=options)
    browser.get("https://etax99.hubei.chinatax.gov.cn:5100")

    # 替换硬编码的等待时间，使用显式等待
    # 假设我们将等待页面中的某个元素出现作为页面加载完成的标志
    # 请根据实际页面结构替换BY条件
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "yourElementId")))

finally:
    if 'browser' in locals():
        browser.quit()
