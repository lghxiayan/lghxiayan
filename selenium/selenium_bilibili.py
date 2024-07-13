from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time
from selenium.webdriver import ActionChains, Keys

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

"""
初始化Chrome驱动，访问B站并搜索'python'视频
"""

# 设置Chrome驱动的路径
# 我将123.0.6312.122版本的chrome和chromedriver都放在了这个目录中
service = ChromeService(executable_path='D:\\google_chrome\\chromedriver-win64\\chromedriver.exe')

# 使用Chrome驱动创建浏览器实例
driver = webdriver.Chrome(service=service)
# driver.maximize_window()
# 打开B站网站
driver.get('http://www.bilibili.com')
driver.implicitly_wait(20)
driver.maximize_window()

# print(driver.name)
# print(driver.window_handles)
# print(driver.current_window_handle)
# print(driver.get_log('browser'))
# driver.save_screenshot('foo.png')
# driver.get_screenshot_as_file('foo1.pdf')

# 在搜索框中输入'python'
search_input = driver.find_element(By.CLASS_NAME, "nav-search-input")

actions = webdriver.ActionChains(driver)
actions.send_keys_to_element(search_input, '测试').perform()

time.sleep(3)
actions.key_down(Keys.SHIFT).send_keys('p').key_up(Keys.SHIFT).send_keys('ython').perform()
time.sleep(2)
# actions.move_by_offset(0, 20).perform()
# search_input.send_keys('python')
el1 = driver.find_element(By.CLASS_NAME, "nav-search-btn")
actions.click_and_hold(search_input).move_to_element(el1).release().perform()
# actions.move_to_element(el1).perform()
time.sleep(2)
# actions.move_to_element_with_offset(el1, 20, 20).context_click(el1).perform()
actions.scroll_by_amount(0, 5000).perform()
time.sleep(2)
actions.scroll_by_amount(0, 5000).perform()
time.sleep(2)
actions.scroll_by_amount(0, 5000).perform()
# actions.context_click(el1).perform()


# el1.screenshot('el.png')
# print(el1.text, el1.tag_name)

# WebDriverWait(driver, 10).until(lambda x: driver.find_element(By.CLASS_NAME, "nav-search-btn"))

# actions = webdriver.ActionChains(driver)
# actions.double_click(el1).perform()
# print('iHaveADream')

# el1.click()
time.sleep(20)

# elements = driver.find_elements(By.CLASS_NAME, "channel-link")
# for ele in elements:
#     print(ele.text)
# 等待30秒，以便查看搜索结果
time.sleep(5)
# 关闭浏览器实例
# driver.close()
