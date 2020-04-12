import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.base import BaseEstimator,TransformerMixin
from collections import defaultdict
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier

class MajorityVotingTagger(BaseEstimator,TransformerMixin):
    """
    投票模型进行实体命名识别
    precision 最终0.94
    """
    def __init__(self):
        self.tags=[]
        self.mjvote=dict()

    def fit(self,X,y):
        """
        X: list of words
        y: list of tag
        """
        word2cnt= dict()
        # self.tags=[]
        for x, t in zip(X,y):
            if t not in self.tags:
                self.tags.append(t)
            if x in word2cnt:
                if t in word2cnt[x]:
                    word2cnt[x][t] +=1
                else:
                    word2cnt[x][t] = 1
            else:
                word2cnt[x] = {t:1}

        for k,v in word2cnt.items():
            self.mjvote[k]=max(v,key=v.get)

    def predict(self, X, y=None):
        """
        Predict the the tag from memory. If word is unknown, predict 'O'.
        """
        return [self.mjvote.get(x, 'O') for x in X]


def analyse_data(path):
    data=pd.read_csv(path,sep=',',encoding='latin1')
    print(r'data info\n {}'.format(data.info()))
    print('---'*7)
    print(f'data describe\n {data.describe()}')
    print('---'*7)
    print(f'data null distribution\n {data.isnull().sum()}')
    # sentence # 这一列进行缺失值的填充
    data=data.fillna(method='ffill')
    print(f'data null distribution\n {data.isnull().sum()}')
    print(r'clean data done')
    return data

def precision_report(words,tags):
    pred=cross_val_predict(estimator=MajorityVotingTagger(),X=words,y=tags,cv=5)
    report= classification_report(y_pred=pred,y_true=tags)
    print(report)

def main():
    root= Path.cwd()
    path = root / r'KnowledgeGraph\NLP\data\NER\ner_dataset.csv'
    data= analyse_data(path)
    words=data['Word'].values.tolist()
    tags=data['Tag'].values.tolist()
    precision_report(words,tags)

if __name__ == "__main__":
    main()