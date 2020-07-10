# -*- encoding: utf-8 -*-
'''
@File        :letcode05.py
@Time        :2020/07/10 16:38:10
@Author      :Reid
@Version     :1.0
@Desc        :请实现一个函数，把字符串 s 中的每个空格替换成"%20"。

'''

# 示例:
# 输入：s = "We are happy."
# 输出："We%20are%20happy."

# 限制：
# 0 <= s 的长度 <= 10000


def resolution():
    """
    内置replace 方法
    """
    s = 'we are happy'
    return s.replace(' ', '%20')


def manual_replace():
    """
    手写实现replace 方法
    """
    s = 'we are happy'
    res = list()
    for char in s:
        if char != ' ':
            res.append(char)
        else:
            char = '%20'
            res.append(char)
    return ''.join(res)


if __name__ == "__main__":
    res = manual_replace()
    print(res)
