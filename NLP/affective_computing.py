import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from pathlib import Path

def data_analyse(path):
    data=pd.read_csv(path,encoding='utf8',header=None)
    print(data.head())
    # print(data.describe())
    # print(data.info())
    print(data.isnull().sum())
    print('data analyse done')
    return data

def feature_engineer(data):
    """
    用onehot TF-IDF表示词 的向量
    """
    X=data[1].values
    y=data[0].values
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

    vectorizer=TfidfVectorizer()
    X_train = vectorizer.fit_transform(X_train)
    X_test= vectorizer.transform(X_test)
    print('feature engineer done')
    return X_train,X_test,y_train,y_test

def model_training(*args):
    """
    LogisticRegression 中超参数C, 用来控制L2/L1 正则的的倒数，C 越小表示正则的影响越大
    GridSearchCV 用来寻找最优解的超参数C
    """
    X_train,X_test,y_train,y_test=args[0],args[1],args[2],args[3]
    print('model training began')
    parameters={'C':[0.000001,0.00001,0.0001,0.01,0.1,0.5,1,2,5,10]}
    lr= LogisticRegression(multi_class='auto')
    # lr= LogisticRegression(C=2)
    lr.fit(X_train,y_train)
    # 预测测试集
    y_pred=lr.predict(X_test)

    # 生成混淆矩阵，以及准确率、召回率分析结果
    cm = confusion_matrix(y_test,y_pred)
    cr= classification_report(y_test,y_pred)
    print(cm,'\n',cr)

    # 通过交叉验证, 指定最优解; cv 交叉验证参数,指定把数据分为几份，其中一份作为交叉验证集合，其余作为training集合，默认为3
    # scoring :准确度评价标准，默认None,这时需要使用score函数；或者如scoring='roc_auc'，根据所选模型不同，评价准则不同。字符串（函数名），或是可调用对象，需要其函数签名形如：scorer(estimator, X, y)；如果是None，则使用estimator的误差估计函数。
    # gsearch1=GridSearchCV(estimator=lr,param_grid=parameters,scoring='roc_auc',cv=10)
    #roc_auc 不支持分类数据
    gsearch1=GridSearchCV(estimator=lr,param_grid=parameters,cv=10)
    gsearch1.fit(X_train,y_train)
    gsearch1.score(X_test,y_test)
    print(gsearch1.cv_results_)
    print(gsearch1.best_params_)  #最好的参数
    print(gsearch1.best_estimator_) #最好的模型
    print(gsearch1.best_score_)
    # 上面打印出 交叉验证最好的C 为2

    #混淆矩阵，对角线数值越高代表效果越来，同一行代表一种类别
    cm=confusion_matrix(y_test,gsearch1.predict(X_test))
    print(cm)
    """
    result as below:
    [[ 98  33  19  26  14  20  17]
    [ 25 124  13  16   9   3  14]
    [ 14   7 141   9  13  11   5]
    [ 23  12  12 107  13  16  26]
    [  6   7  10   8 182  11   9]
    [ 17  18  15   8  18 122   7]
    [ 22  27  17  35  22   6  97]]
    """

if __name__ == "__main__":
    root = Path.cwd()
    path=root / r'KnowledgeGraph\NLP\data\EmotionData\ISEAR.csv'
    data=data_analyse(path)
    vector=feature_engineer(data)
    model_training(*vector)