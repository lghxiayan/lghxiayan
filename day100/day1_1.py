a, b = 0, 1
while b < 10000:
    print(b, end=',')
    a, b = b, a + b
