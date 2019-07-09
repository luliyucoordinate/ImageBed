---
layout: post
title: python中的super到底是怎么样的（1）
category : python
tags : [python]
stickie: true
date: 2018-03-10 00:00:00
---

子类中调用父类的方法可以使用`super`函数

```python
class A:
    def func(self):
        print('A.func')
        
class B(A):
    def func(self):
        print('B.func')
        super().func() 
print(A().func())
print(B().func())
```

结果为

```python
A.func
None
B.func
A.func
None
```

注意`super()`这种写法是在`python3`里面的，如果`python2`的话你要这样用`super(B, self)`。当然在这里你同样可以这样去做

```python
class B(A):
    def func(self):
        print('B.func')
        A.func(self) 
```

同样没有任何问题。

好，那么问题就出现了。同样可以解决问题，`python`中为什么要出现`super()`呢？

我们看这样一个问题，我们的类的继承关系是一种菱形继承

```
	 Base
      /  \
     /    \
    A      B
     \    /
      \  /
       C
```

代码是这样的

```python
class Base:
    def __init__(self):
        print('Base.__init__')
class A(Base):
    def __init__(self):
        Base.__init__(self)
        print('A.__init__')
class B(Base):
    def __init__(self):
        Base.__init__(self)
        print('B.__init__')
class C(A, B):
    def __init__(self):
        A.__init__(self)
        B.__init__(self)
        print('C.__init__')
print(C())
```

输出结果是

```python
Base.__init__
A.__init__
Base.__init__
B.__init__
C.__init__
<__main__.C object at 0x000001A493AF6358>
```

这显然和你想象中的输出不一样，我们看到 `Base.__init__`被调用了两次。当然这有没有坏处，不好说。但是有一点可以明确的是，这里的结果和大多数程序员想要的结果不一样，那么就会出现被误用的问题。当然你非这样设计也没有问题，前提是你要知道这么做的结果。

我们使用`super()`函数去做的话，就是这样的

```python
class Base:
    def __init__(self):
        print('Base.__init__')
class A(Base):
    def __init__(self):
        super().__init__()
        print('A.__init__')
class B(Base):
    def __init__(self):
        super().__init__()
        print('B.__init__')
class C(A, B):
    def __init__(self):
        super().__init__()
        print('C.__init__')
```

结果是

```python
Base.__init__
B.__init__
A.__init__
C.__init__
<__main__.C object at 0x000001A493ACFE10>
```

嗯，这个结果是我们大多数人想要的。

那么我们就要想，为什么会这样呢？

我们每定义一个类，`python`会创建一个`MRO`列表，用来管理类的继承信息（你可以把它简单的理解为一个列表）。

```python
C.__mro__
Out[14]: (__main__.C, __main__.A, __main__.B, __main__.Base, object)
```

`python`通过这个列表从左到右的顺序，查找类的继承信息。这个列表是通过`C3`线性算法实现的，这个算法我们不去讨论，这里我们只要知道有这个表就可以了。

接着回到`super()`函数问题。我们可以通过这样的形式调用`super(cls, inst)`，这也是我们上面`python2`里使用的方案。这里的`cls`是一个类，`inst`可以是一个类也可以是一个对象。我们通过`inst`获取`MRO`列表。然后再这个列表中查找`cls`类，返回类`cls`后面一个类的信息。例如

```python
class C(A,B):
    def __init__(self):
        super(C, self).__init__()
        print('C.__init__')
print(C())
```

这里我们获取到临时对象`C()`的`MRO`列表

```python
(__main__.C, __main__.A, __main__.B, __main__.Base, object)
```

返回类`C`后面类`A`的信息，调用`super(A, self).__init__`。因为`self`还是`C`，`MRO`表不变，所以我们接着调用类`A`后的类`B`，`super(B, self).__init__`。同理接着调用`super(Base, self).__init__`，也就输出了`Base.__init__`。`B`中的`super().__init__()`执行完后，会执行`print('B.__init__')`。然后就是你看到的打印结果。

我这里要强调的是，如果你这里`A`类中使用的不是`super().__init__`，而是使用`A.__init__`，那么结果会像之前那样会出人意料。因为前者在调用时，传入的`inst`是`C`对象，而后者传入的是`A`类。这两者的`MRO`列表不同，所以就会出现不同的结果，为了你更好的理解我这里列出`A`和`B`的`MRO`表。

```python
A.__mro__
Out[15]: (__main__.A, __main__.Base, object)

B.__mro__
Out[16]: (__main__.B, __main__.Base, object)
```

你可以借此去推导，前面出现两次`Base.__init__`的原因。


虽然我的这篇文章貌似把`super`说的很明白了，但是我强烈建议你去读一下我的这篇文章[super(type, self)与super(type1, type2)的区别](http://blog.csdn.net/qq_17550379/article/details/79508630)，你会发现上面很多的东西都是有待商榷的QAQ!!!

当然这是我的理解，可能有不对之处，欢迎大家指出！