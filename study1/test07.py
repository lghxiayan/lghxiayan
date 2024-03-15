import wordcloud
import jieba

f = open("新时代中国特色社会主义.txt", 'r', encoding='utf8')
txt = f.read()
f.close()
txt = jieba.lcut(txt)
words = []
for word in txt:
    if len(word) < 2:
        continue
    else:
        words.append(word)
print(words)

w = wordcloud.WordCloud(width=1000, height=700, font_path='msyh.ttc', background_color='white', max_words=15)
w.generate(' '.join(words))
w.to_file("2.png")
