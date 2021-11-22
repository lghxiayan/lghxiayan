f = open("latex.log", 'r')
txt = f.readlines()
f.close()

dict = {}
for line in txt:
    dict[line] = dict.get(line, 0) + 1

for x in list(dict.items()):
    if x[1] == 1:
        continue
    else:
        del dict[x[0]]

print("共{}独特行".format(len(dict)))
