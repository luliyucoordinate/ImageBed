---
layout: post
title: Leetcode 28：实现strStr()（超详细的解法！！！）
category : 算法
tags : [python, c, c++]
stickie: true
date: 2018-12-4 00:00:00
---

实现 [strStr()](https://baike.baidu.com/item/strstr/811469) 函数。

给定一个 haystack 字符串和一个 needle 字符串，在 haystack 字符串中找出 needle 字符串出现的第一个位置 (从0开始)。如果不存在，则返回  **-1**。

**示例 1:**

```
输入: haystack = "hello", needle = "ll"
输出: 2
```

**示例 2:**

```
输入: haystack = "aaaaa", needle = "bba"
输出: -1
```

**说明:**

当 `needle` 是空字符串时，我们应当返回什么值呢？这是一个在面试中很好的问题。

对于本题而言，当 `needle` 是空字符串时我们应当返回 0 。这与C语言的 [strstr()](https://baike.baidu.com/item/strstr/811469) 以及 Java的 [indexOf()](https://docs.oracle.com/javase/7/docs/api/java/lang/String.html#indexOf(java.lang.String)) 定义相符。

**解题思路**

这个问题最简单的思路就是逐个字符比较

```python
class Solution:
    def strStr(self, haystack, needle):
        """
        :type haystack: str
        :type needle: str
        :rtype: int
        """
        haystack_len, needle_len = len(haystack), len(needle)
        if haystack_len < needle_len:
            return -1
        
        for i in range(haystack_len - needle_len + 1):
            if haystack[i:i+needle_len] == needle:
                return i
        return -1
```

一个更取巧的做法

```python
class Solution:
    def strStr(self, haystack, needle):
        """
        :type haystack: str
        :type needle: str
        :rtype: int
        """
        try:
            return haystack.index(needle)
        except:
            return -1
```

关于字符串匹配的问题，当然更好的做法是`KMP`算法。

```python
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        if not needle:
            return 0
        m, n = len(haystack), len(needle)
        if m < n:
            return -1
        
        ne, i, j = [-1]*n, 0, -1
        while i < n-1:
            while j != -1 and needle[i] != needle[j]:
                j = ne[j]
            i += 1
            j += 1
            if needle[i] == needle[j]:
                ne[i] = ne[j]
            else:
                ne[i] = j
        
        i, j = 0, 0
        while i < m:
            while j != -1 and haystack[i] != needle[j]:
                j = ne[j]
            i += 1
            j += 1
            if j >= n:
                return i - n
        return -1
```

**我将该问题的其他语言版本添加到了我的[GitHub Leetcode](https://github.com/luliyucoordinate/Leetcode)**

**如有问题，希望大家指出！！！**