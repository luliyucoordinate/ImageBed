---
layout: post
title: 深入理解python super
category : python
tags : [python,  super]
stickie: true
date: 2018-03-13 00:00:00
---

我们在[super(type, self)与super(type1, type2)的区别](http://blog.csdn.net/qq_17550379/article/details/79508630)中，谈到了这样一个问题，在`python 3.6`中

```python
super(C, C).__init__
Out[108]: <function __main__.A.__init__>
```

而在，`python 2.7`里面是这样的

```python
>>> super(C, C).__init__
<unbound method C.__init__>
```

这是因为在`python 3.x`中已经没有`unbound method`这样的概念了。在`python 3.x`中，如果对象调用方法的话，会返回一个函数对象，如果你对于`function`和`method`的区别困惑的话，可以去阅读[python描述符使用指南](http://blog.csdn.net/qq_17550379/article/details/79517349#t5)。


在文章的末尾留下了一个疑问：

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

为什么文档中说`super(type, type)`是一个`bound`，但是我们在之前的测试中得到的是这样的结果

```python
>>> super(C, C).__init__
<unbound method C.__init__>
```

其实原因在于，我始终忽略了一个细节，就是文档中说的`bound super object`，也就是说它是一个绑定的`super`对象，而不是一个`unbound method`。

和`method`一样，既然有`bound super object`，那么就一定有`unbound super object`，根据文档上的叙述，就是通过`super(type)`实现`unbound super object`。

那么我们这样`super(C).__init__`调用会返回什么呢？会是`unbound method`吗？有了前面的基础，我想你这个时候应该不会轻易地下这样的结论了。

```python
>>> super(C).__init__
<method-wrapper '__init__' of super object at 0x03656490>
```

那么什么是`method-warpper`呢？

在`python 3.x`，你可以将它理解为通过`C`实现的`bound method`。至于`python 2.7`，(+_+)?

另外，`unbound super object`可以通过下面这种方式转化为`bound super object`（`python 2.7`）

```python
>>> super(C).__get__(C, C)
<super: <class 'C'>, <C object>>
>>> super(C).__get__(c, C)
<super: <class 'C'>, <C object>>
>>> super(C, C)
<super: <class 'C'>, <C object>>
>>> super(C, c)
<super: <class 'C'>, <C object>>
```

如果在`python 3.x`的话

```python
super(C).__get__(C, C)
Out[23]: <super: __main__.C, __main__.C>
super(C).__get__(c, C)
Out[24]: <super: __main__.C, <__main__.C at 0x19b1ad02438>>
super(C, C)
Out[25]: <super: __main__.C, __main__.C>
super(C, c)
Out[26]: <super: __main__.C, <__main__.C at 0x19b1ad02438>>
```

至此你应该对于`super`对象有一个大概的映像了，并且你也就清楚了[python描述符使用指南](http://blog.csdn.net/qq_17550379/article/details/79517349#t0)简介中所说的`描述符是一个强大的通用协议，它们是属性，方法，静态方法，类方法和super()的工作机制`。