# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service as ChromeService


class TestSearchHelloWorld():
    def setup_method(self, method):
        self.service = ChromeService(executable_path='D:\\google_chrome\\chromedriver-win64\\chromedriver.exe')
        self.driver = webdriver.Chrome(service=self.service)
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_searchHelloWorld(self):
        # Test name: SearchHelloWorld
        # Step # | name | target | value
        # 1 | store | https://www.baidu.com | baiduURL
        self.vars["baiduURL"] = "https://www.baidu.com"
        # 2 | open | ${baiduURL} | 
        self.driver.get(self.vars["baiduURL"])
        # 3 | store | id=kw | baiduTextboxLocator
        self.vars["baiduTextboxLocator"] = "id=kw"
        # 4 | store | hello world | searchContent
        self.vars["searchContent"] = "hello world"
        # 5 | type | id=kw | ${searchContent}
        self.driver.find_element(By.ID, "kw").send_keys(self.vars["searchContent"])
        # 6 | click | id=su | 
        self.driver.find_element(By.ID, "su").click()
        # 7 | waitForElementVisible | xpath=//span[contains(text(),' - 百度百科')] | 30000
        WebDriverWait(self.driver, 30).until(
            expected_conditions.visibility_of_element_located((By.XPATH, "//span[contains(text(),\' - 百度百科\')]")))
        # 8 | assertElementPresent | xpath=//span[contains(text(),' - 百度百科')] | 
        elements = self.driver.find_elements(By.XPATH, "//span[contains(text(),\' - 百度百科\')]")
        assert len(elements) > 0