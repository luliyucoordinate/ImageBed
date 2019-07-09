---
layout: post
title: 	advance与next的区别
category : cpp
tags : [cpp, advance, next]
stickie: true
---

[`std::advance`](http://en.cppreference.com/w/cpp/iterator/advance)

- modifies its argument
- returns nothing
- works on input iterators or better (or bi-directional iterators if a negative distance is given)

[`std::next`](http://en.cppreference.com/w/cpp/iterator/next)

- leaves its argument unmodified
- returns a copy of the argument, advanced by the specified amount
- works on forward iterators or better (or bi-directional iterators if a negative distance is given))


前向迭代器[`ForwardIterator`](http://zh.cppreference.com/w/cpp/concept/ForwardIterator)  与输入迭代器[`InputIterator`](http://zh.cppreference.com/w/cpp/concept/InputIterator) 的区别在于输入迭代器自增后之前和该迭代器相等的都失效了。前向迭代器能够保证两个迭代器实例a与b，如果a==b，则一定也满足++a=++b，而输入迭代器不能保证这一点。  

constexpr与const的区别：constexpr表示在编译期就可以算出来（前提是为了算出它所依赖的东西也是在编译期可以算出来的）。而const只保证了运行时不直接被修改（但这个东西仍然可能是个动态变量）。

例如，转自[知乎夏洋](https://www.zhihu.com/question/35614219/answer/63681192)

```c++
template<int N> class C{};

constexpr int FivePlus(int x) {
  return 5 + x;
}

void f(const int x) {
  C<x> c1;            // Error: x is not compile-time evaluable.
  C<FivePlus(6)> c2;  // OK
}
```