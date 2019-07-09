---
layout: post
title: std::allocator
category : cpp
tags : [cpp, stl]
stickie: true
---

在vc6的allocator只是以::operator new 和::operator delete 完成allocate()和deallocate(),没有任何特殊的设计。  
在bc5中的allocator只是以::operator new 和::operator delete 完成allocate()和deallocate(),没有任何特殊的设计。  
在G2.9中的allocator只是以::operator new 和::operator delete 完成allocate()和deallocate(),没有任何特殊的设计，但是它内部并没有使用，而是使用的std::alloc。  
在4.9版中叫__pool_alloc，但是这两个都不是标准分配器。

```c++
// NB: __n is permitted to be 0.  The C++ standard says nothing
 // about what the return value is when __n == 0.
pointer
allocate(size_type __n, const void* = 0)
{
	if (__builtin_expect(__n > this->max_size(), false))
		std::__throw_bad_alloc();

	return static_cast<_Tp*>(::operator new(__n * sizeof(_Tp)));
}

// __p is not permitted to be a null pointer.
void
deallocate(pointer __p, size_type)
{ ::operator delete(__p); }
```

alloc的设计  
申请32bytes，由于pool为空，所以成功所求32*20*2+RoundUp(0(目前的申请总量)>>4) =1280，从中切出一个，另外的19个给list#3，剩余640备用。每次分配前都是先看原先的是否有剩余pool，从pool切给出来的数量永远在1~20之间，pool余量不足够的时候，先将pool余量给相应的list#，然后索取相应的内存。当内存不够时，往右边找一块给他。如果就近找不到的话，就会失败。但是这样的话，还有很多的空内存未使用

