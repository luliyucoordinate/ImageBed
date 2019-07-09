---
layout: post
title: c++ ADL(Argument-Dependent Lookup)查找
category : cpp
tags : [c++, ADL]
stickie: true
date: 2018-04-19 00:00:00
---

# 0X00 简述

`ADL`全称是`Argument-Dependent Lookup`的简写，作用是扩展命名空间的查找范围，通过函数参数查找函数的命名空间。

# 0x01 问题引出

我们通过一个例子引出为什么要有这种机制。现在我们有这样一种命名空间`f1`

```c++
namespace f1
{
    struct data {};
    data operator+(const data& A, const data& B)
    {
        data C;
        add(A, B, C);//A+B-->C
        return C;
    }
}
```

我们想要实现这样的操作

```c++
A = B + C + D
```

如果没有`ADL`机制的话，我们式子就会变得很复杂

```c++
A = f1::operator+(f1::operator+(B, C), D);
```

而由于出现了`ADL`这种机制，我们的操作写法就变得很简洁

```c++
A = operator+(operator+(B, C), D);
```

这实际上等价于`A = B + C + D;`这种写法。我们这里通过`ADL`机制获取了参数的命名空间。

这个问题看上去很容易，但是一旦我们使用了多重命名空间、`name hiding`、`overload`混合，那么这个问题将会变得很复杂。

# 0x02 问题深入

我们看这样的一个问题

```c++
namespace c1
{
    namespace c2
    {
        struct cc{}
        void f(const cc& o){}
    }
    void f(const c2::cc& o){}
}
void f(const c1::c2::cc& o){}
namespace f1
{
    void f(const c1::c2::cc& o){}
    namespace f2
    {
        void f(const c1::c2::cc& o){}
        void g()
        {
            c1::c2::cc o;
            f(o);
        }
    }
}
```

这个时候我问你，在`f1::f2::g`中的`f(o)`使用的是哪个`f` ？我们分析一下，我们有几个选择

- 因为我们知道参数`o`的类型是`c1::c2::cc`，所以我们通过`ADL`推测出命名空间为`c1::c2`，这时候的答案就是`c1::c2::f`。
- `c1::f`可以吗？
- `::f`可以吗？
- `f1::f`可以吗？
- `f1::f2::f`，这个有可能吗？可能啊，因为我们的`g`函数的命名空间就是`f1::f2::g`。同一个命名空间下的函数，这样调用也没问题啊。

OK! 这个时候问题就出现了。到底答案是哪个呢？我们加大难度，这个时候我们将全局函数`f`的参数去除`const`，变为这样

```c++
void f(c1::c2::cc& o){}
```

如果我们这个时候从函数重载（`overload`）的角度考虑这个问题，那么现在这个全局的`f`成为了最佳匹配。但是它被`f1::f2::f`这个函数给隐藏了（`name hiding`）。那么同样的道理`f1::f`和`c1::f`也就不会被调用了。那么我们一定要使用这个全局函数怎么做呢？可以这样子做

```c++
void f(c1::c2::cc& o){}
namespace f1
{
    void f(const c1::c2::cc& o){}
    namespace f2
    {
        void f(const c1::c2::cc& o){}
        using ::f;
        void g()
        {
            c1::c2::cc o;
            f(o);
        }
    }
}
```

这个时候对于函数`g`，函数`c1::c2::f`和`::f`都是可调用的，但是根据参数类型的最佳匹配原则，我们调用了`::f`。

接着回到最初问题，这个时候我们就有了两个答案`c1::c2::f`和`f1::f2::f`。实际上这个程序就会编译出错。

# 0x03 问题后续

我们接着看这样的问题

```c++
namespace c1
{
    namespace c2
    {
        struct cc{};
        void f(cc& o){}				//#1
    }
}
void f(c1::c2::cc& o){}
namespace f1
{
    namespace f2
    {
        void f(const c1::c2::cc& o){}	//#2
        void g()
        {
            c1::c2::cc o;
            const c1::c2::cc c(o);
            f(o);
            f(c);
        }
        void f(c1::c2::cc& o){}		//#3
    }
}
```

因为`#3`是定义于`g`的后面，所以在`g`中是不可见的。全局函数`::f`被`#2`隐藏（`name hiding`）。因此对于`f(o)`来说，我们通过使用`ADL`可以调用`#1`，我们通过`name hiding`也可以调用`#2`，但是我们最后调用最佳匹配`#1`。而对于`f(c)`我们通过同样的分析，我们知道调用`#2`。

最后我们总结为以下三个步骤帮助我们判断

- 找到所有的重载函数
  - 调用函数自己的命名空间中
  - 调用函数的父命名空间中
  - 参数的命名空间中
  - 通过`using directive;`导入的命名空间中（`using namespace std;`）
  - 通过`using declaration;`导入的命名空间中（`using std::cout;`）
- 排除掉所有的`name hiding`
- 选择最佳匹配（如果没有最佳匹配，程序编译出错）
