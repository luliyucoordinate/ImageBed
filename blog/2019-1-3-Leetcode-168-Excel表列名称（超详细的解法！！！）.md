---
layout: post
title: Leetcode 168：Excel表列名称（超详细的解法！！！）
category : 算法
tags : [python, c, c++]
stickie: true
date: 2019-1-3 00:00:00
---

给定一个正整数，返回它在 Excel 表中相对应的列名称。

例如，

```
    1 -> A
    2 -> B
    3 -> C
    ...
    26 -> Z
    27 -> AA
    28 -> AB 
    ...
```

**示例 1:**

```
输入: 1
输出: "A"
```

**示例 2:**

```
输入: 28
输出: "AB"
```

**示例 3:**

```
输入: 701
输出: "ZY"
```

**解题思路**

这个问题很简单，没什么难点，就是将**余数**不断添加到字符串的最前面。

```python
class Solution:
    def convertToTitle(self, n):
        """
        :type n: int
        :rtype: str
        """
        res = ''
        while n:
            n -= 1
            res += chr(ord('A') + n%26)
            n //= 26
            
        return res[::-1]
```

实现的实收采用了一个`trick`，就是`n -= 1`，如果不这样写的话，会写大量的判断语句。

一个精彩的解法

```python
class Solution:
    def convertToTitle(self, n):
        """
        :type n: int
        :rtype: str
        """
		return "" if num == 0 else self.convertToTitle((num - 1) / 26) + chr((num - 1) % 26 + ord('A'))
```

reference:

https://leetcode.com/problems/excel-sheet-column-title/discuss/51398/My-1-lines-code-in-Java-C%2B%2B-and-Python

**我将该问题的其他语言版本添加到了我的[GitHub Leetcode](https://github.com/luliyucoordinate/Leetcode)**

**如有问题，希望大家指出！！！**