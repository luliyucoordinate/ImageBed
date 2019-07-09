---
layout: post
title: 内存管理 primitives
category : cpp
tags : [cpp, stl]
stickie: true
---

```c++
void *p1 = malloc(512);
free(p1);

complex<int> *p2 = new complex<int>;
delete p2;

void *p3 = ::operator new(512);
::operator delete(p3);

#ifdef _MSR_VER
//以下两个函数都是non-static，一定要通过object调用
int *p4 = allocator<int>().allocate(3, (int*)0);
allocator<int>().deallocate(p4, 3);
#endif

#ifdef __BORLANDC__
//以下两个函数都是non-static，一定要通过object调用
int *p4 = allocator<int>().allocate(5);
allocator<int>().deallocate(p4, 5);
#endif

#ifdef __GNUC__
//以下两个函数都是static，可以通过全名调用，2.9ver
void *p4 = alloc::allocate(512);
alloc::deallocate(p4, 512);
//4.9ver 以下两个函数都是non-static，一定要通过object调用
void *p4 = allocator<int>().allocate(7);
allocator<int>().deallocate((int*)p4, 7);

void *p5 = __gnu_cxx::__pool_alloc<int>().allocate(9);
__gnu_cxx::__pool_alloc<int>.deallocate((int*)p5, 9);
#endif
```


New expression
===
```c++
void *mem = operator new(sizeof(Complex));
pc = static_cast<Complex*>(mem);
pc->Complex::Complex(1,2);//只有编译器可以这样调用ctor
//想要直接调用ctor，可以运用placement new；
//new(p)Complex(1,2);
void *operator new(size_t size, const std::nothrow _t&) _THROW0()
//nothrow struct is used as a function parameter to operator new to 
//indicate that the function should return a null pointer to report
//an allocation failure ,rather than throw an exception
{       // try to allocate size bytes
	void *p;
	while ((p = malloc(size)) == 0)
	    if (_callnewh(size) == 0)
	    {       // report no memory
	            _THROW_NCEE(_XSTD bad_alloc, );
	    }

	return (p);
}
delete expression
Complex* pc = new Complex(1,2);
...
delete pc;
pc->~Complex();
operator delete(pc);
void __cdecl operator delete(void *p)_THROW0()
{
	free(p);
}
```


Array new,array delete
===
```c++
Complex *pca = new Complex[3];
//唤起3次ctor
...
delete[] pca;//唤起3次dtor
//一下做法会造成内存泄漏，string的内部有指针
string *psa = new string[3];
...
delete psa;
```
```c++
int *pi = new int[10];
delete pi;
```

<a href="http://wx2.sinaimg.cn/mw690/af2d2659gy1feijde9fnuj20860hxdmk.jpg" data-lightbox="roadtrip">
<img src="http://wx2.sinaimg.cn/mw690/af2d2659gy1feijde9fnuj20860hxdmk.jpg" class="img-fluid">
</a>


61h为cookie，用来记录空间的大小，最后一个字节用来记录内存是在使用，还是未使用

```c++
Demo *p = new Demo[3];
delete [] p;
```

<a href="http://wx3.sinaimg.cn/mw690/af2d2659gy1feijdeoxfpj20830hjgrh.jpg" data-lightbox="roadtrip">
<img src="http://wx3.sinaimg.cn/mw690/af2d2659gy1feijdeoxfpj20830hjgrh.jpg" class="img-fluid">
</a>


第一个p指向的地址是00481c30，第二个p指向的地址是00481c34，如果写成delete p;的话，那么会从第一个p开始而不是第二个，就会出问题，多出一个3，这个3表示调用几次析构。如果Demo没有nontrivial dtor ,就不会记录3，也就是说，和上面的int类似，可以不加[]。  
关于内存空间，必须要调节16的倍数，所以增加了pad这个东西。



Placement new
===

Placement new 允许我们将object建立于 allocated memory中没有所谓的placement delete，因为placement new根本没有分配memory亦或称呼placement new 对应的operator delete为placement delete

```c++
#include <new>
char *buf = new char[sizeof(Complex)*3];
Complex *pc = new(buf)Complex(1,2);//等同于调用构造函数
void *mem = operator new(sizeof(Complex));//没有做任何事
void *operator new (size_t ,void *loc)
{ return loc; }
pc = static_cast<Complex*>(mem);
pc->Complex::Complex(1,2);


delete[] buf;
```
关于placement new，或指为new(p)，或指为::operator new(size, void*)



