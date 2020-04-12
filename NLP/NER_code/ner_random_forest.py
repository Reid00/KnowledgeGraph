import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from ner_majority_voting import MajorityVotingTagger

def word_feature_engineer(word):
    return np.array([word.istitle(),word.islower(),word.isupper(),len(word),word.isdigit(),word.isalpha()])

def get_sentences(data):
    agg_func= lambda s: [(word,pos,tag) for word, pos,tag in zip(s['Word'].values.tolist(),s['POS'].values.tolist(),s['Tag'].values.tolist())]
    sentence_grouped= data.groupby('Sentence #').apply(agg_func)
    return [s for s in sentence_grouped]

def new_features(data):
    out=[]
    y=[]
    mv_tagger = MajorityVotingTagger()
    tag_encoder=LabelEncoder()
    pos_encoder=LabelEncoder()

    words=data['Word'].values.tolist()
    pos=data['POS'].values.tolist()
    tags=data['Tag'].values.tolist()

    mv_tagger.fit(words,tags)
    tag_encoder.fit(tags)
    pos_encoder.fit(pos)
    sentences=get_sentences(data)
    for sentence in sentences:
        for i in range(len(sentence)):
            w, p, t = sentence[i][0], sentence[i][1], sentence[i][2]
            
            if i < len(sentence)-1:
                # 如果不是最后一个单词，则可以用到下文的信息
                mem_tag_r = tag_encoder.transform(mv_tagger.predict([sentence[i+1][0]]))[0]
                true_pos_r = pos_encoder.transform([sentence[i+1][1]])[0]
            else:
                mem_tag_r = tag_encoder.transform(['O'])[0]
                true_pos_r =  pos_encoder.transform(['.'])[0]
                
            if i > 0: 
                # 如果不是第一个单词，则可以用到上文的信息
                mem_tag_l = tag_encoder.transform(mv_tagger.predict([sentence[i-1][0]]))[0]
                true_pos_l = pos_encoder.transform([sentence[i-1][1]])[0]
            else:
                mem_tag_l = tag_encoder.transform(['O'])[0]
                true_pos_l =  pos_encoder.transform(['.'])[0]
            #print (mem_tag_r, true_pos_r, mem_tag_l, true_pos_l)
            
            out.append(np.array([w.istitle(), w.islower(), w.isupper(), len(w), w.isdigit(), w.isalpha(),
                                    tag_encoder.transform(mv_tagger.predict([sentence[i][0]])),
                                    pos_encoder.transform([p])[0], mem_tag_r, true_pos_r, mem_tag_l, true_pos_l]))
            y.append(t)
    print('sentence features done.')
    return out,y

def random_forest1(words,tags):
    """
    利用单词本身的特征用随机森林进行命名实体识别
    结果precision 是0.88 还不如一开始的baseline majority voting 0.94
    """
    word_features=[word_feature_engineer(word) for word in words]
    pred=cross_val_predict(RandomForestClassifier(n_estimators=20),X=word_features,y=tags,cv=5)
    report=classification_report(y_pred=pred,y_true=tags)
    print(report)

def random_forest2(data):
    """
    利用单词的词性的更多的特征添加模型之中
    precision 0.97
    """
    print('random_forest2 starting...')
    out,y = new_features(data)
    pred = cross_val_predict(RandomForestClassifier(n_estimators=20), X=out, y=y, cv=5)
    report = classification_report(y_pred=pred, y_true=y)
    print(report)

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

# def main():


if __name__ == "__main__":
    root= Path.cwd()
    path = root / r'KnowledgeGraph\NLP\data\NER\ner_dataset.csv'
    data= analyse_data(path)
    words=data['Word'].values.tolist()
    tags=data['Tag'].values.tolist()
    # random_forest1(words,tags)
    random_forest2(data)
