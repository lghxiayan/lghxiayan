import requests

url = 'http://84.52.16.1/s-admin/login.html'

# resp = requests.get(url)
# resp.encoding = 'utf-8'
# html = resp.text
# print(html)

data = {
    'cloud_dldm': "j289103",
    'cloud_dlmm': "D2CC32491D85682ABC772328E7A645A8"
    # 'cloud_dlmm': "xia11111111"
}

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
}

session = requests.session()
resp = session.get(url, data=data, headers=header)
resp.close()
resp.encoding = 'utf-8'
html = resp.text
print(html)
