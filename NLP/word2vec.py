from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 只考虑词频
vectorizer=CountVectorizer()
corpus=[
    'this is test sentence',
    'where you want to go'
    'this is your restult'
]
X=vectorizer.fit_transform(corpus)
print(X)
print(X.toarray())
# print(vectorizer.get_feature_names)

#既考虑词频也考虑 词语的重要性(tf-idf)
vectorizer=TfidfVectorizer()
X=vectorizer.fit_transform(corpus)
print(X)
print(X.toarray())
# print(vectorizer.get_feature_names)


# 用sklearn计算余弦相似度
print(r'计算余弦相似度')
x=np.arange(15).reshape(-1,5)
y=np.arange(20).reshape(4,5)
print(x)
print(y)
print(cosine_similarity(x,y))