重载
===


重载::operator new/::operator delete
---
```c++
void *myAlloc(size_t size)
{ return malloc(size); }
void myAlloc(void *ptr)
{ return free(ptr); }
inline void* operator new(size_t size) {}
inline void* operator new[](size_t size) {}
inline void operator delete(size_t size) {}
inline void operator delete[](size_t size) {}
```


重载operator new/operator delete
---
```c++
Foo *p = new Foo;
...
delete p;

class Foo
{
public:
	void *operator new (size_t);
	void operator delete(void*, size_t);
};
```


重载operator new[]/operator delete[]
---
```c++
Foo *p = new Foo[n];
...
Delete[] p;

class Foo
{
public:
	void *operator new[] (size_t);
	void operator delete[](void*, size_t);
};
```


重载new()/delete()
---

我们重载class member operator new(),前提是每一个版本的声明都必须是独特的参数列，其中第一个参数必须是size_t，其余参数以new所指定的placement arguments为初值.出现new()小括号内的便是所谓的placement argument

```c++
Foo *pf = new (300,'c') Foo;//第一个参数表所示Foo的大小
//一般重载
void *operator new(size_t size)
{ return malloc(size); }
//placement new()的标准写法
void *operator new(size_t size, void *start)
{ return start; }
```

我们也可以重载class member operator delete(),但是他们不会被delete调用。只有当new所调用的ctor抛出异常，才会带调用这些重载版的operator delete()。他只能这样被调用，主要用来clean未完成创建的object所占的memory。即使operator delete() 未能一一对应operator new() ,编译器也不会报错，这样做的意思是放弃处理ctor发出的异常。  

Basic_string使用new(extra)    
平时使用的string就是typdef  

```c++
template<...>
class basic_string
{
private:
	struct Rep
	{
		void release() { if( --ref == 0) delete this;}
		inline static void* operator new(size_t, size_t);
		inline static void* operator delete(void *);
		inline static Rep* create(size_t);
		...
	};
	...
};
template<class charT, class traits, class Allocator>
inline basic_string<charT, traits, Allocator>::Rep*
basic_string<charT, traits, Allocator>::Rep::
create(size_t extra)
{
	extra = frob_size(extra + 1);
	Rep *p = new(extra) Rep;
	...
	return p;
}
template<class charT, class traits, class Allocator>
inline void *basic_string<charT, traits, Allocator>::Rep::
operator new (size_t s,size_t extra)
{
	return Allocator::allocate(s + extra * sizeof();//placement new的重载
}
template<class charT, class traits, class Allocator>
inline void basic_string<charT, traits, Allocator>::Rep::
opreraotr delete(void *ptr)
{
	Allocator::deallocate(ptr...
}

Pre-class allocator，1
#include <cstddef>
#include <iostream>
using namespace std;

class Screen
{
public:
	Screen(int x) :i(x) {};
	int get() { return i; }
	void *operator new(size_t);
	void operator delete(void*, size_t);
private:
	Screen *next;
	static Screen *freeStore;
	static const int screenChunk;
private:
	int i;
};
//
Screen *Screen::freeSore = 0;
const int Screen::screenChunk = 24;
void *Screen::operator new(size_t size)
{
	Screen *p;//这种设计多用了一个指针
	if(!freeStore)
	{
		size_t chunk = screenChunk *size;
		freeStore = p = reinterpret_cast<Screen*>(new char [chunk]);
//将一大块分割后，用链表穿起来
		for(; p!= &freeStore[screenChunk-1]; ++p)
			p->next = p +1;
		p->next = 0;
	}
	p = freeStore;
	freeStore = freeStore->next;
	return p;
}
void Screen::operator delete(void *p,size_t)
{
//将delete object插回
	(static_cast <Screen*>(p))->next = freeStore;
	freeStore = static_cast<Screen*>(p);
} 

Pre-class allocator，2
class Airplane
{
private:
	struct AirplaneRep
	{
		unsigned long miles;
		char type;
	};
private:
	union
	{
		AirplaneRep rep;
		Airplane *next;//嵌入式指针，相对于前面的来说非常不错
	};
//一个union 只配置一个足够大的空间以来容纳最大长度的数据成员，以上例而言，最大长
//度是AirplaneRep型态。
//在C++里，union 的成员默认属性页为public。union 主要用来压缩空间。如果一些数
//据不可能在同一时间同时被用到，则可以使用union。
public:
	unsigned long getMiles() { return rep.miles;}
	char getType() { return rep.type; }
	void set(unsigned long m, char t)
	{
		rep.miles = m;
		rep.type = t;
	}
	static void *opertor new(size_t size);
//注意这里static，编译器默认也是static，原因在于，要在对象创建时调用，
//如果不是static，对象创建时，可能这个东西还在创建的过程中
	static void operator delete(void *deadObject, size_t size);
private:
	static const int BLOCK_SIZE;	static Airplane *headOfFreeList;
};
Airplane *Airplane::headOfFreeList;
const int Airplane::BLOCK_SIZE=512;
void *Airplane::operator new(size_t size)
{
//当继承发生时
	if(size != sizeof(Airplane))
		return ::operator new(size);
	Airplane *p = headOfFreeList;
	if(p)
		headOfFreeList = p->next;
	else
	{
		Airplane *newBlock = static_cast<Airplane*>
		(::operator new(BLOCK_SIZE * sizeof(Airplane));
		for(int i = 1; i <BLOCK_SIZE - 1;++i)
			newBlock[i].next = &newBlock[i+1];
		newBlock[BLOCK_SIZE-1].next = 0;
		p = newBlock;
		headOfFreeList = &newBlock[1];
	}
	return p;
}
void Airplane::operator delete(void *deadObject, size_t size)
{
	if(deadObject == 0) return;
	if(size != sizeof(Airplane))
	{
		::operator delete(deadObject);
		return;
	}
	Airplane *carcass = static_cast<Airplane*>(deadObject);
	carcass->next = headOfFreeList;
	headOfFreeList = carcass;
}
```


