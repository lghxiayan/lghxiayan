from lxml import etree
import requests

# resp = requests.get('a.html')
with open('a.html') as f:
    resp = f.read()

# print(resp)
# html = '<html><body><h1>This <a>is a </a>test</h1></body></html>'
tree = etree.HTML(resp)
result = tree.xpath("//h1")[0].xpath("string(.)")
print(result)
# s1 = etree.tostring(result[0], method='text')
# print(s1)
