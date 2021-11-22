import wordcloud
import jieba
from imageio import imread

mask = imread("fivestar2.png")
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

w = wordcloud.WordCloud(width=1000, height=700, font_path='msyh.ttc', background_color='white', mask=mask)
w.generate(' '.join(words))
w.to_file("2.png")