static allocator
===

不同的class重写一遍几乎相同member operator new和member operator delete时，应该有方法将他们统一在一起，是他可以重用。

```c++
class allocator
{
private:
	struct obj
	{
		struct obj* next;//与linux里的链表做法一样
	}
public:
	void *allocate(size_t);
	void deallocate(void*, size_t);
private:
	obj* freeStore = nullptr;
	const int CHUNK = 5;
};
void *allocator::allocate(size_t size)
{
	obj *p;
	if(!freeStore)
	{
		size_t chunk = CHUNK *size;
		freeStore = p = (obj*)malloc(chunk);
		for(int  i = 0; i < (CHUNK-1); +i)
		{
			p->next = (obj*)((char*)p+size);
			p = p->next;
		}
		p->next = nullptr;
	}
	p = freeStore;
	freeStore = freeStore->next;
	return p;
}
void deallocate(void *p, size_t)
{
	((obj*)p)->next = freeStore;
	freeStore = (obj*)p;
}
```
此时Foo可以这样写了

```c++
class Foo
{
public:
    static allocator myAlloc;
public:
	static void *operator new (size_t size)
    { return myAlloc.allocate(size); }
	static void operator delete(void* pHead, size_t size);
    { return myAlloc.deallocate(pHead, size); }
};
```
这样做就方便了很多



Macro for static allocator
===
```c++
\表示续行符
#define DECLARE_POOL_ALLOC()\
public:\
	void *operator new(size_t size) { return myAlloc.allocate(size); }\
	void operator delete(void *p) { myAlloc.deallocate(p, 0); }\
protected:\
	static allocator myAlloc;
	
#define IMPLEMENT_POOL_ALLOC(class_name)\
allocator class_name::myAlloc;
```
原来的变成如下形式

```c++
class Foo
{
	DECLARE_POOL_ALLOC()
public:
	long L;
	string str;
public:
	Foo(long l) : L(l) {}
};
IMPLEMENT_POOL_ALLOC(Foo)
```


New handler
===

当operator new 没有能力分配申请的memory，会抛出异常std::bad_alloc execption以仍然可以让编译器new(nothrow) Foo;  
抛出异常之前会调用一个可由client指定的handler，以下是new handler的形式和设定方法：

```c++
typedef void(*new_handler)();
new_handler set_new_handler(new_handler p) throw();
```

设计良好的new handler只有俩个选择：  
让更多的memory可用 调用abort()和exit()



=default,=delete
===

It is not only for ctor and assignments,but also apllies to operator new/new[],operator delete/delete[] and their overloads

```c++
class Foo
{
public:
	Foo() = default;//表示使用默认版本，如果没有的话使用编译器合成版
	Foo(const Foo&)=delete;//表示不使用这个函数 
	Foo& operator=(const Foo&)=delete;
	~Foo()=defalut;
};

```
