from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 设置Edge浏览器的选项
options = Options()
# 如果您希望浏览器在后台运行，可以添加以下选项
# options.headless = True

# 创建WebDriver实例
service = Service('D:/edgedriver_win64/msedgedriver.exe')  # 替换为您的Edge WebDriver路径
driver = webdriver.Edge(service=service, options=options)

# 打开网址
driver.get('https://etax99.hubei.chinatax.gov.cn:5100/')

# 等待页面加载完成
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'loginButtonID')))

# 点击登录按钮
# 注意：您需要根据实际的HTML元素属性来替换下面的ID
login_button = driver.find_element(By.ID, 'loginButtonID')
login_button.click()

# ...在这里可以继续添加其他操作，比如填写用户名和密码等...

# 当所有操作完成后，关闭浏览器
driver.quit()
