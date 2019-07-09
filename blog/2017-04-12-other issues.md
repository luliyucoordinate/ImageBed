---
layout: post
title: other issues
category : cpp
tags : [cpp, stl]
stickie: true
---

当将元素加入容器中，容器必须分配更多的内存以足够保存这些元素，于是他们向他的模板参数allocator发出申请，该模板参数往往被另一个名为 allocator_type。甚至将chars添加到string class也是如此，因为string也算是一个正规的STL容器。每个元素类型为T的容器的Allocator模板默认为allocator<T>。其接口只有大约20个public申明，包括嵌套的typedefs和成员函数。最重要的两个成员函数是：

```c++
T* allocate(size_type n, const void* hint = 0);
Void deallocate(T* p, size_type n);
```
N指的是客户申请的元素个数，不是指空间总量。这些空间是通过调用::operator new获得，但何时需要并无具体指定。  

最容易满足需求的做法就是每当容器需要内存就调用operator new，每当容器释放内存就调用operator delete。这种做法比起分配大块内存并缓存然后小块小块的使用当然较慢，优势则是可以在极大范围的硬件和操作系统有效运作。

```c++
__gnu_cxx::new_allocator
```
实现出简洁的operator new 和operator delete。

```c++
__gnu_cxx::malloc_allocator
```
实现上例唯一不同的是，它使用c函数std::malloc和std::free  

另外一种做法就是使用智能型allocator，将分配所得的内存加以缓存。这种额外机制可以数种形式呈现：可以是个bitmap index，用以索引至一个以2的指数倍成长的篮子。也可以是个相较之下比较简易的fixed-size pooling cache这里所说的cache被程序内的所有容器共享，而operators new和operator delete不经常
被调用，这可带来速度上的优势。使用这个技巧的allocators包括：

```c++
__gnu_cxx::bitmap_allocator
```
一个高效能的allocator，使用bit-map追踪被使用和未使用的内存块。

```c++
__gnu_cxx::pool_allocator
__gnu_cxx::__mt_alloc
```

Class allocator 只拥有typedef,constructor,和rebind等成员。它继承自一个high-speed extension allocators。也因此，所有分配器和归还都取决于该base class，而这个base class也许是终端用户无法碰触和操控的。很难挑选出某个分配策略说他可以提供最大共同利益而不至于令某些行为过度优势。事实上，就算要挑选何种典型动作以测量速度，都是一种困难。  
GNU C++提供三项综合测试用以C++allocators之间的速度比较：  
Insertion进过多次iterations后各种STL容器将拥有某个极大量。分别测试sequence和associative容器。多线程环境中的insertion and erasure 。这个测试展示allocator归还内存，测量线程之间对内存的竞争。A threaded producer/consumer model分别测试sequence和associative容器。

另外两个智能allocator：  
__gnu_cxx::debug_allocator  
这个是一个外覆器(wrapper)，可包含于任何allocator之上。他把客户的申请量添加一些，然后由allocator回应，并以那个一小块额外内存放置size信息。一旦deallocate()收到一个pointer，就会检查size并以assert()保证吻合。  
__gnu_cxx::array_allocator  
允许分配一个已知固定大小的内存块，内存来自std::array objects。用上这个allocator，大小固定的容器就无需在调用::operator new 和::operator delete。这就允许我们使用STL abstractions而无需再运行期添加额外开销。甚至在program startup情况下也可使用。注意他是静态的，所以他不需要调用delete。

Array allocator
--
```c++
//array内的第二个参数表示array的大小
template<typename _Tp,typename _Array = std::tr1::array<_Tp,1>>
class array_allocator:public array_allocator_base<_Tp>
{
public:
	typedef size_t size_type;
	typedef _Tp value_type;
	typedef _Array array_type;
	...
private:
	array_type* _M_array;
	size_type _M_used;
public:
	array_allocator(array_type* __array = NULL)throw()
		:_M_array(__array), _M_used(size_type()){}
		...
	pointer
	allocate(size_type __n,const void* =0)
	{
		if(_M_array == 0|| _M_used + __n>_M_array > size())
			std::__throw_bad_alloc();
		pointer __ret = _M_array->begin() + _M_used();
		_M_used += __n;
		return __ret;
	}
};

debug_allocator
template<typename _Alloc>
class debug_allocator
{
...
private:
	size_type _M_extra;//额外的空间，记录整个区块的大小
	_Alloc _M_allocator;
	
	size_type _S_extra()
	{
		const size_t __obj_size = sizeof(value_type);
		return (sizeof(size_type) + __obj_size - 1)/__obj_size;
	}
public:
	debug_allocator(const _Alloc& __a)
		:_M_allocator(__a), _M_extra(_S_extra()){}
	pointer allocate(size_type __n)
	{
		pointer __res = _M_allocator.allocate(__n + __m_extra);
		size_type *__ps = reinterpret_cast<size_type*>(__res);
		*__ps = __n;
		return __res + _M_extra;
	}
	
	void deallocate(pointer __p,size_type __n)
	{
		using std::__throw_runtine_error;
		if(__p)
		{
			pointer __real_p = __p + _m_extra;
			if(*reinterpret_cast<size_type*>(__real_p) != __n)
				__throw_runtime_error
					("debug_allocator::deallocate wrong size");
			_M_allocator.deallocate(__ + _M_extra);
		}
		else
		{
			__throw_runtime_error
				("debug_allocator::deallocate wrong size");
		}
	}
};
```

bitmap_allocator
---
```c++
template<typename _Tp>
class bitmap_allocator:private free_list
{
public:
	pointer allocate(size_type __n)
	{
		if(__n > this->max_size())
			std::__throw_bad_alloc();
		if(__builtin_expect(__n == 1,true))
			return this->_M_allocate_single_object();
		else
		{
			const size_type __b = __n * sizeof(value_type);
			return reinterpret_cast<pointer>(::operator new(__b));
		}
	}
	void deallocate(pointer __p,size_type __n)throw()
	{
		if(__builtin_expect(__p !=0,true)
		{
			if(__builtin_expect(__n == 1,tue))
			{
				this->_M_delaoocate_single_object(__p);
			}
			else
				::operator delete(_p);
		}
	}
}; 
```
Vector的元素排列将以super block size为依据，新进者若大于最末者，便直接delete新进者，否则delete最末者后再insert新进者，若没有到达64则insert到适当位置。
