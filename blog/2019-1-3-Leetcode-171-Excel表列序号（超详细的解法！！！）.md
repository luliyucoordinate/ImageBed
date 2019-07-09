---
layout: post
title: Leetcode 171：Excel表列序号（超详细的解法！！！）
category : 算法
tags : [python, c, c++]
stickie: true
date: 2019-1-3 00:00:00
---

给定一个Excel表格中的列名称，返回其相应的列序号。

例如，

```
    A -> 1
    B -> 2
    C -> 3
    ...
    Z -> 26
    AA -> 27
    AB -> 28 
    ...
```

**示例 1:**

```
输入: "A"
输出: 1
```

**示例 2:**

```
输入: "AB"
输出: 28
```

**示例 3:**

```
输入: "ZY"
输出: 701
```

**解题思路**

这是之前问题[Leetcode 168：Excel表列名称（超详细的解法！！！）](https://blog.csdn.net/qq_17550379/article/details/85696288)的逆变换。很简单

```python
class Solution:
    def titleToNumber(self, s):
        """
        :type s: str
        :rtype: int
        """
        n, res = len(s), 0
        for c in s:
            n -= 1
            res += (ord(c) - 64) * (26**n)
            
        return res
```

一个更`pythonic`的解法

```python
from functools import reduce
class Solution:
    def titleToNumber(self, s):
        """
        :type s: str
        :rtype: int
        """
        return reduce(lambda x, y : x * 26 + y, [ord(c) - 64 for c in s])
```

reference:

https://leetcode.com/problems/excel-sheet-column-number/discuss/52107/My-solutions-in-3-languages-does-any-one-have-one-line-solution-in-Java-or-C%2B%2B

**我将该问题的其他语言版本添加到了我的[GitHub Leetcode](https://github.com/luliyucoordinate/Leetcode)**

**如有问题，希望大家指出！！！**