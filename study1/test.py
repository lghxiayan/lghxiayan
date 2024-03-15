'''
附件是《沉默的羔羊》中文版内容，请读入内容，分词后输出长度大于等于2且出现频率最多的单词。
如果存在多个单词出现频率一致，请输出按照Unicode排序后最大的单词。
'''
import jieba

txt = open('沉默的羔羊.txt', 'r', encoding='utf-8').read()
words = jieba.lcut(txt)
dict = {}
for word in words:
    if len(word) < 2:
        continue
    else:
        dict[word] = dict.get(word, 0) + 1

list = list(dict.items())
list.sort(key=lambda x: x[1], reverse=True)
print(list[0][0])
