---
layout: post
title: python 子类中扩展 property
category : python
tags : [python, property]
stickie: true
date: 2018-03-18 00:00:00
---

这是`python cookbook 8.8`节中的一个问题

```python
class Person:
    def __init__(self, name):
        self.name = name
    # Getter function
    @property
    def name(self):
        return self._name
    # Setter function
    @name.setter
    def name(self, value):       
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._name = value
    # Deleter function
    @name.deleter
    def name(self):
        raise AttributeError("Can't delete attribute")
        
class SubPerson(Person):
    @property
    def name(self):
        print('Getting name')
        return super().name
    @name.setter
    def name(self, value):
        print('Setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)
    @name.deleter
    def name(self):
        print('Deleting name')
        super(SubPerson, SubPerson).name.__delete__(self)
        
s = SubPerson('Guido')
print(s.name)
s.name = 'fa'
print(s.name)
```

输出结果是

```python
Setting name to Guido
Getting name
Guido
Setting name to fa
Getting name
fa
```

如果我们把`super(SubPerson, SubPerson)`，变成`super(SubPerson, self)`，那么会报这样的错误

```python
AttributeError: 'SubPerson' object has no attribute '_name'
```

这是为什么呢？我们平时在使用`super`时，都是用的后者的做法啊？

你要搞清楚这个问题前，你需要阅读这些

[python super中的mro表](http://blog.csdn.net/qq_17550379/article/details/79487433)

[super(type, self)与super(type1, type2)的区别](http://blog.csdn.net/qq_17550379/article/details/79508630)

[深入理解python super](http://blog.csdn.net/qq_17550379/article/details/79531891)

当然你可能是个高手，这些都清楚了。那么我们不妨思考一下，我们知道`super()`的内部机制是一个描述符（关于描述符的话题可以看这个[python描述符使用指南](http://blog.csdn.net/qq_17550379/article/details/79517349)），也就是说对于`super(SubPerson, SubPerson).name`这种操作，实际上是这样的`super(SubPerson, SubPerson).__get__['name']`，这个时候`SubPerson`内部是有一个`name`属性的（这个属性是我们通过`property`做出来的），所以可以访问。但是`super(SubPerson, self).__get__['name']`，我们发现实例对象并不存在`name`这个属性，自然就报错了。

其实`python`中的属性访问是一个很大的话题，这里就不展开。如有任何问题，希望大家指出(●'◡'●)。