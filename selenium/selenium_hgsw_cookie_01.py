"""
该脚本使用Selenium自动化进行网页操作，具体流程如下：
1. 打开指定网址并登陆；
2. 点击进入子系统，选择特定的页面；
3. 在页面上填写信息、选择接收对象，并发送信息；
4. 完成后关闭浏览器。

注意：该脚本依赖于具体的网页结构和元素ID、CSS选择器等，若网页结构发生变化，脚本可能无法正常工作。
"""
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import mysql

# 初始化Chrome驱动
service = Service(executable_path='D:\\google_chrome\\chromedriver-win64\\chromedriver.exe')
driver = webdriver.Chrome(service=service)
# 打开指定网页
driver.get('http://84.52.16.1/s-admin/index.html?v=20200116')
# 设置隐式等待时间
driver.implicitly_wait(10)
# 最大化窗口
driver.maximize_window()
#
# # 输入用户名和密码，点击登录
# driver.find_element(By.ID, 'dldm').send_keys('j289103')
# driver.find_element(By.ID, 'dlmm').send_keys('xia11111111')
# driver.find_element(By.ID, 'btn-login').click()
# time.sleep(1)
#
# # 点击进入子系统，进一步选择页面
# driver.find_element(By.XPATH, '//*[contains(text(),"子系统")]').click()
# # 进入特定的子页面
# driver.find_element(By.CSS_SELECTOR, 'a[href="/s-email/index.html?type=sjx"]').click()
# driver.find_element(By.CSS_SELECTOR, 'a[href="publish.html"]').click()
# time.sleep(1)
#
# # 填写信息，选择接收对象
# driver.find_element(By.XPATH, '//input[@placeholder="标题建议不要超过23个汉字"]').send_keys('test11')
# driver.find_element(By.XPATH, '//button[contains(text(),"选择接收对象...")]').click()
# time.sleep(1)
# driver.find_element(By.XPATH, '//span[@title="夏燕"]').click()
# time.sleep(1)
# driver.find_element(By.XPATH, '//button[contains(text(),"确定")]').click()
# time.sleep(3)
#
# # 进入iframe，输入内容
# driver.switch_to.frame(0)
# driver.find_element(By.XPATH, '/html/body').click()
# ActionChains(driver).send_keys('helloWorld').perform()
# time.sleep(1)
#
# # 退出iframe
# driver.switch_to.default_content()
#
# # 发送信息
# driver.find_element(By.XPATH, '//button[@id="fasong"]').click()
# time.sleep(1)
#
# # 确认发送
# driver.find_element(By.XPATH, '//span[contains(text(),"确定")]').click()
# time.sleep(3)


# 添加Cookies
# 假设你已经有了Cookies，格式如下：
# cookies = [
#     {'name': 'cookie_name', 'value': 'cookie_value', 'domain': '.example.com', 'path': '/'}
# ]
cookies = [
    {'domain': '84.52.16.1', 'httpOnly': True, 'name': 'JSESSIONID', 'path': '/', 'sameSite': 'Lax', 'secure': False,
     'value': '92qLmZKYLHwbVLpMny1dBynyP8cfC1cXS3HhrdNJSs3MyJp22zx9!-2102725246'}
]

for cookie in cookies:
    driver.add_cookie(cookie)

# 再次访问网页，这时应该已经应用了Cookies
driver.get('http://84.52.16.1/s-admin/index.html?v=20200116')

time.sleep(10)
# 获取网页内容
page_content = driver.page_source

# 打印网页内容
# print(driver.get_cookies())
print(page_content)

# 关闭浏览器
driver.close()
driver.quit()
