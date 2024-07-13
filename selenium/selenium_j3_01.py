from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import time

# 设置Chrome驱动的路径
# 我将123.0.6312.122版本的chrome和chromedriver都放在了这个目录中
service = ChromeService(executable_path="D:\\google_chrome\\chromedriver-win64\\chromedriver.exe")

# 使用Chrome驱动创建浏览器实例
driver = webdriver.Chrome(service=service)
driver.get('http://portal.hbsw.tax.cn/sword?ctrl=MH003InitLoginxxCtrl_openWin')

# 设置页面加载策略
driver.implicitly_wait(10)  # 隐式等待
driver.set_page_load_timeout(30)  # 页面加载超时
title = driver.title


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
    ActionChains(driver).drag_and_drop_by_offset(huakuai, 340, 0).perform()
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[@class='el-button btn_login el-button--primary el-button--small']").click()
    time.sleep(10)

    # print(driver.current_url)
    # source1 = driver.page_source
    # print(source1)

    # driver.find_element(By.XPATH, "//span[text()='金税三期']").click()
    # time.sleep(1)
    time.sleep(3)


def j3():
    driver.find_element(By.XPATH, "//input[@name='search']").send_keys('监管人员信息查询')
    time.sleep(3)
    driver.find_element(By.XPATH, "//input[@name='search']").send_keys(Keys.RETURN)
    time.sleep(3)
    driver.find_element(By.XPATH, "//span[contains(text(),'监管人员信息查询[综合查询岗]')]").click()
    time.sleep(30)

    iframe = driver.find_element(By.CLASS_NAME, "frametabDiv")
    driver.switch_to.frame(iframe)
    time.sleep(10)

    driver.find_element(By.XPATH, "//span[contains(text(),'领导小组')]").click()
    time.sleep(30)

    # driver.find_element(By.XPATH, "//input[@name='DJRQQ']").clear()
    # driver.find_element(By.XPATH, "//input[@name='DJRQQ']").send_keys('2024-01-01')
    # time.sleep(3)
    # driver.find_element(By.XPATH, "//span[contains(text(),'执行查询')]").click()
    # time.sleep(300)


if __name__ == '__main__':
    if title == "统一身份管理平台":
        login()

    j3()
    print('不用登录')

    # driver.close()
    # driver.quit()
