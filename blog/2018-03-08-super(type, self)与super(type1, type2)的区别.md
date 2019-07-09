---
layout: post
title: super(type, self)与super(type1, type2)的区别
category : python
tags : [python, super]
stickie: true
date: 2018-03-08 00:00:00
---

好的，我最近通过一些实验发现，我的理解有一些问题。在此之前我们先关心一下`python`文档中是怎么描述`super`的

- super(type[, object-or-type])
    Return the superclass of type. If the second argument is omitted the super object returned is unbound. If the second argument is an object, isinstance(obj, type) must be true. If the second argument is a type, issubclass(type2, type) must be true. super() only works for new-style classes.

我之所以说我们之前 [ python super中的mro表](http://blog.csdn.net/qq_17550379/article/details/79487433)文章中还有一些问题没有解决，也是因为文档的第一句话`返回一个superclass类型`，但是我们这样测试的时候出现了问题

```python
c = C()
super(C, c) == A
Out[18]: False
```

这就让我很困惑了，**文档中的第一句描述是不对的**。这其实很好理解

```python
A.__mro__
Out[19]: (__main__.A, __main__.Base, object)
C.__mro__
Out[20]: (__main__.C, __main__.A, __main__.B, __main__.Base, object)
```

因为`A`的`mro`表中不包含`B`。好的，我们处理了第一个问题。

我现在要提到的是两个新的概念`bound`和`unbound`，看这样的一个例子

```python
class Base:
    def __init__(self, name):
        self.name = name
    def func(self):
        print('name ', self.name)
a = Base('a')   
```

我们这样去做（python2.7下）

```python
>>> a.func
<bound method Base.func of <__main__.Base instance at 0x03479440>>
>>> Base.func
<unbound method Base.func>
```

而在`python3.6`下

```python
>>> a.func
Out[35]: <bound method Base.func of <__main__.Base object at 0x0000026FBF418EF0>>
>>> Base.func
Traceback (most recent call last):
  File "<ipython-input-36-5647957570f7>", line 1, in <module>
    Base.func
AttributeError: type object 'Base' has no attribute 'func'
```

我们暂时不讨论这个变化，我们先在`python2.7`下看问题。字面上很容易理解`bound`就是绑定，我们通过实例去调用类的方法实际上是这样做的`Base.__dict__['func'].__get__(a, Base)`，很容易验证

```python
>>> Base.__dict__['func'].__get__(a, Base) == a.func
True
```

而对于`unbound`操作来说

```python
>>> Base.__dict__['func'].__get__(None, Base) == Base.func
True
```

你应该注意到了`bound`和`unbound`的区别，就是`__get__`操作的第一个参数是不是传入了一个实例对象。

我们将上述的过程放到`python3.6`下同样也是成立的，以下是验证。

```python
Base.__dict__['func'].__get__(a, Base) == a.func
Out[46]: True
Base.__dict__['func'].__get__(None, Base) == Base.func
Out[47]: True
```

我们继续回到`super`的话题，我们这里给出`super`是什么。它是一个代理对象，用来访问`MRO`表中的方法。

我们在`python2.7`下回答上一篇文章中没有提到的问题，`super(C, C)`和`super(C, c)`有什么关系

```python
>>> super(C, C)
<super: <class 'C'>, <C object>>
>>> super(C, c)
<super: <class 'C'>, <C object>>
>>> super(C, C).__init__ == A.__init__
True
>>> super(C, c).__init__ == A.__init__
False
>>> super(C, C) == super(C, c)
False
```

我们发现这里出现一个然我们很困惑的东西，为什么`super(C, C)`和`super(C, c)`既相同又不相同？我想这应该是一个bug。我们到`python3.6`下验证

```python
super(C, C)
Out[89]: <super: __main__.C, __main__.C>
super(C, c)
Out[90]: <super: __main__.C, <__main__.C at 0x26fbf253518>>
super(C, C).__init__ == A.__init__
Out[91]: True
super(C, c).__init__ == A.__init__
Out[92]: False
```

那么现在我们就应该猜到了`super(C, C).__init__`和`super(C, c).__init__`的区别，也就是一个`unbound`一个`bound`。很容易验证（`python 3.6`）

```python
super(C, C).__init__
Out[108]: <function __main__.A.__init__>
super(C, c).__init__
Out[109]: <bound method A.__init__ of <__main__.C object at 0x0000026FBF253518>>
```

但是在`python 2.7`下又出现了这样

```python
>>> super(C, C).__init__
<unbound method C.__init__>
>>> super(C, c).__init__
<bound method C.__init__ of <__main__.C object at 0x039C0EF0>>
```

原因可以看这篇[深入理解python super](http://blog.csdn.net/qq_17550379/article/details/79531891)

那么是否可以这样去做`super(C, C).__dict__['__init__'].__get__(None, A)`，并不可以，这样做是错的！！！

```python
>>> super(C, C).__dict__['__init__'].__get__(None, A)
Traceback (most recent call last):
  File "<ipython-input-96-07b8366bac1b>", line 1, in <module>
    super(C, C).__dict__['__init__'].__get__(None, A)
TypeError: 'getset_descriptor' object is not subscriptable
```

究其原因，其实就像本文的一开头

```python
super(C, C) == A
Out[101]: False
super(C, c) == A
Out[102]: False
```

原因我也说了，`super`返回的是一个代理对象，自然和对象本身不同。

貌似没什么问题了，但是，，，

```python
python2.7
>>> print super.__doc__
super(type, obj) -> bound super object; requires isinstance(obj, type)
super(type) -> unbound super object
super(type, type2) -> bound super object; requires issubclass(type2, type)
Typical use to call a cooperative superclass method:
class C(B):
    def meth(self, arg):
        super(C, self).meth(arg)
python3.6
>>> print(super.__doc__)
super() -> same as super(__class__, <first argument>)
super(type) -> unbound super object
super(type, obj) -> bound super object; requires isinstance(obj, type)
super(type, type2) -> bound super object; requires issubclass(type2, type)
Typical use to call a cooperative superclass method:
class C(B):
    def meth(self, arg):
        super().meth(arg)
This works for class methods too:
class C(B):
    @classmethod
    def cmeth(cls, arg):
        super().cmeth(arg)
```

你也看到了`super(type, type2)`是一个`bound`，QAQ。看这篇[深入理解python super](http://blog.csdn.net/qq_17550379/article/details/79531891)