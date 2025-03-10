import re
import urllib.parse

# 更改为自己从wireshark提取出的csv文件地址
f = open(r"a2.csv")
lines = f.readlines()
datas = []
# 转码, 保存进datas
for line in lines:
    datas.append(urllib.parse.unquote(line))
# print(datas)
lines = []  # 懒得改, 就复用一下, 这个lines保存注入flag的url
for i in range(len(datas)):  # 提取出注入flag的url
    if datas[i].find("!=") > 0:
        lines = datas[i:]
        break
print(lines)
flag = {}
# 用正则匹配
macth1 = re.compile(r"LIMIT 0,1\),(\d*?),1\)\)>(\d*?) HTTP/1.1")
macth2 = re.compile(r'"HTTP","(\d*?)","HTTP/1.1 200 OK')
for i in range(0, len(lines), 2):  # 因为有返回响应, 所以步长为2
    get1 = macth1.search(lines[i])
    if get1:
        key = int(get1.group(1))  # key保存字符的位置
        value = int(get1.group(2))  # value保存字符的ascii编码
        get2 = macth2.search(lines[i + 1])
        if get2:
            if int(get2.group(1)) > 450:
                value += 1
        flag[key] = value  # 用字典保存flag
f.close()
result = ''
for value in flag.values():
    result += chr(value)
print(result)
