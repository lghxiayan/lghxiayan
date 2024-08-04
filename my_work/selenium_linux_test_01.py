from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.binary_location = "/home/xiayan/myenv/chrome-linux64/chrome"

# 这个路径要改成你下载的的chromedriver的存放地址
service = Service(executable_path="/home/xiayan/myenv/chromedriver-linux64/chromedriver")
driver = webdriver.Chrome(options, service)

driver.get("https://baidu.com")
print(driver.title)
