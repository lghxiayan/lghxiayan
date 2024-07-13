from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
import time

# 设置Chrome驱动的路径
# 我将123.0.6312.122版本的chrome和chromedriver都放在了这个目录中
service = ChromeService(executable_path="D:\\google_chrome\\chromedriver-win64\\chromedriver.exe")

# 使用Chrome驱动创建浏览器实例
driver = webdriver.Chrome(service=service)
driver.get('http://tpass.hbsw.tax.cn/')

# 设置页面加载策略
driver.implicitly_wait(10)  # 隐式等待
driver.set_page_load_timeout(30)  # 页面加载超时
driver.maximize_window()


def login():
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[@placeholder='请输入税务人员代码/身份证件号码']").send_keys('54211280004')
    time.sleep(1)
    # 要先点击一下密码栏，否则不能输入密码
    driver.find_element(By.XPATH, "//input[@type='password']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys('L5eZir3BIKu6')
    time.sleep(1)
    # 滑块
    huakuai = driver.find_element(By.XPATH, "//div[@class='drag_bg animate']")
    login_bottom = driver.find_element(By.XPATH,
                                       "//button[@class='el-button btn_login el-button--primary el-button--small']")
    find_pw = driver.find_element(By.XPATH, "//span[text()='找回密码']")
    ActionChains(driver).drag_and_drop(huakuai, find_pw).perform()
    time.sleep(1)
    login_bottom.click()
    time.sleep(10)

    driver.find_element(By.XPATH, "//span[text()='金税三期']").click()
    time.sleep(1)
    time.sleep(100)


if __name__ == '__main__':
    login()

    # driver.close()
    # driver.quit()
