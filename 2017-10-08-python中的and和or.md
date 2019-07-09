---
layout: post
title: python中的and和or
category : python
tags : [python]
---

在python中and和or返回的值并不是True和false这么简单。虽然他们看上去和c++中的&&和||有些相似。在了解and和or之前，我们先要了解python中的True和False。

在python里面，0、''、[]、()、{}、None为假，其它任何东西都为真。ok，在此前提下。看这样一个例子：

```python
>>> 'a' and 'b'  
'b'  
>>> '' and 'b'  
''  
>>> 'a' and 'b' and 'c'  
'c' 
```

我们大致可以总结出这样的一个规律，对于and，如果没有假值，返回的是最后一个真值，如果有假值，则返回的是第一个假值。

```python
>>> 'a' or 'b'  
'a'  
>>> '' or 'b'  
'b'  
>>> '' or [] or{}  
{}  
```

对于or，如果没有真值，返回的是最后一个假值，如果有真值，则返回的是第一个真值。

知道了这些我们就可以模拟出c语言中的三目运算符操作`a ? b : c`

```python
>>> a = "haha"
>>> b = "hehe" 
>>> 1 and a or b 
'haha'
>>> 0 and a or b 
'hehe'
```

但是这样做会出现一个问题，如下

```python
>>> a = ""
>>> b = "hehe" 
>>> 1 and a or b 
'hehe'
```

解决办法如下

```python
(1 and [a] or [b])[0]
```

解决思路就是，对于`['']`，我们知道它为真，即上面的式子中括号里面的值是`['']`，`[''][0]` 的结果就是`''` 。