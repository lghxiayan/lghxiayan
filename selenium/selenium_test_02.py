from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time

# 设置Chrome驱动的路径
# 我将123.0.6312.122版本的chrome和chromedriver都放在了这个目录中
service = ChromeService(executable_path="D:\\google_chrome\\chromedriver-win64\\chromedriver.exe")

# 使用Chrome驱动创建浏览器实例
driver = webdriver.Chrome(service=service)
# 打开B站网站
driver.get('http://www.bilibili.com')
# 在搜索框中输入'python'
# driver.find_element(By.CLASS_NAME, "nav-search-input").send_keys('python')
# driver.find_element(By.CLASS_NAME, "nav-search-btn").click()
driver.find_element(By.TAG_NAME, "input").send_keys('python')

# 关闭浏览器实例
time.sleep(5)
# driver.close()
driver.quit()
