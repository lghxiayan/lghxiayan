from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import time


def auto():
    # options = Options()
    # options.binary_location = r"D:\edgedriver_win64\msedge.exe"
    # driver = webdriver.Edge(options=options)

    driver = webdriver.Edge()
    driver.get("https://etax99.hubei.chinatax.gov.cn:5100/")
    element = driver.find_element(By.ID, 'sb_form_q')
    element.send_keys("WebDriver")
    element.submit()

    time.sleep(10)
    driver.quit()


if __name__ == "__main__":
    # for i in range(10):
    auto()
