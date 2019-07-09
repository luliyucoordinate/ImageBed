---
layout: post
title: Leetcode 187:重复的DNA序列（超详细解决方案！！！）
category : 算法
tags : [python, c, c++]
stickie: true
date: 2019-1-11 00:00:00
---

所有 DNA 由一系列缩写为 A，C，G 和 T 的核苷酸组成，例如：“ACGAATTCCG”。在研究 DNA 时，识别 DNA 中的重复序列有时会对研究非常有帮助。

编写一个函数来查找 DNA 分子中所有出现超多一次的10个字母长的序列（子串）。

**示例:**

```
输入: s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"

输出: ["AAAAACCCCC", "CCCCCAAAAA"]
```

**解题思路**

这个问题一个简单粗暴的做法就是将所有`10`个字母长的序列存放到`set`中，然后我们遍历的过程中还要判断我们新遍历到的字符串是不是已经添加到`set`里面了，如果已经添加过了的话，我们知道此时已经重复了，所以我们将字符串添加到`res`中即可。

```python
class Solution:
    def findRepeatedDnaSequences(self, s):
        """
        :type s: str
        :rtype: List[str]
        """
        res, mem = set(), set()
        for i in range(len(s)-9):
            cur = s[i:i+10]
            if cur in mem:
                res.add(cur)
            else:
                mem.add(cur)
                
        return list(res)
```

或者直接通过`defaultdict`统计所有`10`个字母长的序列出现次数。

```python
class Solution:
    def findRepeatedDnaSequences(self, s):
        """
        :type s: str
        :rtype: List[str]
        """
        sequences = collections.defaultdict(int) 
        for i in range(len(s)-9):
            sequences[s[i:i+10]] += 1
        return [key for key, value in sequences.items() if value > 1]
```

**我将该问题的其他语言版本添加到了我的[GitHub Leetcode](https://github.com/luliyucoordinate/Leetcode)**

**如有问题，希望大家指出！！！**