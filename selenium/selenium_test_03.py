from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService, Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

# 设置Chrome驱动的路径
# 我将123.0.6312.122版本的chrome和chromedriver都放在了这个目录中
service = ChromeService(executable_path="D:\\google_chrome\\chromedriver-win64\\chromedriver.exe")

# 使用Chrome驱动创建浏览器实例
driver = webdriver.Chrome(service=service)
# 打开B站网站
# driver.get('https://iviewui.com/view-ui-plus/component/form/radio')
driver.get('https://iviewui.com/view-ui-plus/component/form/date-picker')

# time.sleep(2)
# select = Select(driver.find_element(By.ID, "s1"))
# select.select_by_visible_text('Fax')

driver.find_elements(By.XPATH, "//input[@class='ivu-input ivu-input-default ivu-input-with-suffix']")[1].send_keys(
    '2024-04-18 - 2024-05-22')
# time.sleep(3)
# driver.find_element(By.XPATH, "//li[contains(text(),'北京')]").click()
# time.sleep(3)
# driver.find_element(By.XPATH, "//li[contains(text(),'故宫')]").click()
# driver.find_element(By.CLASS_NAME, "nav-search-btn").click()


# driver.find_element(By.XPATH, '//span[text()="香蕉"]/preceding-sibling::span/input').click()
# time.sleep(3)

# driver.find_element(By.XPATH, "//input[@type='radio' and @class='ivu-radio-input']").click()
# time.sleep(3)
# driver.find_elements(By.XPATH, "//input[@type='radio' and @class='ivu-radio-input']")[3].click()

# driver.find_element(By.CSS_SELECTOR, "#su").click()
# 关闭浏览器实例
time.sleep(3)
# driver.close()
driver.quit()
