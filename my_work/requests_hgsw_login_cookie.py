import requests

WEB_HEADERS = {
    'Host': '84.52.16.1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'X-Requested-With': 'XMLHttpRequest',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'http://84.52.16.1/s-admin/index.html?v=20200116',
    # 'Cookie': ''}
    'Cookie': 'JSESSIONID=sGTmmfyLBpxLhTN44v42Hzg8y1jv70FVdpvTLSWyLPTng7SwNFmJ!-2102725246'}

# 创建Session对象
# session = requests.Session()
session = requests.session()

url = 'http://84.52.16.1/s-admin/index.html?v=20200116'
# 登录数据
data = {
    'dldm': 'j289103',
    'dlmm': 'xia11111111'
}

# 发送登录请求
try:
    response = session.post(url, headers=WEB_HEADERS)
    # response = session.post(url)
    response.encoding = 'UTF-8'
    # print(response.text)  # 成功
    # 检查响应状态码
    if response.status_code == 200 and '个人资料1' in response.text:
        print("使用WEB_HEADERS登录成功")
        # print(response.text)
    else:
        print("登录失败,使用用户名和密码登录")
        login_response = session.post('http://84.52.16.1/s-admin/login.html?v=20191023', data=data, json=data)
        login_response.encoding = 'UTF-8'
        # print(login_response.text)
        print(login_response.request, login_response.request.headers, login_response.cookies)
        for value in login_response.request.headers.items():
            print(value)
        for cookie in login_response.cookies.items():
            print(cookie)
        if login_response.status_code == 200 and '个人资料' in response.text:
            print("登录成功")
            # print(response.text)
        else:
            print("使用用户名和密码登录，登录失败。")
except Exception as e:
    print("登录失败，原因：", e)
