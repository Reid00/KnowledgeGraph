import numpy as np

def markov():
    """
    马尔科夫假设的收敛验证
    下一个词的出现仅依赖于它前面的一个或几个词
    """
    init_array=np.array([0.3,0.2,0.4,0.1])  # 初始对应，A，B，C，D 被访问的概率
    # ABCD 这四个页面转移的概率
    transfer_matrix= np.array([
        [0,0.5,0.3,0],
        [0.5,0.1,0.6,0],
        [0.3,0.3,0,0.9],
        [0.2,0.1,0.1,0.1],
    ])
    res_tep= init_array
    for i in range(50):
        res=np.dot(res_tep,transfer_matrix)
        print(i,'===',res)
        res_tep=res

if __name__ == "__main__":
    markov()