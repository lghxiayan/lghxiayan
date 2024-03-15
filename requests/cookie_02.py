import requests

url = 'http://84.52.16.1/s-admin/index.html?v=20200116'
data = {
    'dldm': 'j289103',
    'dlmm': 'xia11111111'
}
session = requests.session()
resp = session.get(url, data=data)
resp.encoding = 'utf-8'
# print(resp.text)
print(resp.cookies)
