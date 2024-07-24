import requests

# 假设这是你想要获取cookie的服务器URL
url = 'http://84.52.16.1/s-admin/index.html?v=20200116'

# 服务器设置的JSESSIONID cookie值
jsessionid_cookie = '6G91mhmVLfJ4TV2V11htnypD3LX83n0QncLgwnf9hQLHTsZyBKK4!-2102725246'

# 创建一个RequestsCookieJar对象，并设置JSESSIONID cookie
cookie_jar = requests.cookies.RequestsCookieJar()
cookie_jar.set('JSESSIONID', jsessionid_cookie)

# 发送一个POST请求，并传递cookie jar
response = requests.post(url, cookies=cookie_jar)

# 获取所有设置的cookie
cookies = response.cookies

# 检查是否有名为JSESSIONID的cookie
if 'JSESSIONID' in cookies:
    # 打印JSESSIONID的值
    print(f"JSESSIONID: {cookies['JSESSIONID']}")
else:
    print("JSESSIONID cookie not found in the response.")
