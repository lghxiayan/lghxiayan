from pycipher import ADFGVX
from base64 import b64encode
from secret import flag

assert len(flag)==40
assert flag[:7]=='DASCTF{'

m1 = flag[7:27]
print('c1 =',b64encode(m1.encode())[::-1].decode())

m2 = flag[27:-1]
c2 = ADFGVX('6s5xc21d0aro3luyenj74mthvfpgiwzkbq98','helloadfgvx').encipher(m2)
print('c2 =',c2)

'''
c1 = =ADN4gjMkhjZmdjM4ADN1QTYlNDO
c2 = DVVGGAGGVVDDGDDGDVVAADAD
'''