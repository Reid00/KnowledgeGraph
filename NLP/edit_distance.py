import numpy as np
def edit_dis(str1,str2):
    """
    基于动态规划求解编辑距离
    str1 -> str2
    """
    # m,n 分别是字符串的长度
    m,n=len(str1),len(str2)
    #构建一个二维数组来存储子问题
    # dp=[[0 for x in range(n+1)] for j in range(m+1)]
    dp=np.zeros((m+1,n+1))

    # 利用动态规划算法，填充数组
    for i in range(m+1):
        for j in range(n+1):
            # 如果第一个字符串为空, 则转换的代价为j
            if i==0:
                dp[i][j]=j
            # 如果第二个字符串为空, 则转换的代价为j
            elif j==0:
                dp[i][j]=i
            # 如果最后一个字符相等，就不会产生代价
            elif str1[i-1]==str2[j-1]:
                dp[i][j]=dp[i-1][j-1]
            # 如果最后一个字符不相同，则需要考虑多个情况，计算最小的值
            else:
                dp[i][j]= 1 + min(dp[i][j-1],  # insert
                dp[i-1][j],     # remove
                dp[i-1][j-1]       # replace
                )

            
    return dp[m][n]

def generate_edit_one(str):
    """
    生成编辑距离为1 的字符串
    str: 指定字符串,eg: apple
    """
    # insert，delete，replace
    # 操作需要的字符串
    letters='abcdefghijkmnopqrstuvwxyz'

    #把原有的字符串拆分各种可能性
    splits= [ (str[:i],str[i:]) for i in range(len(str)+1)]
    # 通过插入的方法生成字符串
    inserts= [L + letter + R for L,R in splits for letter in letters]
    # 通过删除的方式生成字符串
    deletes=[ L + R[1:] for L,R in splits if R]
    # 通过替换的方式生成字符串
    replaces=[ L + letter + R[1:] for L,R in splits if R for letter in letters]
    return set(inserts + deletes + replaces)

def generate_edit_two(str):
    """
    生成编辑距离不大于2的字符串
    """
    eles= [e2 for e1 in generate_edit_one(str) for e2 in generate_edit_one(e1)]
    return eles

if __name__ == "__main__":
    res=edit_dis('he0000lo','hello')
    print(res)
    res=generate_edit_one('apple')
    # print(res)
    res=generate_edit_two('apple')
    print(len(res))