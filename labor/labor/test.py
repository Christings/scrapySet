# import re
# import requests

# content="<p><h>微风红伟未发货\n\n\t\s设为首页使用百度前必读意见反馈京证号京公网安备号后端数据'"

# content = re.sub(r'设为首页使用百度前必读意见反馈京证号京公网安备号后端数据', '', content)
# # content = re.sub(r'[ \xa0?]+', ' ', content)
# # content = re.sub(r'\s*\n\s*', '\n', content)
# # content = re.sub(r'\s*(\s)', r'\1', content)

# print(content)

# url="https://k.sina.com.cn/article_3121600265_ba0fd70900100vwgj.html"

# result=requests.get(url=u)

import collections
from typing import TextIO
import pandas as pd
from collections import Counter

def del_stopword(path="data/content.txt"):
#     df=pd.read_csv(path)
# #     print(df.head())
#     # df["cut"]=df["content"].apply(lambda x:list(jieba.cut(x)))
#     # df.head()
#     stopwords=pd.read_csv("data/stopwords/stopwords.txt", names=["stopword"], delimiter="\t", quoting=csv.QUOTE_NONE, encoding='utf-8')
# #     print(stopwords.head())
#     stop_list=stopwords['stopword'].tolist()
    df['cut'] = df['content'].apply(lambda x : [i for i in jieba.cut(x) if i not in stop_list])
# #     print(df.head())

#     result=[]
#     for index,row in df.iterrows():
#         result+=row["cut"]
    
#     highwords=Counter(result)
#     print(highwords.most_common(500))
#     df["cut"].to_csv("data/content_cut.txt", header="content", index=False)

    df=pd.read_csv("data/content_cut.txt")
    
    result=[]
    for index,row in df.iterrows():
        row=row[0].split(" ")
        for each in row:
            if len(each) >= 3:
                print(each)
    
    # highwords=Counter(result)

    # for k,v in highwords.items():
    #     print(k,v)
del_stopword()