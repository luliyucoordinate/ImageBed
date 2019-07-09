---
layout: post
title: Leetcode 208:实现 Trie (前缀树)（超详细解决方案！！！）
category : 算法
tags : [python, c, c++]
stickie: true
date: 2019-1-11 00:00:00
---

实现一个 Trie (前缀树)，包含 `insert`, `search`, 和 `startsWith` 这三个操作。

**示例:**

```
Trie trie = new Trie();

trie.insert("apple");
trie.search("apple");   // 返回 true
trie.search("app");     // 返回 false
trie.startsWith("app"); // 返回 true
trie.insert("app");   
trie.search("app");     // 返回 true
```

**说明:**

- 你可以假设所有的输入都是由小写字母 `a-z` 构成的。
- 保证所有输入均为非空字符串。

**解题思路**

很基础的问题，考察基础概念。

```python
class Node:
    def __init__(self, isWord=False):
        self.isWord = isWord
        self.next = dict()
        
class Trie:
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = Node()

    def insert(self, word):
        """
        Inserts a word into the trie.
        :type word: str
        :rtype: void
        """
        cur = self.root
        for c in word:
            if c not in cur.next:
                cur.next[c] = Node()
            cur = cur.next[c]
            
        if not cur.isWord:
            cur.isWord = True
        
    def search(self, word):
        """
        Returns if the word is in the trie.
        :type word: str
        :rtype: bool
        """
        cur = self._search(word)
        return cur != None and cur.isWord
        
    def _search(self, word):
        cur = self.root
        for c in word:
            if c not in cur.next:
                return None
            cur = cur.next[c]
            
        return cur
        
    def startsWith(self, prefix):
        """
        Returns if there is any word in the trie that starts with the given prefix.
        :type prefix: str
        :rtype: bool
        """
        return self._search(prefix) != None 
```

在使用`cpp`实现的时候不要漏掉**析构函数**。

**我将该问题的其他语言版本添加到了我的[GitHub Leetcode](https://github.com/luliyucoordinate/Leetcode)**

**如有问题，希望大家指出！！！**