from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import random

# 设置Chrome选项以避免被识别为自动化控制
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_argument("--incognito")  # 无痕模式
# chrome_options.add_argument("start-maximized")  # 最大化窗口

# 设置代理（如果需要）
# proxy = Proxy()
# proxy.proxy_type = ProxyType.MANUAL
# proxy.http_proxy = "your_http_proxy:port"
# proxy.socks_proxy = "your_socks_proxy:port"
# proxy.ssl_proxy = "your_ssl_proxy:port"
# capabilities = webdriver.DesiredCapabilities.CHROME
# proxy.add_to_capabilities(capabilities)

# 创建WebDriver实例
service = ChromeService(executable_path=("D:\google_chrome\chromedriver-win64\chromedriver.exe"))
driver = webdriver.Chrome(service=service, options=chrome_options)

# driver = webdriver.Chrome(options=chrome_options, executable_path=(ChromeDriverManager().install()))

# 设置用户代理
driver.execute_cdp_cmd("Network.setUserAgentOverride", {
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.61 Safari/537.36"})

# 设置窗口大小
driver.set_window_size(1920, 1080)

# 设置页面加载策略
driver.implicitly_wait(10)  # 隐式等待
driver.set_page_load_timeout(30)  # 页面加载超时

# 访问目标网站
driver.get("http://84.52.16.1")

# 模拟用户行为
try:
    # 等待元素加载并模拟点击
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="someElementId"]'))).click()

    # 模拟键盘输入
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys("some search terms" + Keys.RETURN)

    # 模拟滚动页面
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(2, 5))  # 随机等待时间

    # 其他用户行为...

except Exception as e:
    print(e)

finally:
    # 关闭浏览器
    driver.quit()
