class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        """
        有效的字母异位词
        判断两个字符串是否可以通过字母顺序变换得到一样的结果
        Input: s = "anagram", t = "nagaram"
        Output: true
        Input: s = "rat", t = "car"
        Output: false
        """
        # method 1:
        # return sorted(s)==sorted(t)

        # method 2 用哈希表的方式，牺牲空间复杂度，降低时间复杂度
        if len(s) != len(t):
            return False
        s_dic,t_dic={},{}
        for c in s:
            if c in s_dic:
                s_dic[c] +=1
            else:
                s_dic[c] = 1
        print(s_dic)
        for c in t:
            if c in t_dic:
                t_dic[c] +=1
            else:
                t_dic[c] = 1
        print(t_dic)
        if s_dic==t_dic:
            return True
        else:
            return False


if __name__ == "__main__":
    s = Solution()
    print(s.isAnagram('anagram','nagaram'))
    print(s.isAnagram('rat','car'))

        