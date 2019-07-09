---
layout: post
title: 关于python中super的困惑（3）
category : python
tags : [python]
stickie: true
date: 2018-03-08 00:00:00
---

我这次带来了新的问题，至于上次文末那个问题，我们还是

我们看这样的一个代码

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

输出结果为

```python
Setting name to Guido
Getting name
Guido
Setting name to fa
Getting name
fa
```

我们注意到这里`super(SubPerson, SubPerson).name.__set__(self, value)`，这是为什么？

并且我们将上面的结构变成这样`super(SubPerson, self).name.__set__(self, value)`，结果出现如下错误

```python
AttributeError: 'SubPerson' object has no attribute '_name'
```

这是为什么呢？我们先思考后者为什么报错。

分析这个问题之前，你要对`python`的`MRO`列表有所了解。如果不清楚的话，你可以看这篇 [python super中的mro表](http://blog.csdn.net/qq_17550379/article/details/79487433)

我们先打印`SubPerson`的`MRO`列表

```python
SubPerson.__mro__
Out[18]: (__main__.SubPerson, __main__.Person, object)
```

也就是说，我们获取`MRO`列表中`SubPerson`后面一个类`Person`的信息。如果这个时候你认为调用了`Person.__dict__`，那你应该看一下我写的这篇[super(type, self)与super(type1, type2)的区别](http://blog.csdn.net/qq_17550379/article/details/79508630)。你应该就知道了

```python
super(SubPerson, SubPerson).name == Person.name
Out[117]: True
super(SubPerson, s).name == Person.name
Out[118]: False
```



那么会在`Person.__dict__`中查找`name`，这会调用`__get__`方法。

```python
Person.__dict__
Out[46]: 
mappingproxy({'__dict__': <attribute '__dict__' of 'Person' objects>,
              '__doc__': None,
              '__init__': <function __main__.Person.__init__>,
              '__module__': '__main__',
              '__weakref__': <attribute '__weakref__' of 'Person' objects>,
              'name': <property at 0x255cde5fea8>})
```

我们看到`__get__`方法中`return self._name`，我们并没有`_name`这个属性，那么就报错了。

接着我们来思考`super(SubPerson, SubPerson).name`的问题。



我们首先用上面`super(SubPerson, SubPerson).name.__set__(self, value)`这个例子，看`s.name`到底是怎么被执行的。首先`print('Getting name')`，接着`super().name`，也就是`super(SubPerson, self).name`（这里的`self`就是`SubPerson`类的实例）。根据前面分析的结果，接着会调用`Person.name`，接着就是`return self._name`。这个时候你就会困惑了？我们明明没有给`self._name`赋初值啊（`self.name = name`）？到底发生了什么？

我们这个时候回到`s = SubPerson('Guido')`，看看到底发生了什么。首先`self.name = name`，要注意了，这里很关键，我们知道这里的`self`是一个`SubPerson`的对象，接着调用**SubPerson的setter方法**。接着这句话`print('Setting name to', value)`就被执行了，输出结果是`Setting name to Guido`。接着根据上面的分析就是调用`Person.name.__set__(self, value)`，通过调用`Person.__dict__['name'].__get__(None, Person)`这个时候`self._name`被设置了（`self._name = value`）。所以当我们调用`s.name`时，会成功执行。

接着，如果`super(SubPerson, self).name.__set__(self, value)`话，那么`super(SubPerson, self).name`会先在`type(s).__dict__`中查找`name`，结果会调用`__get__`方法，最后会调用`return self._name `，我们还没有`_name`属性，自然就报错了。