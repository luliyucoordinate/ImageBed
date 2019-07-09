---
layout: post
title: python中__get__、__getattr__以及__getattribute__有什么区别
category : python
tags : [python]
stickie: true
date: 2018-03-12 00:00:00
---

我们还是先看官方文档的描述

- `object.__get__(self, instance, owner)`

  Called to get the attribute of the owner class (class attribute access) or of an instance of that class (instance attribute access). *owner* is always the owner class, while *instance* is the instance that the attribute was accessed through, or None when the attribute is accessed through the *owner*. This method should return the (computed) attribute value or raise an **AttributeError** exception.

- `object.__set__(self, instance, value)`

  Called to set the attribute on an instance *instance* of the owner class to a new value, *value*.

- `object.__delete__(self, instance)`

  Called to delete the attribute on an instance *instance* of the owner class.

文档也说的很清楚了，通过调用`__get__`方法获取类或者实例的属性，参数`instance`是实例，参数`owner`是类。另外的`__set__`和`__delete`同样。

