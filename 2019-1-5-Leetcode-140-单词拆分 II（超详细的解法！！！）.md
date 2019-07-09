---
layout: post
title: Leetcode 140：单词拆分 II（超详细的解法！！！）
category : 算法
tags : [python, c, c++]
stickie: true
date: 2019-1-5 00:00:00
---

给定一个**非空**字符串 *s* 和一个包含**非空**单词列表的字典 *wordDict*，在字符串中增加空格来构建一个句子，使得句子中所有的单词都在词典中。返回所有这些可能的句子。

**说明：**

- 分隔时可以重复使用字典中的单词。
- 你可以假设字典中没有重复的单词。

**示例 1：**

```
输入:
s = "catsanddog"
wordDict = ["cat", "cats", "and", "sand", "dog"]
输出:
[
  "cats and dog",
  "cat sand dog"
]
```

**示例 2：**

```
输入:
s = "pineapplepenapple"
wordDict = ["apple", "pen", "applepen", "pine", "pineapple"]
输出:
[
  "pine apple pen apple",
  "pineapple pen apple",
  "pine applepen apple"
]
解释: 注意你可以重复使用字典中的单词。
```

**示例 3：**

```
输入:
s = "catsandog"
wordDict = ["cats", "dog", "sand", "and", "cat"]
输出:
[]
```

**解题思路**

这是之前问题[Leetcode 139：单词拆分（最详细的解法！！！）](https://blog.csdn.net/qq_17550379/article/details/82933187)的提高。

首先想到的解法就是回溯法。通过遍历`s`，然后判断`s[:i]`是不是单词，如果是的话，我们继续找下一个，直到遍历结束。然后我们再继续判断`s[:i+1]...s[:i+n]`是不是单词，也就是找第二个解。

```python
class Solution(object):
    def wordBreak(self, s, wordDict):
        """
        :type s: str
        :type wordDict: List[str]
        :rtype: List[str]
        """
        wordDict = set(wordDict)
        res = list()
        self.dfs(s, wordDict, "", res)
        return res
        
    def _wordBreak(self, s, wordDict, st, res):
        if not s:
            res.append(st.rstrip())
            return
        
        for i in range(len(s)+1):
            if s[:i] in wordDict:
                self._wordBreak(s[i:], wordDict, st+str(s[:i])+' ', res)
```

但是这样解会超时，所以我们想到了通过添加记忆变量的方法。但是上面这种写法我发现无法写出对应的记忆化搜索形式，关键问题在于我们在得到`mem[s]`的时候，我们返回什么？（我们上面定义的函数`_wordBreak`返回的是`None`），所以我们需要重新定义一个函数。

这也非常简单，我们定义函数$f(i)$返回`s[i:]`的结果。然后我们只需要判断`s[:i]`是不是在`wordDict`中，如果在的话，我们遍历$f(i)$中的每个元素`it`，然后将`s[:i]`添加到`it`前，然后在添加到结果中去。接着就是边界问题，当我们发现`s==""`，我们此时只需将`""`添加到结果中去，然后返回即可。

```python
class Solution(object):
    def wordBreak(self, s, wordDict):
        """
        :type s: str
        :type wordDict: List[str]
        :rtype: List[str]
        """
        wordDict = set(wordDict)
        mem = dict()
        return self._wordBreak(s, wordDict, mem)
        
    def _wordBreak(self, s, wordDict, mem):
        if s in mem:
            return mem[s]
        
        res = list()
        if not s:
            res.append("")
            return res
        
        for i in range(len(s)+1):
            if s[:i] in wordDict:
                sublist = self._wordBreak(s[i:], wordDict, mem)
                for it in sublist:
                    res.append(str(s[:i]) + ('' if not it else ' ') + it)
                
        mem[s] = res
        return res
```

一个`pythonic`的实现

```python
class Solution:
    def wordBreak(self, s, wordDict):
        """
        :type s: str
        :type wordDict: List[str]
        :rtype: List[str]
        """
        memo = {len(s): ['']}
        def sentences(i):
            if i not in memo:
                memo[i] = [s[i:j] + (tail and ' ' + tail)
                           for j in range(i+1, len(s)+1)
                           if s[i:j] in wordDict
                           for tail in sentences(j)]
            return memo[i]
        return sentences(0)
```

reference:

https://leetcode.com/problems/word-break-ii/discuss/44169/9-lines-Python-10-lines-C%2B%2B

**我将该问题的其他语言版本添加到了我的[GitHub Leetcode](https://github.com/luliyucoordinate/Leetcode)**

**如有问题，希望大家指出！！！**