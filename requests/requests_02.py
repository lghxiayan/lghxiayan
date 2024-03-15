import requests

url = 'https://fanyi.baidu.com/sug'
data = {"kw": "dog"}
resp = requests.post(url, data=data)
print(resp.json())
