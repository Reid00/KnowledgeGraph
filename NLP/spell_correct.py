from pathlib import Path
from nltk.corpus import reuters
from collections import defaultdict
#构建词库
def generate_vocab(path):
    vocab = set([line.strip() for line in open(vocab_path)])
    print(f'vocab is:\n {vocab}')
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
    print(f'corpus is:\n {corpus}')
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
    print(term_count)
    print(bigram_count)
    return term_count,bigram_count


#用户打错的概率 --- Channel　probability
def wrong_probability(path):
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


if __name__ == "__main__":
    # vocab_path=Path(r'D:\GitRepository\KnowledgeGraph\NLP\data\vocab.txt')
    # vocab=generate_vocab(vocab_path)
    # candidates=generate_candidates('apple',vocab)
    # print(candidates)
    spell_errors_path=Path(r'D:\GitRepository\KnowledgeGraph\NLP\data\spell-errors.txt')
    channel_prob=wrong_probability(spell_errors_path)
    for k,v in channel_prob.items():
        print(k,v)
        break;