```c++
//第二级分配器
 enum { __ALIGN = 8 };//定义常量,小区快的下限
 enum { __MAX_BYTES = 128 };//上限
 enum { __NFREELISTS = __MAX_BYTES/ __ALIGN };//freelist的长度
 template <bool threads, int inst>
 class __default_alloc_template
 {
 private:
 	static size_t ROUND_UP(size_t bytes)
 	{
 		return ((bytes) + _ALIGN-1) & ~(_ALIGN - 1));
 	}
 private:
 	union obj
 	{
 		union obj* free_list_link;
 	};
 private:
 	static obj *volatile free_list[__NFREELISTS];
 	//计算list#
 	static size_t FREELIST_INDEX(size_t bytes)
 	{
 		return (((bytes) +__ALIGN-1)/__ALIGN-1);
 	}
 	static void* refill(size_t n);
 	static char *chunk_alloc(size_t size, int &nobjs);
 	static char *start_free;//指向pool头
 	static char *end_free;//指向pool尾
 	static size_t heap_size;
 public:
 	static void* allocate(size_t n)
 	{
 		obj* volatile *my_free_list;
 		obj* result;
 		if(n > (size_t) __MAX_BYTES)//改用第一级
 		{
 			return (malloc_alloc::allocate(n));
 		}
 		my_free_list = free_list + FREELIST_INDEX(n);
 		result = *my_free_list;
 		if(result == 0_
 		{
 			void* r = refill(ROUND_UP(n));
 			return r;
 		}
 		*my_free_list = result->free_list_link;
 		return (result);
 	}
 	//回收的时候，把要回收的部分插入二级链表的头
 	//函数内部没有做p指针的检查，如果这个p指针不是这个系统的，
 	//如果他不是8的倍数的话，回收后再分配时会出问题，原来分配给list#1，
 	//可能现在到了list#2
 	static void deallocate(void* p,size_t n)
 	{
 		obj* q = (obj*)p;
 		obj* volatile *my_free_list;
 		if(n > (size_t)__MAX_BYTES)
 		{
 			malloc_alloc::deallocate(p,n);
 			return;
 		}
 		my_free_list = free_list +FREELIST_INDEX(n);
 		q->free_list_link = *my_free_list;
 		*my_free_list = q;
 	}
 	static void* reallocate(void* p, size_t old_sz, size_t new_sz);//略
 };
 template <bool threads, int inst>
 char *
 __default_alloc_template<threads, inst>::
 chunk_alloc(size_t size, int& nobjs)
 {
 	char *result;
 	size_t total_bytes = size * nobjs;
 	size_t bytes_left = end_free - start_free;
 	
 	if( bytes_left >= total_bytes)//pool能否满足20个
 	{
 		result = start_free;
 		start_free += total_bytes;
 		return(result);
 	}
 	else if( bytes_left >= size)//pool能否满足1个
 	{
 		nobjs = bytes_left /size;
 		total_bytes = size * nobjs;
 		result = start_free;
 		start_free += total_bytes;
 		return(result);
 	}
 	else
 	{
 	//空pool或者为碎片
 		size_t bytes_to_get = 2*total_bytes + ROUND_UP(heap_size >> 4);
 		//将碎片挂接
 		if( bytes_left > 0)
 		{
 			obj* volatile *my_free_list = free_list + FREELIST_INDEX(bytes_left);
 			((obj*)start_free)->free_list_link = *my_free_list;
 			*my_free_list = (obj*)start_free;
 		}
 		//分配内存
 		start_free = (char *)malloc(bytes_to_get);
 		if( 0 == start_free)//分配失败的话，从freelist中找
 		{
 			int i;
 			obj* volatile *my_free_list, *p;
//try to make do with what we have.that can’t hurt.
//we do not try smaller requests,since that tends
//to result in disaster on muti-process machines.
 			for( i = size; i <= __MAX_BYTES; i+= __ALIGN)
 			{
 				my_free_list = free_list + FREELIST_INDEX(i);
 				p = *my_free_list;
 				if( 0 != p)
 				{
 					*my_free_list = p->free_list_link;
 					start_free = (char *)p;
 					end_free = start_free + i;
 					return (chunk_alloc(size, nobjs));
 				}
 			}
 			//表示memory已经‘没有’了
 			end_free = 0;
 			start_free = (char*)malloc_alloc::allocate(bytes_to_get);
 		}
 		heap_size += bytes_to_get;
 		end_free = start_free + bytes_to_get;
 		return (chunk_alloc(size, nobjs));
 	}
 }
 template <bool threads, int inst>
 void *
 __default_alloc_template<threads, inst>::refill(size_t n)//n已经是8的倍数
 {
 	int nobjs = 20;//预设20个
 	char *chunk = chunk_alloc(n, nobjs);
 	obj* volatile *my_free_list;
 	obj* result;
 	obj* current_obj;
 	obj* next_obj;
 	int i;
 	if( 1== nobjs) return (chunk);
 	my_free_list = free_list_link;
 	result = (obj*)chunk;
 	*my_free_list = next_obj = (obj*)(chunk + n);
 	//在chunk内建立freelist
 	for( i = 1; ; ++i)
 	{
 		current_obj = next_obj;
 		next_obj = (obj*)((char*)next_obj + n);
 		if( nobjs-1 == i)
 		{
 			current_obj->free_list_link = 0;
 			break;
 		}
 		else
 		{
 			current_obj->free_list_link = next_obj;
 		}
 	}
 	return (result);
 }
template <bool threads, int inst>
char *__default_alloc_template<threads, inst>;:start_free = 0;
template <bool threads, int inst>
char *__default_alloc_template<threads, inst>;:end_free = 0;
template <bool threads, int inst>
char *__default_alloc_template<threads, inst>;:heap_free = 0;
template <bool threads, int inst>
__default_alloc_template<threads, inst>::obj* volatile
__default_alloc_template<threads, inst>::free_list[_NFREELISTS]
= { 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}
typedef __default_alloc_template<false, 0> alloc;
```
deallocate完全没有free，设计上的缺陷，没有变量记录freelist的起始位置

