"""
词性标注的实现
"""
import numpy as np
import pandas as pd
from collections import defaultdict
from pathlib import Path

def generate_dict(path):
    """
    生成单词和标签的词典库
    word2id,id2word  --> word2id={'Newsweek':0,'trying':1...} id2word={0:'Newsweek',1:'trying'...}
    tag2id,id2tag  --> tag2id={'VB':0,'NNP':1...}
    """
    word2id,id2word={},{}
    tag2id,id2tag={},{}
    print('starting generate dict for word and tag')
    with open(path,encoding='utf8') as f:
        lines=f.readlines()
        for line in lines:
            items=line.split('/')
            word,tag=items[0],items[1].rstrip()
            
            if word not in word2id:
                word2id[word] = len(word2id)
                id2word[len(id2word)]=word
            if tag not in tag2id:
                tag2id[tag]= len(tag2id)
                id2tag[len(id2tag)] = tag
    print(list(word2id.items())[:5],list(id2word.items())[:5])
    print(list(tag2id.items())[:5],list(id2tag.items())[:5])
    print('dictionary generated.')
    return word2id,id2word,tag2id,id2tag

def generate_model_args(path,*args):
    """
    构建模型所需要的参数: z=argmax logP(w|z) + logP(z) + P(z_i|z_i-1) 的和。z 代表词性，w 代表每个单词
    logP(w|z) 每个词性下面每个单词的概率 用A表示 (N*M 的矩阵，M是单词的长度, N是词性的长度)
    logP(z) 每个词性出现为句子开头的概率 用pi 表示 (N维的数组)
    P(z_i|z_i-1) 前一个是z_i-1 的词性，下面是z_i 的概率，词性转移的概率  用B表示 N*N 的矩阵
    """
    print('开始生成模型所需要的表达式参数')
    word2id,id2word,tag2id,id2tag=args
    M = len(word2id)
    N=len(tag2id)
    pi = np.zeros(N)
    A = np.zeros((N,M))
    B= np.zeros((N,N))
    prev_tag=''
    with open(path,encoding='utf8')as f:
        lines = f.readlines()
        for line in lines:
            items= line.split('/')
            wordId,tagId= word2id[items[0]],tag2id[items[1].rstrip()]
            if prev_tag=='': # 这意味着是句子的开始
                pi[tagId] +=1
                A[tagId][wordId] +=1
            else: # 如果不是句子的开头
                A[tagId][wordId] +=1
                B[tag2id[prev_tag]][tagId] +=1

            if items[0]=='.':
                prev_tag=''
            else:
                prev_tag=items[1].rstrip()

    # normalize 之前统计的只是个数，标准化为概率
    pi= pi/sum(pi)
    for i in range(N):
        A[i] /=sum(A[i])
        B[i] /=sum(B[i])
    #  到此为止计算完了模型的所有的参数： pi, A, B
    print(pi,A,B)
    print('arguments generate done.')
    return pi,A,B

def log(v):
    """
    定义log方法，计算log 值
    """
    if v == 0:
        return np.log(v+0.000001)
    return np.log(v)

def viterbi(x, pi, A, B,word2id,id2word,tag2id,id2tag):
    """
    x: user input string/sentence: x: "I like playing soccer"
    pi: initial probability of tags
    A: 给定tag, 每个单词出现的概率
    B: tag之间的转移概率
    """
    x = [word2id[word] for word in x.split(" ")]  # x: [4521, 412, 542 ..]
    T = len(x)
    N=len(tag2id)
    
    dp = np.zeros((T,N))  # dp[i][j]: w1...wi, 假设wi的tag是第j个tag
    ptr = np.array([[0 for x in range(N)] for y in range(T)] ) # T*N
    # TODO: ptr = np.zeros((T,N), dtype=int)
    
    for j in range(N): # basecase for DP算法
        dp[0][j] = log(pi[j]) + log(A[j][x[0]])
    
    for i in range(1,T): # 每个单词
        for j in range(N):  # 每个词性
            # TODO: 以下几行代码可以写成一行（vectorize的操作， 会使得效率变高）
            dp[i][j] = -9999999
            for k in range(N): # 从每一个k可以到达j
                score = dp[i-1][k] + log(B[k][j]) + log(A[j][x[i]])
                if score > dp[i][j]:
                    dp[i][j] = score
                    ptr[i][j] = k
    
    # decoding: 把最好的tag sequence 打印出来
    best_seq = [0]*T  # best_seq = [1,5,2,23,4,...]  
    # step1: 找出对应于最后一个单词的词性
    best_seq[T-1] = np.argmax(dp[T-1])
    
    # step2: 通过从后到前的循环来依次求出每个单词的词性
    for i in range(T-2, -1, -1): # T-2, T-1,... 1, 0
        best_seq[i] = ptr[i+1][best_seq[i+1]]
        
    # 到目前为止, best_seq存放了对应于x的 词性序列
    for i in range(len(best_seq)):
        print (id2tag[best_seq[i]])  

if __name__ == "__main__":
    root=Path.cwd()
    path=root / r'KnowledgeGraph\NLP\data\pos_tagging\traindata.txt'
    data=generate_dict(path)
    pi,A,B=generate_model_args(path,*data)
    x = "Social Security number , passport number and details about the services provided for the payment"
    viterbi(x,pi,A,B,*data)  