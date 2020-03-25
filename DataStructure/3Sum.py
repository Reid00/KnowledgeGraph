from typing import List
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """
        给定三个数，返回指定和为指定数值的组合. 此处target 为0

        Given array nums = [-1, 0, 1, 2, -1, -4],
        A solution set is:
        [
        [-1, 0, 1],
        [-1, -1, 2]
        ]
        """

        #方法一 暴力求解，遍历三遍
        if len(nums) <3:
            return []
        nums= sorted(nums)
        res=set()
        for i in range(len(nums)):
            for j in range(i+1,len(nums)):
                for z in range(j+1,len(nums)):
                    if nums[i] + nums[j] + nums[z] == 0:
                        res.add((nums[i],nums[j],nums[z]))
        return list(res)
    def threeSum2(self, nums: List[int]) -> List[List[int]]:        
        #方法二用hashtable
        if len(nums)<3:
            return []
        nums=sorted(nums)
        res=set()
        dic=dict()
        for i, v in enumerate(nums):
            dic[v] =1
        print(dic)
        for i in range(len(nums)):
            for j in range(i+1,len(nums)):
                if 0-nums[i]-nums[j] in dic:
                    print(0-nums[i]-nums[j] )
                    print(nums[i],nums[j])
                    print('----')
                    res.add(tuple(sorted((nums[i],nums[j],0-nums[i]-nums[j]))))
        return list(res)
      
if __name__ == "__main__":
    s=Solution()
    print(s.threeSum( [-1, 0, 1, 2, -1, -4]))
    print(s.threeSum2( [-1, 0, 1, 2, -1, -4]))

