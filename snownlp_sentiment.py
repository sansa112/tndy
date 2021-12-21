# 神经网络模型
import paddle
import paddlehub
import json
import csv
import os

file_path = '/Users/wongrhuipoh/PycharmProjects/pythonProject13/comment'
files = os.listdir(file_path) #获取该文件夹下所有的文件名称
articles = []
for fname in files:
    fin = open('/Users/wongrhuipoh/PycharmProjects/pythonProject13/comment/' + fname)
    articles.append(fin.readlines())
    fin.close()

senta = paddlehub.Module(name="senta_bilstm")
input_dict = {"text": articles}
results = senta.sentiment_classify(data=input_dict)
file_con = []
k = 0
n = 0
for i in range(len(results)):
    k += 1
    con = results[i].get('sentiment_label')
    con2 = results[i].get('sentiment_key')
    p_rate = results[i].get('positive_probs')
    n += p_rate
    n_rate = results[i].get('negative_probs')
    file_con.append({'序号': k, '标签号': con, '情感标签': con2, '正向率': p_rate, '负向率': n_rate})

ave_p  = n / k
print(ave_p)
# with open('/Users/wongrhuipoh/PycharmProjects/pythonProject13/情感分析.csv', 'w', newline='') as csvfile:
#     fieldnames = ('序号', '标签号', '情感标签', '正向率', '负向率')
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     for con in file_con:
#         writer.writerow(con)


