# encoding=UTF-8
# 导入用到的python包
import os
import oknlp


# 加载停止词
stopwords_path = "/Users/wongrhuipoh/Downloads/第九讲代码/stopwords.txt"
stopwords = ['\n']
for line in open(stopwords_path):
    stopwords.append(line.strip())

# 此处是爬虫爬取的文章路径
file_path = '/Users/wongrhuipoh/PycharmProjects/pythonProject13/comment'
files = os.listdir(file_path) #获取该文件夹下所有的文件名称
articles = []
for fname in files:
    fin = open('/Users/wongrhuipoh/PycharmProjects/pythonProject13/comment/' + fname)
    articles.append(fin.read())
    fin.close()

# 存储词和df值的文件
words_df_path = '/Users/wongrhuipoh/PycharmProjects/pythonProject13/words_df.txt'
# 初始化分词
cws = oknlp.cws.get_by_name("thulac")

words_df = {}
cnt = 0
for article in articles:
    words = cws([article])[0]
    article_vocab = []
    for word_tuple in words:
        word = word_tuple
        word = word.strip()
        # 去掉停止词
        if word in stopwords:
            continue
        if word in article_vocab:
            continue
        article_vocab.append(word)
    for word in article_vocab:
        if word not in words_df:
            words_df[word] = 1
        else:
            words_df[word] += 1
    cnt += 1
print(cnt)

# 打开输出文件
output_file = open(words_df_path, 'w')
# 输出文件第一行写入总的文档数
output_file.write(str(cnt) + '\n')
output_dict = {}
for word, rest in words_df.items():
    output_dict[word] = rest
for word, df in sorted(output_dict.items(), key=lambda d: d[1], reverse=True):
    output_file.write(word + ' ' + str(df) + '\n')
output_file.close()
