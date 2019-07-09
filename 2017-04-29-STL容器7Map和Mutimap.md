---
layout: post
title: STL容器（7）Map和Mutimap
category : cpp
tags : [cpp, notes, cpp标准库]
stickie: true
---


定义于头文件 <map>

```c++
template<
    class Key,
    class T,
    class Compare = std::less<Key>,
class Allocator = std::allocator<std::pair<const Key, T> >> 
class map;
```
std::map是一个有序关联容器，包含具有唯一键的键值对。键使用比较函数Compare比较来进行排序。搜索，删除和插入操作具有对数复杂性。map通常实现为红黑树。

```c++
template<
    class Key,
    class T,
    class Compare = std::less<Key>,
class Allocator = std::allocator<std::pair<const Key, T> >> 
class multimap;
```
multimap是一个关联容器，它包含一个有序的键值对列表。键值按照Compare比较函数来排序。搜索、插入和删除操作具有对数的复杂性。
 相等的键值对在比较中的排序是保持插入时的顺序。 (C++11 起)

Map和Multimap的能力
---
Map和multimap后根据元素的key自动对元素排序。这么一来，根据已知的key查找某个元素时就能够有很好的效率，而根据已知value查找元素时，效率就会很糟糕。map和multimap身上有一个重要的限制：你不可以直接改变元素的key，因为这会破坏正确顺序。要修改元素的key，必须先移除该key的元素，然后插入key/value的元素。

Map和Multimap的操作函数
---
成员函数find用来查找第一个“拥有某key”的元素，并返回一个迭代器指向该位置。如果没有这样的元素，就返回容器的end。你不能以find查找拥有某特定value的元素。你可以使用下面的方法查找value：

```c++
std::multimap<std::string,float> coll;
std::multimap<std::string,float>::iterator pos;
for(pos = coll.begin(); pos != coll.end(); ++pos)
{
	if(pos->second == value)
	{
		do_something();
	}
}
```
还可以使用find_if:

```c++
auto pos = find_if(coll.begin(),coll.end(),
					[](const pair<float,float>& elem)
					{
						return elem.second == value;
					});
```
Map和multimap只支持“所有容器都提供的基本赋值操作”，赋值动作的两端容器必须拥有相同类型，尽管“比较准则”本身可能不同，但其类型必须相同。如果准则不同，准则本身也会随着容器被赋值或交换。但只要注意的是，元素比较函数只能用于类型相同的容器身上，换言之，两个容器的key、value、排序准则都必须相同的类型。
如果你一定要修改元素的key，只有一条路：以一个“value相同”的新元素替换掉旧元素。

```c++
namespace MyLib {
    template <typename Cont>
    inline
    bool replace_key (Cont& c,
                      const typename Cont::key_type& old_key,
                      const typename Cont::key_type& new_key)
    {
        typename Cont::iterator pos;
        pos = c.find(old_key);
        if (pos != c.end()) {
            // insert new element with value of old element
            c.insert(typename Cont::value_type(new_key,
                                               pos->second));
            // remove old element
            c.erase(pos);
            return true;
        }
        else {
            // key not found
            return false;
        }
    }
}
```
但是map提供一个非常方便的手法，然你改变元素的key。

```c++
//insert new element with value of old element
coll["new_key"] = coll["old_key"];
//remove old key
coll.erase("old_key");
```
有三种方法可以将value传入map或multimap

1.  运用value_type

```c++
std::map<std::string,float> coll;
coll.insert(std::map<std::string,float>::value_type("ot",12));
```
或

```c++
coll.insert(decltype(coll)::value_type("oit",12));
```
2.  运用pair<>

```c++
std::map<std::string,float> coll;
coll.insert(std::pair<std::string,float>("ot",12));
coll.insert(std::pair<const std::string,float>("ot",12));
```
3.  运用make_pair，这是C++11前最方便的做法

```c++
std::map<std::string,float> coll;
coll.insert(std::make_pair ("ot",12));
```
查看是否插入成功，可以使用和set和multiset相同的方法，也就是coll.insert().second。  
使用emplace函数与insert的区别在于：  
The element is constructed in-place by calling allocator_traits::construct with args forwarded.  
A similar member function exists, insert, which either copies or moves existing objects into the container.  
移除元素时，当心发生意外情况。移除迭代器所指对象时，有一个很大的危险。

```c++
std::map<std::string,float> coll;
for(auto pos = coll.begin();pos != coll.end(); ++pos)
{
	if(pos->second == value)
	{
		coll.earse(pos);//RUNTIME ERROR
	}
}
```
对pos所指元素erase，会使pos不再成为coll的一个有效迭代器。所以后面++pos，这样做是不合理的。  
C++11后的做法很简单，earse总是返回一个迭代器所指元素其后继元素：

```c++
std::map<std::string,float> coll;
for(auto pos = coll.begin();pos != coll.end();)
{
	if(pos->second == value)
	{
		coll.earse(pos);
	}
	else
	{
    	++pos;
	}
}
```
而在C++11之前的做法是：

```c++
for(auto pos = coll.begin();pos != coll.end();)
{
	if(pos->second == value)
	{
		coll.earse(pos++);	
	}
	else
	{
    	++pos;
	}
}
```
关联式数组的优点是你可以通过更方便的接口对map安插新元素。例如：

```c++
coll["fdsa"] = 12;
```
对于coll["fdsa"]的处理：  
如果存在key为“fdsa”的元素，上式会返回元素的reference。如果没有任何元素的key是“fdsa”，便为map插入一个新元素，令其key为“fdsa”，value以default构造函数完成，并返回一个reference指向新元素。  
但是上面的这种做法是会存在缺点的，你很容易想到如果这样做的话：

```c++
std::cout << coll["fdsaa"];
```
这和我预先的做法就有出入，它的结果是输出0。
