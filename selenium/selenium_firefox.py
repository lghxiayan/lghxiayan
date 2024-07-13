from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager as GeckoDriverManager
import time



## 报错，懒得处理了。
service = FirefoxService(executable_path=(GeckoDriverManager().install()))
driver = (webdriver.Firefox(service=service))
driver.get("https://etax99.hubei.chinatax.gov.cn:5100")
time.sleep(100)
driver.quit()

