import json
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from wordcloud import WordCloud

with open('/Users/wongrhuipoh/PycharmProjects/pythonProject13/article_info.json', 'r', encoding='utf8') as f:
    data = json.load(f)

mask_image = np.array(Image.open('/Users/wongrhuipoh/Downloads/mask doge.jpg'))

#建立颜色数组，可更改颜色
color_list=['#6F4E37','#E1C16E','#DAA06D','#E97451','#6E260E','#C19A6B','#722F37','#F5DEB3',
            '#C2B280','#A95C68','#808000','#F2D2BD']

#调用
color=colors.ListedColormap(color_list)
wordc = WordCloud(font_path='/Users/wongrhuipoh/Library/Fonts/华康海报体W12.TTF',
                      mask=mask_image,
                      width=1200,
                      height=1500,
                      max_words=900,
                      scale=2,
                      colormap=color,
                      max_font_size=120,
                      background_color='white'
                      ).generate_from_frequencies(data)

# 将生成的wordcloud图片保存
wordc.to_file('/Users/wongrhuipoh/PycharmProjects/pythonProject13/wc.png')

# 将生成的wordcloud图片打开显示出来
plt.imshow(wordc)
plt.axis("off")
plt.show()
