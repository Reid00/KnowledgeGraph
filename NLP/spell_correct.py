from pathlib import Path
from nltk.corpus import reuters
from collections import defaultdict
import numpy as np
#构建词库
def generate_vocab(path):
    vocab = set([line.strip() for line in open(vocab_path)])
    print(f'vocab is:\n {list(vocab)[:10]}')
    return vocab

# 生成所有候选集合(编辑距离为1 的单词)
def generate_candidates(word,vocab):
    """
    word: 给定的错误的输入
    返回所有的候选集合
    """
    #假设插入26 的字母
    letters='abcdefghijklmnopqrstuvwxyz'
    splits=[(word[:i],word[i:]) for i in range(len(word)+1)]

    inserts=[ L+letter+R for L,R in splits for letter in letters]
    deletes=[ L+ R[1:] for L,R in splits if R]
    replaces=[ L+letter + R[1:] for L,R in splits if R for letter in letters]

    # 过滤不存在词典库的单词
    candidates=[word for word in set(inserts + deletes + replaces) if word in vocab]
    return candidates


#构建语言模型 : bigram
def language_mode():
     # 读取语料库 from NLTK
    categories = reuters.categories()
    corpus=reuters.sents(categories=categories)
    print(f'top 3 corpus is:\n {corpus[:3]}')
    term_count={}
    bigram_count={}
    for doc in corpus:
        doc=['<s>'] + doc
        for i in range(0,len(doc)-1):
            #bigram :[i,i +1]
            term=doc[i]
            bigram=doc[i:i+2]
            if term in term_count:
                term_count[term] +=1
            else:
                term_count[term] =1
            bigram=' '.join(bigram)
            if bigram in bigram_count:
                bigram_count[bigram] +=1
            else:
                bigram_count[bigram]=1
    print(f'term_count length is: \n {len(term_count)}') # {'<s>': 54716, 'ASIAN': 12, 'EXPORTERS': 46, 'FEAR'
    print(f'bigram_count length is: \n {len(bigram_count)}')  #{'<s> ASIAN': 4, 'ASIAN EXPORTERS': 1, 'EXPORTERS FEAR': 1, 'FEAR DAMAGE': 1,
    return term_count,bigram_count


#用户打错的概率 --- Channel　probability
def wrong_probability(path):
    """
    计算每个错误单词的概率
    return :
    raining defaultdict(<class 'int'>, {'rainning': 0.5, 'raning': 0.5})
    """
    channel_prob=defaultdict(int)
    with open(path,'r',encoding='utf-8') as f:
        lines=f.readlines()
        for line in lines:
            items=line.split(':')
            correct=items[0].strip()
            mistakes= [mis.strip() for mis in items[1].strip().split(',')]
            channel_prob[correct] = defaultdict(int)
            for mis in mistakes:
                channel_prob[correct][mis] = 1.0 / len(mistakes)
    return channel_prob


# 用测试集验证哪些单词出现了错误
def validation_test(vocab,channel_prob,term_count,bigram_count):
    data_path=Path(r'D:\GitRepository\KnowledgeGraph\NLP\data\testdata.txt')
    with open(data_path,'r',encoding='utf-8') as f:
        lines= f. readlines()
        for line in lines:
            items=line.split('\t')[2]  # 句子
            words= items.split()
            for word in words:
                if word not in vocab:            
                # 如果单词不在词典中 1. 拼写出错 --> 生成所有的(valid)候选集合
                # 2. 该单词不在词典中 （默认所有的单词都是词典中）
                    probs=[]
                    candidates = generate_candidates(word,vocab)
                    if 0<len(candidates)<5:  # 如果候选集合少于五个，生成编辑距离不小于2 的集合
                        candidates_2=set([ele2 for word in candidates for ele2 in generate_candidates(word,vocab)])
                        probability=[]
                        # 对于每一个candidate, 计算它的score
                        # score = p(correct)*p(mistake|correct)
                        # = log p(correct) + log p(mistake|correct)
                        # 返回score最大的candidate
                        for candi in candidates_2:
                            prob=0
                            if channel_prob[candi]!=0 and channel_prob[candi][word]!=0:
                                prob += np.log(channel_prob[candi][word])
                            else: #如果单词不在用户打错的集合里面，就给一个很小的数值
                                prob += np.log(0.001)
                            #  b. 计算语言模型的概率
                            idx= items.index(word) +1
                            if items[idx-1] in bigram_count and candi in bigram_count[items[idx-1]]:
                                 prob += np.log((bigram_count[items[idx - 1]][candi] + 1.0) / (
                            term_count[bigram_count[items[idx - 1]]] + len(vocab)))
                            else:
                                prob += np.log(0.001)
                        probs.append(prob)
                        max_idx = probs.index(max(probs))
                        print (word, candidates_2[max_idx])
                    elif len(candidates)>=5:
                        probability=[]
                        # 对于每一个candidate, 计算它的score
                        # score = p(correct)*p(mistake|correct)
                        # = log p(correct) + log p(mistake|correct)
                        # 返回score最大的candidate
                        for candi in candidates:
                            prob=0
                            if channel_prob[candi]!=0 and channel_prob[candi][word]!=0:
                                prob += np.log(channel_prob[candi][word])
                            else: #如果单词不在用户打错的集合里面，就给一个很小的数值
                                prob += np.log(0.001)
                            #  b. 计算语言模型的概率
                            idx= items.index(word) +1
                            if items[idx-1] in bigram_count and candi in bigram_count[items[idx-1]]:
                                 prob += np.log((bigram_count[items[idx - 1]][candi] + 1.0) / (
                            term_count[bigram_count[items[idx - 1]]] + len(vocab)))
                            else:
                                prob += np.log(0.001)
                        probs.append(prob)
                        max_idx = probs.index(max(probs))
                        print (word, candidates[max_idx])
                    else:
                        print(f'{word} not found the candidates')

if __name__ == "__main__":
    vocab_path=Path(r'D:\GitRepository\KnowledgeGraph\NLP\data\vocab.txt')
    vocab=generate_vocab(vocab_path)
    candidates=generate_candidates('apple',vocab)
    print(candidates)
    term_count,bigram_count = language_mode()
    spell_errors_path=Path(r'D:\GitRepository\KnowledgeGraph\NLP\data\spell-errors.txt')
    channel_prob=wrong_probability(spell_errors_path)
    validation_test(vocab,channel_prob,term_count,bigram_count)