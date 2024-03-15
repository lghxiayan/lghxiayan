f = open("latex.log", 'r')
txt = f.read()
f.close()
dict = {}
length_Word = len(txt)

for word in txt:
    dict[word] = dict.get(word, 0) + 1

for key in list(dict):
    if key in "abcdefghijklmnopqrstuvwxyz":
        continue
    else:
        del dict[key]

ls = list(dict.items())
ls.sort(key=lambda x: x[0], reverse=False)
result = []
for x in ls:
    s = "{}:{}".format(x[0], x[1])
    result.append(s)

result2 = ','.join(result)

print("共{}字符,{}".format(length_Word, result2))
