# 将得到的baseinfoSet_TELECOMPASSWORD替换string字符串。记得去掉最后一个&
string = '120&105&112&105&103&115&113&101&104&113&109&114&55&56&53&50&55&53&57&55'
list1 = string.split("&")

result = ''

for i in list1:
    if len(result) <= 11:
        result += chr(int(i) - 4)
    else:
        result += chr(int(i))

print('密码为：' + result)
