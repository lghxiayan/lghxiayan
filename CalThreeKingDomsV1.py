import jieba

txt = open('threekingdoms.txt', 'r', encoding='utf-8').read()
words = jieba.lcut(txt)
dict = {}
exclude = ['却说', '二人', '不可', '荆州', '不能', '如此', '将军', '商议', '如何', '主公', '军士', '左右', '军马', '引兵', '次日', '大喜', '天下', '东吴']
for word in words:
    if len(word) == 1:
        continue
    elif word == '孔明曰':
        rword = '孔明'
    elif word == '玄德曰' or word == '玄德':
        rword = '刘备'
    elif word == '关公' or word == '云长':
        rword = '关羽'
    elif word == '丞相' or word == '孟德':
        rword = '曹操'
    else:
        rword = word
    dict[rword] = dict.get(rword, 0) + 1
for word in exclude:
    del dict[word]
# print(dict)
listtxt = list(dict.items())
listtxt.sort(key=lambda x: x[1], reverse=True)
for i in range(15):
    word, count = listtxt[i]
    print("{:<15}{:>5}".format(word, count))
