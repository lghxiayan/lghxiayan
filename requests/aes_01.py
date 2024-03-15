from Crypto.Random import get_random_bytes
import base64

key = get_random_bytes(16)
print(key)

str1 = base64.b64encode(key)
print(type(str1), str1)

result1 = str1.decode('utf-8')
print(type(result1), result1)

print('--' * 50)

str2 = 'U2FsdGVkX1/lhjFmn5nju/dinvZVWwNxcUxvuLu6nUVzUZVz5AAzK7T2udkRNcKjncLqcqSyLbyuH120O7Udog=='
result2 = base64.b64decode(str2)
print(type(result2), result2)

# with open('aes_01.txt', 'wb') as f:
#     f.write(key)
