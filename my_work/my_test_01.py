import requests
import logging

logging.basicConfig(level=logging.DEBUG)
from http.cookies import SimpleCookie

# 假设这是登录的URL和登录表单的参数
# login_url = 'http://84.52.16.1/s-admin/login'
login_url = 'http://84.52.16.1/s-admin/index.html?v=20200116'
login_data = {
    'dldm': 'j289103',
    'dlmm': 'xia11111111'
}
# 创建一个Session对象
session = requests.Session()

# 发送POST请求进行登录
response = session.post(login_url, data=login_data)
response.encoding = 'utf-8'
print(response.text)

# 此时，session对象会自动保存登录后返回的cookies
# 使用session对象发送后续请求，它会自动携带cookies
response = session.get(login_url)

# 输出响应内容
print(response.text)
