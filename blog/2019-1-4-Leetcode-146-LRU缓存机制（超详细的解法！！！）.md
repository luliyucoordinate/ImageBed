---
layout: post
title: Leetcode 146：LRU缓存机制（超详细的解法！！！）
category : 算法
tags : [python, c, c++]
stickie: true
date: 2019-1-4 00:00:00
---

运用你所掌握的数据结构，设计和实现一个  [LRU (最近最少使用) 缓存机制](https://baike.baidu.com/item/LRU)。它应该支持以下操作： 获取数据 `get` 和 写入数据 `put` 。

获取数据 `get(key)` - 如果密钥 (key) 存在于缓存中，则获取密钥的值（总是正数），否则返回 -1。
写入数据 `put(key, value)` - 如果密钥不存在，则写入其数据值。当缓存容量达到上限时，它应该在写入新数据之前删除最近最少使用的数据值，从而为新的数据值留出空间。

**进阶:**

你是否可以在 **O(1)** 时间复杂度内完成这两种操作？

**示例:**

```
LRUCache cache = new LRUCache( 2 /* 缓存容量 */ );

cache.put(1, 1);
cache.put(2, 2);
cache.get(1);       // 返回  1
cache.put(3, 3);    // 该操作会使得密钥 2 作废
cache.get(2);       // 返回 -1 (未找到)
cache.put(4, 4);    // 该操作会使得密钥 1 作废
cache.get(1);       // 返回 -1 (未找到)
cache.get(3);       // 返回  3
cache.get(4);       // 返回  4
```

**解题思路**

这个问题非常简单，只要按照题目意思做就可以了。

```python
class LRUCache:
    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.capacity = capacity
        self.stack = list()
        self.cache = dict()

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        if key in self.cache:
            self.stack.remove(key)
            self.stack.append(key)
            return self.cache[key]
            
        return -1

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: void
        """
        if key in self.cache:
            self.stack.remove(key)  
        else:
            if len(self.cache) == self.capacity:
                del self.cache[self.stack[0]]
                self.stack.pop(0)
                
        self.stack.append(key)
        self.cache[key] = value
```

如果使用`python`语言的话，一个比较好的实现手段就是通过`OrderedDict`。

```python
class LRUCache:
    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.capacity = capacity
        self.cache = collections.OrderedDict()

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        if key in self.cache:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
            
        return -1

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: void
        """
        if key in self.cache:
            self.cache.pop(key)
        else:
            if len(self.cache) == self.capacity:
                self.cache.popitem(last=False)
                
        self.cache[key] = value
```

这个问题的`cpp`实现，我使用了`list`，主要其中的`splice`很适合这里的操作，大家可以参考的`github`代码。

reference:

https://leetcode.com/problems/lru-cache/discuss/45952/Python-concise-solution-with-comments-(Using-OrderedDict).

**我将该问题的其他语言版本添加到了我的[GitHub Leetcode](https://github.com/luliyucoordinate/Leetcode)**

**如有问题，希望大家指出！！！**