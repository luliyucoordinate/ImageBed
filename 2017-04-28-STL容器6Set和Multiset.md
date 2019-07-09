---
layout: post
title: STL容器（6）Set和Multiset
category : cpp
tags : [cpp, notes, cpp标准库]
stickie: true
---


Set和Multiset
===
定义于头文件 <set>

```c++
template<
    class Key,
    class Compare = std::less<Key>,
class Allocator = std::allocator<Key>> 
class set;
```
std::set是一个关联容器，是一个有序的集合，集合中包含不可重复的、类型为Key的元素。排序通过使用类型为Compare的比较函数比较来实现。搜索，删除和插入操作具有对数时间复杂度。set通常实现为红黑树。

```c++
template<
    class Key,
    class Compare = std::less<Key>,
class Allocator = std::allocator<Key>> 
class multiset;
```
multiset 是一个关联容器，它包含一些有序的Key类型的对象。与set不同的是，它允许多个带有相同值的键存在。排序通过使用键比较函数比较来实现。搜索，插入和删除操作具有对数的复杂性.  
在比较中相等的元素，顺序为插入时的顺序，且不会改变。 (C++11 起)

Set和Multiset的能力
---
自动排序会造成set和multiset的一个重要限制：你不能直接改变元素值，因为这样会打乱原本正确的顺序。  
因此，要改变元素值，必须先删除旧元素，在插入新元素。一下接口反映这种行为：  
Set和multiset不提供任何操作函数可以直接访问元素。  
从迭代器的角度看，元素只是一个常量。

Set和Multiset的操作函数
---
排序准则也被用来检查元素的相等性。采用默认排序准则时，两元素的相等性检查如下：

```c++
if(!(elem1 < elem2)||（elem2 < elem1))
```
这种做法有三种好处：  
1.  只需传递一个实参作为排序准则
2.   不必针对元素类型提供operator==
3.   可以对“相等性”有相反的定义。
元素比较只适用于类型相同的容器。换而言之，元素和排序准则则必须有相同的类型，否则编译器会报错。

```c++
std::set<float> c;
std::set<float,std::greater<float>> c2;
if(c == c2)//ERROR different  types
{}
```
lower_bound和upper_bound分别返回第一个和最后一个“元素可安插点”。换而言之，lower_bound返回第一个“大于等于实参值”的元素位置，upper_bound返回第一个“大于实参值”的位置。equal_range则是将lower_bound和upper_bound的返回值做成一个pair返回，所以他返回的是“与实参值相等”的元素所形成的区间。  
和所有关联式容器类似，这里迭代器是双向迭代器。所以，对于那些“只能接受随机访问迭代器”的STL算法。  
更重要的是，从迭代器的角度看，所有元素都被视为常量。这使得你无法对set或multiset调用更易性算法。例如你不能对它们调用remove，因为remove算法实际上是以其实参值覆盖被移除的元素。  
注意，用于安插元素的函数：insert和emplace，其返回值不尽相同：  
返回类型之所以不相同，原因是：multiset允许元素重复而set不允许。因此，如果将某元素安插至set内，而该set内含同值元素，安插失败。所以set的返回类型是以pair组织起来的两个值：  
1.  pair结构中的second成员表示安插是否成功。
2.   pair结构中first成员表示新元素的位置，或现存的同元素位置。
