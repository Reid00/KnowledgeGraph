
class MaxMatchSeg():
    def __init__(self):
        self.segment_dict = {"伟大", "中国", "勤劳","中国人民", "北京", "人民政府"}     #分词词典，一般比较大
        self.hot_dict = {"伟大", "中国", "中国人民", "北京", "人民政府"}        #热词词表
        self.max_word_length = 4        #词语的最大长度，可调

    def max_match(self,text):
        """
        正向匹配算法分词
        """
        index=0     #存储当前索引
        words=[]    #存储分词结果
        while index < len(text):
            #每一轮匹配，就是在一个窗口内，遍历所有前缀子字符串
            #首先计算窗口最右端的索引。快到文本末尾时，需要截断。
            window_end_index= min(len(text),index + self.max_word_length)
            #传进来的是指针，如果在text末尾添加3个符号，会改变text;深拷贝一个的话，还需要操作内存，消耗也挺大。
            word = None         #用于存储本轮匹配到的词语
            for i in range(window_end_index,index,-1):
                sub_string=text[index:i]
                if sub_string in self.segment_dict:
                    word=sub_string
                    break #如果匹配到合适的词语，更短的就不需要考虑了
            if word==None: #如果没有匹配到词语，index对应的字单独成词，索引加一
                words.append(text[index])
                index +=1
            else:
                words.append(word)
                index +=len(word)
        return words

if __name__ == "__main__":
    seg=MaxMatchSeg()
    text= "伟大的中国人民是勤劳的"
    print(seg.max_match(text)) #打印分词结果
