# base.py
# base全家桶


import base64

'''
Base16特征:
0-9 A-F
偶数
'''


def base16encode(text):
    return base64.b16encode(text.encode('utf-8')).decode('utf-8')


def base16decode(text):
    if len(text) % 2:
        print('error')
    return base64.b16decode(text.upper()).decode('utf-8')


'''
Base32特征：
A-Z 0-7
补等号至8的倍数
'''


def base32encode(text):
    return base64.b32encode(text.encode('utf-8')).decode('utf-8')


def base32decode(text):
    return base64.b32decode(text + '=' * ((8 - len(text) % 8) % 8)).decode('utf-8')


'''
Base64特征:
0-9 a-z A-Z +/
补等号至4的倍数
'''


def base64encode(text):
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')


def base64decode(text):
    return base64.b64decode(text + '=' * ((4 - len(text) % 4) % 4)).decode('utf-8')


'''
Base85特征:
0-9 a-z A-Z
.-:+=^!/*?&<>()[]{}@%$#
'''


def base85encode(text):
    return base64.b85encode(text.encode('utf-8')).decode('utf-8')


def base85decode(text):
    return base64.b85decode(text).decode('utf-8')


'''
Base58特征:
相比Base64，Base58不使用数字"0"，字母大写"O"，字母大写"I"，和字母小写"l"，以及"+"和"/"符号。
'''


def base58encode(s):
    b58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    result = ''
    temp = 0
    for c in s:
        temp = temp * 256 + ord(c)
    while temp > 0:
        result = b58[temp % 58] + result
        temp = temp // 58
    return result


def base58decode(s):
    b58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    result = ''
    temp = 0
    for c in s:
        temp = temp * 58 + b58.find(c)
    while temp > 0:
        result = chr(temp % 256) + result
        temp = temp // 256
    return result


'''
Base8特征:
0-7
'''


def base8encode(s):
    b8 = '01234567'
    result = ''
    temp = 0
    for c in s:
        temp = temp * 256 + ord(c)
    while temp > 0:
        result = b8[temp % 8] + result
        temp = temp // 8
    return result


def base8decode(s):
    b8 = '01234567'
    result = ''
    temp = 0
    for c in s:
        temp = temp * 8 + b8.find(c)
    while temp > 0:
        result = chr(temp % 256) + result
        temp = temp // 256
    return result


'''
DIY base编解码
'''
baseList = '0123456789abcdef'  # 在此处自定义索引表


def baseAllencode(s):
    listlen = len(baseList)
    result = ''
    temp = 0
    for c in s:
        temp = temp * 256 + ord(c)
    while temp > 0:
        result = baseList[temp % listlen] + result
        temp = temp // listlen
    return result


def baseAlldecode(s):
    listlen = len(baseList)
    result = ''
    temp = 0
    for c in s:
        temp = temp * listlen + baseList.find(c)
    while temp > 0:
        result = chr(temp % 256) + result
        temp = temp // 256
    return result


if __name__ == "__main__":
    str = input("input base code:")
    for i in ['8', '16', '32', '64', '58', '85']:
        try:
            eval("print(base" + i + "decode(str))")
        except:
            pass
    input()
