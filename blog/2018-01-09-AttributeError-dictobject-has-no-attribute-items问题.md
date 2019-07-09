---
layout: post
title: AttributeError 'dict' object has no attribute 'items' 问题
category : python
tags :  [python, dict]
stickie: true
---

其实这是一个很小的问题，但是我看到网上很多答案不怎么喜欢，所以写一下。

我们通常这样做的时候

```python
dict_obj.has_key(key1)
```

这样做在python3中会报错。因为python3中去除了`has_key`这个方法。

看到网上很多人这样去做

```python
if key1 in dict_obj:
```

这样做肯定是没有问题的。

但是难道python3下面就没有一个和`has_key`功能一样的函数吗？有！！！

```python
dict_obj.__contains__(key1)
```

这才是最符合python3的做法。
