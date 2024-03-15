string = '<CAP>u2f<CAP>sd<CAP>gv<CAP>k<CAP>x<CAP>1/lhjq<CAP>f<CAP>mn5njua/dinv<CAP>zvw<CAP>w<CAP>n<CAP>xc<CAP>u<CAP>xvu<CAP>l<CAP>u6n<CAP>uv<CAP>zz<CAP>uzv<CAP>z5<CAP>aa<CAP>z<CAP>k7t2<CAP>udkws<CAP>rn<CAP>xc<CAP>k<CAP>jnc<CAP>l<CAP>qcqu<CAP>s<CAP>y<CAP>l<CAP>byu<CAP>h<CAP>1j20<CAP>o<CAP>7i<CAP>u<CAP>kdog==h'

s = string.split('<CAP>')
s1 = ''
print(s)
for i in range(len(s)):
    if i % 2 == 0:
        s1 += s[i]
    else:
        s1 += s[i].upper()

print(s1)


