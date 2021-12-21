# encoding=UTF-8
# 导入用到的python包
import os
import math
import csv
import oknlp



# 加载停止词
stopwords_path = '/Users/wongrhuipoh/Downloads/第九讲代码/stopwords.txt'
stopwords = []
for line in open(stopwords_path):
    stopwords.append(line.strip())

# 初始化分词
cws = oknlp.cws.get_by_name("thulac")

# 加载word-df
words_df_path = '/Users/wongrhuipoh/PycharmProjects/pythonProject13/words_df.txt'
words_df = {}
total_docs = 0
k = 0
total_df = 0
first_line_flag = True
for line in open(words_df_path):
    if first_line_flag:
        total_docs = int(line.strip())
        first_line_flag = False
    else:
        content = line.strip().split(' ')
        # exclude ''
        if len(content) != 2:
            continue
        word, df = content
        words_df[word] = int(df)
        k += 1
        total_df += words_df[word]

ave_df = total_df/k
print(ave_df)



# 需要提取关键词的文章
# article = '受南京大学邀请，以中国科学院院士、浙江大学教授杨树峰领衔的专家组对南京大学地球科学与工程学院（以下简称“地科院”）开展院系本科教学评估工作。'
# 此处是爬虫爬取的文章路径
file_path = '/Users/wongrhuipoh/PycharmProjects/pythonProject13/comment'
files = os.listdir(file_path) #获取该文件夹下所有的文件名称
articles = []
for fname in files:
    fin = open('/Users/wongrhuipoh/PycharmProjects/pythonProject13/comment/' + fname)
    articles.append({'content': fin.read()})
    fin.close()
print(len(articles))

words_tfidf = {}
words_tf = {}
result = {}
for article in articles:
    # print("======================")
    # 使用分词
    words = cws([article['content']])[0]

    # 计算tf
    for word_tuple in words:
        word = word_tuple
        word = word.strip()
        if word in stopwords:
            continue
        # 去掉停止词
        # 统计词频
        if word in words_tf:
            words_tf[word] += 1
        else:
            words_tf[word] = 1

    # 计算tfidf

    for word, tf in words_tf.items():
        # 如果出现了word_df中未出现的词，为其设置一个默认值
        if not word in words_df:
            words_df[word] = ave_df  # 5是对df取的均值
        words_tfidf[word] = float(tf) * math.log(total_docs / words_df[word] + 1)
    # 结果排序之后输出

file = []
with open('/Users/wongrhuipoh/PycharmProjects/pythonProject13/article_info.json', 'w', encoding='utf8') as f:
    for word, tfidf in sorted(words_tfidf.items(), key=lambda d: d[1], reverse=True)[:2000]:
        result[word] = tfidf
    print(result)
    f.write(json.dumps(result, ensure_ascii=False))

with open('/Users/wongrhuipoh/PycharmProjects/pythonProject13/article_info.csv', 'w', newline='') as csvfile:
    for word, tfidf in sorted(words_tfidf.items(), key=lambda d: d[1], reverse=True)[:30]:
        file.append({'词语': word, '比重': tfidf})
    fieldnames = ('词语', '比重')
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for con in file:
        writer.writerow(con)

#     # 保存tf-idf的值


#
#
