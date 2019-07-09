---
layout: post
title: piecewise_construct的作用
category : cpp
tags : [cpp, piecewise_construct ]
stickie: true
---


常量 std::piecewise_construct 是空的结构体标签类型 std::piecewise_construct_t 的一个实例。  
std::piecewise_construct_t 是用于在接收二个 tuple 参数的不同函数间消歧义的空结构体标签类型。  
不使用 std::piecewise_construct_t 的重载假设每个 tuple 参数各变成一个 pair 的元素。使用 std::piecewise_construct_t 的重载假设每个 tuple 参数用于逐块构造一个指定类型的新对象，而它将成为 pair 的元素。  

```c++
#include <iostream>
#include <utility>
#include <tuple>
 
struct Foo {
    Foo(std::tuple<int, float>) 
    {
        std::cout << "Constructed a Foo from a tuple\n";
    }
    Foo(int, float) 
    {
        std::cout << "Constructed a Foo from an int and a float\n";
    }
};
 
int main()
{
    std::tuple<int, float> t(1, 3.14);
    std::pair<Foo, Foo> p1(t, t);	//Constructed a Foo from a tuple
								//Constructed a Foo from a tuple
    std::pair<Foo, Foo> p2(std::piecewise_construct, t, t);	//Constructed a Foo from an int and a float
    													//Constructed a Foo from an int and a float
}
```