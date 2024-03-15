from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

data = b'secret data'

# key = get_random_bytes(16)
key = b'\x13\x82m\xae\xacT\xef\xd3s\xce\x16llx\x85s'
print(type(key), key)

cipher = AES.new(key, AES.MODE_EAX)
print(type(cipher), cipher)

ciphertext, tag = cipher.encrypt_and_digest(data)
print(type(ciphertext), ciphertext)
print(type(tag), tag)

file_out = open('encrypted.bin', 'wb')
[file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
file_out.close()
