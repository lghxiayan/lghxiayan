import random

keyspace = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}'

flag = 'DASCTF{%s}' % ("".join(random.sample(keyspace[:-2], 32)))
print(flag)

keyspace = "".join(random.sample(keyspace, len(keyspace)))
print('keyspace =', keyspace)

col = 4
period = 7

darr = []
cs = ''
for i in range(len(flag)):
    a = keyspace.find(flag[i])
    b = a // col ** 2 + 1
    c = (a - (b - 1) * col ** 2) // col + 1
    d = (a - (b - 1) * col ** 2) % col + 1
    darr.append([b, c, d])
for i in range(len(flag) // period + 1):
    for j in range(3):
        for k in range(period * i, period * (i + 1)):
            try:
                cs += str(darr[k][j])
            except:
                pass
c = ''
for i in range(0, len(cs), 3):
    c += keyspace[(int(cs[i]) - 1) * col ** 2 + (int(cs[i + 1]) - 1) * col + int(cs[i + 2]) - 1]
print('c =', c)

'''
keyspace = jIx8fuCylrDa}pYh5wE0g7e1GQovtB9LnUN{SFWiPmK4VRkZJH623AdzqOcsbXTM
c = YYm1EEiHUR9Ntx16kjtVXFWejRBBh281JqEzJocl
'''
