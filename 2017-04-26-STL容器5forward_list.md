---
layout: post
title: STL容器（5）forward_list
category : cpp
tags : [cpp, notes, cpp标准库]
stickie: true
---


Forward list
===
定义于头文件 <forward_list>

```c++
template<
    class T,
class Allocator = std::allocator<T>> 
class forward_list;
```
(C++11 起)
单向列表是一个容器，支持在其任何地方快速插入和删除元素，不支持快速的随机访问。它被实现为单向链表，和C中它的实现相比，基本上不会有任何开销。当不需要双向迭代的时候，与std::list相比，该容器具有更高的空间利用率。

Forward list的能力
---
相较于list，forward list有以下约束：  
1.  forward list只提供前向迭代器，而不是双向迭代器。因此它不支持反向迭代器，这意味着reverse_iterator不再提供。
2.  forward list不提供size函数。
3.  forward list没有这项最末元素的锚点。基于这个原因，forward list不提供back、push_back和pop_back函数
4.  对于所有“令元素被安插或删除与forward list的某特定位置上”的成员函数，forward list提供特殊版本。原因是你必须传递第一个被处理元素的前一个位置，因为你必须在哪里指定一个新的后继元素，然而由于froward list不允许回头，因此对于这些成员函数，你必须传递迁移元素位置。

Forward list的操作
---
Forward list不提供size，原因是他不存储元素的数量，亦无法在常量时间内算出它。此外也为了凸显size是一个费时操作，所以不提供它。如果你必须计算元素个数，可以使用distance 函数：  

```c++
std::forward_list<int> l;
std::cout << "l.size()" << std::distance(l.begin(), l.end()) << std::endl;
```
forward list只提供了front函数用于元素访问。  
注意，面对forward list提供的所有安插、安放、抹除成员函数，你会有个疑问：他们需要获取一个元素位置，而你打算在这个位置上安插元素或删除元素。但这就必需改动前导元素，因为必须更改前导元素的pointer。但是对于forward list你无法回头，因此成员函数的行为就会和list不同。所有以after为结尾的函数，会将新元素安插于给定元素之后。  
当你使用成员函数，并使用begin_before，一个典型的例子如下：

```c++
std::forward_list<int> fwlist = {1,2,3};
fwlist.insert_after(fwlist.before_begin(),
					{ 3,4,5});
```
要注意的是，调用after成员函数并传入end或cend函数将导致不明确的行为，因为如果要在forward list的尾端附加一个新元素，你必须传入终端元素的位置：  

```c++
fwlist.insert_after(fwlist.end(),1);// RUNTIME ERROR
```
再插入元素时，要注意的是由于使用的是一个单向链表，所以你只可以不断的向前，但是当你尝试找出某个元素，准备在那安插或删除元素时，“找到的当下”代表“已经超出了”，因为，想要在这个位置安插或删除元素，你必须改写给出的前一元素。  
这里又有这样几种做法，一是可以通过记录前一位置，不断++操作，另一种是使用next函数。  

```c++
auto posBefore = list.before_begin();
for(; next(posBefore) != list.end(); ++posBefore)
{
	if( *next(posBefore) != list.end9); ++posBefore)
	{
		if(*next(posBefore) %2 == 0)
		{
			break;
		}
	}
}
```
注意这里我们要理解一个概念。begin指向的是第一个元素的位置，而before_begin指向的是第一个元素的前面位置，也就是真正意义上的首节点。  
你也可以自己定义算法，找出“拥有特定值”或“满足某特定条件”的元素的前一位置。  

```c++
template <typename InputIterator, typename Tp>
inline InputIterator
find_before (InputIterator first, InputIterator last, const Tp& val)
{
    if (first==last) {
        return first;
    }
    InputIterator next(first);
    ++next;
    while (next!=last && !(*next==val)) {
        ++next;
        ++first;
    }
    return first;
}

template <typename InputIterator, typename Pred>
inline InputIterator
find_before_if (InputIterator first, InputIterator last, Pred pred)
{
    if (first==last) {
        return first;
    }
    InputIterator next(first);
    ++next;
    while (next!=last && !pred(*next)) {
        ++next;
        ++first;
    }
    return first;
}
```
注意，结合操作的来源端和目的端可以相同。因此你可以在同一个forward list中splice operation。但是要注意的是，调用splice_after 并传入end会导致不明确的行为  

```c++
fwlist.splice_after(fwlist.end(),
					fwlist,
					fwlist.begin());//RUNTIME ERROR

```
