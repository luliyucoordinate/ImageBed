---
layout: post
title: Aggregate和POD类型
category : cpp
tags : [cpp, Aggregate, POD]
stickie: true
---


A plain old data structure (POD) is a data structure that is represented only as passive collections of field values, without using encapsulation or other object-oriented features.  
POD是这样的数据结构：用组个field的集合来表示，没有使用封装或者其他面向对象的features。  
A POD type in C++ is defined as either a scalar type or a POD class. A POD class has no user-defined copy assignment operator, no user-defined destructor, and no non-static data members that are not themselves PODs. Moreover, a POD class must be an aggregate, meaning it has no user-declared constructors, no private nor protected non-static data, no base classes and no virtual functions. The standard includes statements about how PODs must behave in C++.  
In certain contexts, C++ allows only POD types to be used. For example, a union in C++98 cannot contain a class that has virtual functions or nontrivial constructors or destructors. This restriction is imposed because the compiler cannot determine which constructor or destructor should be called for a union. POD types can also be used for interfacing with C, which supports only PODs.  
在C++中，我们把传统的C风格的struct叫做POD（Plain Old Data）对象。一般来说，POD对象应该满足如下特性。  
对于POD类型T的对象，不管这个对象是否拥有类型T的有效值，如果将该对象的底层字节序列复制到一个字符数组（或者无符号字符数组）中，再将其复制回对象，那么该对象的值与原始值一样。考试就到对于任意的POD类型T，如果两个T指针分别指向两个不同的对象obj1和obj2，如果用memcpy库函数把obj1的值复制到obj2，那么obj2将拥有与obj1相同的值。  
简言之，针对POD对象，其二进制内容是可以随便复制的，在任何地方，只要其二进制内容在，就能还原出正确无误的POD对象。对于任何POD对象，都可以使用memset()函数或者其他类似的内存初始化函数。  

下面是转自[stackoverflow的一篇文章的译文](https://stackoverflow.com/questions/4178175/what-are-aggregates-and-pods-and-how-why-are-they-special)，比较详细介绍了aggregate 和 POD：  
这篇文章很长，如果Aggregates和PODs都想了解，就静下心来完整的把这篇文章读完，如果你仅仅对Aggregates感兴趣，读第一部分就可以了。如果你仅对PODs感兴趣，那你必须先读懂Aggregates的定义、含义和例子，然后再跳去读PODs，但是我依然推荐你完整的读完第一部分。Aggragates的概念是定义PODs的基础。  

什么是Aggragates，为什么他们这么特别？
---

C++标准（C++ 03 8.5.1 §1）中的正式定义：

```
一个Aggregate是一个数组或者一个没有用户声明构造函数，没有私有或保护类型的非静态数据成员，没有父类和虚函数的类型 
```
现在我们来分析这个定义。首先，数组是Aggregate。class也可以成为Aggregate如果满足…等等！我们还没有说struct和unions，它们可以成为Aggregate吗？是的，他们可以。在C++中，术语class是指所有的classes、structs和unios。所以，class（struct，union）只要满足上面定义中的条件就可以成为Aggregate。这些条件有什么含义呢？  
1.  这并不是说Aggregate类型就不能有构造函数，事实上，它可以拥有一个默认构造函数或者一个复制构造函数，只要他们是被编译器声明的，而不是被用户自己声明的。  
2.  不能拥有私有或者保护类型的非静态数据成员。你可以定义任意多的私有或者保护类型的成员方法（不包括构造函数）和静态类型的数据成员和方法，这都不违背Aggregate类型的规则。  
3.  Aggregate类型可以拥有用户声明的/用户定义的 赋值操作符或者析构函数
4.  数组是Aggregate类型，即便是非Aggregate类型元素的数组。

来看几个例子：  

```c++
class NotAggregate1
{
    virtual void f(){} //remember? no virtual functions
};

class NotAggregate2
{
 	int x; //x is private by default and non-static 
};

class NotAggregate3
{
public:
    NotAggregate3(int) {} //oops, user-defined constructor
};

class Aggregate1
{
public:
    NotAggregate1 member1;   //ok, public member
    Aggregate1& operator = (Aggregate1 const & rhs) {/* */} //ok, copy-assignment  
private:
   void f() {} // ok, just a private function

};
```

你已经理解了Aggregates含义了，现在我们来看为什么它这么特别。他们和非Aggregates类型不同，可以使用“{ }”初始化。这种初始化语法，在数组上很常见，而且，我们刚刚了解到数据就是Aggregates类型，所以，我们从数组开始：  

```c++
Type array_name[n] = {a1, a2, ..., am};

if(m == n) 
```
数组的第i个元素被初始化为ai  

```c++
else if(m < n)
```
数组前边的m个元素被初始化为a1, a2, ..., am，剩余的n-m个元素，如果可能，将按值初始化（下面有关于这个名词的解释）  

```c++
else if(m > n)
```
会引起编译错误

```c++
else（有可能为这种形式a[] = {1,2,3};）
```

数组的长度将被推测为m，所以int a[] = {1,2,3}等于a[3] = {1,2,3}   
标量类型的(bool,int,char,double,指针)对象是按值初始化（value-initialized）的，意思是指它被初始化为 0 （bool类型被初始化为false， double被初始化为0.0，等等）。有用户声明的默认构造函数的Class类型的对象按值初始化时，他的默认构造函数就会被调用。如果默认构造函数是被隐式定义的，那么所有的非静态类型成员变量将会递归地按值初始化。虽然这个定义并不精确，也不完全正确，但是可以让你有个基本的认识。最近我将会写一篇关于zero-initialization，value-initialization和default-initialization之间区别的文章。引用不能按值初始化。对于非Aggregate类型的class进行按值初始化有可能失败，比如在没有合适的默认构造函数的情形下。   
数组初始化的例子：

```c++
class A()
{
  	 A(int){} //no default constructor
};
class B()
{
   	B() {} //default constructor available
};
int main()
{
    A a1[3] = {A(2), A(1), A(14)}; //OK n == m
    A a2[3] = {A(2)}; //ERROR A没有默认构造函数. 不能按值初始化a2[1] 和 a2[2]
    B b1[3] = {B()}; //OK b1[1]和b1[2]使用默认构造函数按值初始化
    int Array1[1000] = {0}; //所有元素被初始化为0
    int Array2[1000] = {1}; //注意: 只有第一个元素被初始化为1，其他为0;
    bool Array3[1000] = {}; //大括号里可以为空，所有元素被初始化为false；
    int Array4[1000]; //没有被初始化. 这和空{}初始化不同；
    //这种情形下的元素没有按值初始化，他们的值是未知的，不确定的; 
    //(除非Array4是全局数据)
    int array[2] = {1,2,3,4}; //ERROR, 太多初始值
}
```
现在我们来看Aggregates类型是如何使用{ }初始化的。和上面非常类似，按照在类内部声明的顺序（按照定义都必须是public类型）初始化非静态类型的成员变量。如果初始值比成员少，那么其他的成员将按值初始化。如果有一个成员无法进行按值初始化，我们将会得到一个编译期错误。如果初始值比成员多，我们同样得到一个编译期错误。  

```c++
struct X{
    int i1;
 	int i2;
};
struct Y{
    char c;
 	X x;
 	int i[2];
    float f; 
protected:
 	static double d;
private:
    void g(){}      
}; 

Y y = {'a', {10,20}, {20,30}};
```
上面的例子中，y.c被初始化为’a’，y.x.i1被初始化为10，y.x.i2被初始化为20，y.i[0]为20，y.i[1]为30，y.f被按值初始化，也即是说，被初始化为0.0，保护类型的静态成员变量d不会被初始化，因为它是静态类型的。   
Aggregate类型的unions有所不同，使用{ }你可能只能初始化它们的第一个成员，我想如果你使用C++高级到考虑使用unions（使用他们非常危险，必须小心谨慎），你一定可以自己在C++标准中找到unions的规则。   
我们知道了Aggregates的特别之处，现在让我们来尝试理解一下它对类型的限制，也就是说为什么会有这些限制。我们应当理解使用{ }进行成员逐一初始化意味着这一类型只是成员的集合。如果有一个用户定义的构造函数，那意味着用户需要做一些额外的工作来初始化成员，因此使用{ }初始化是不正确的。如果出现了虚函数，那意味着这个类型（大多数实现）有一个指向vtable的指针，需要在构造函数内设置，所以使用{ }初始化是不够的。作为练习，你可以按照这种方式自己理解其他限制的含义。  
关于Aggregates的就这么多，现在我们可以更严格定义一个子类型PODs   

什么是PODs，为什么他们这么特别  
---

C++标准（C++ 03 9 §4）中正式的定义为：  

```
POD-struct类型是没有非静态类型的non-POD-struct，non-POD-union （或者这些类型的数组）和引用类型的数据成员，也没有用户定义的赋值操作符和析构函数的Aggregate类型的类。类似地，POD-union是没有非静态类型的non-POD-struct，non-POD-union （或者这些类型的数组）和引用类型的数据成员，也没有用户定义的赋值操作符和析构函数的Aggregate类型的联合。POD类型就是POD-struct和 a POD-union中的一种。   
```
Wow，这个定义更难解读，不是吗？让我们吧unions剥离出去，更清晰的复述为：  

```
POD类型就是没有非静态类型的non-POD类型 （或者这些类型的数组）和引用类型的数据成员，也没有用户定义的赋值操作符和析构函数的Aggregate类型。  
```
这个定义的有什么含义呢？（POD就是Plain Old Data）  

1.  所有的POD类型都是Aggregates类型，换句话说，如果不是aggregate类型，那么它一定不是POD类型。  
2.  类，和结构体一样可以为POD类型，因为标准中POD-struct这个术语包含了这两种情形。  
3.  和Aggregates类型一样，静态成员是什么类型则无关紧要  

例子：  

```c++
struct POD
{
 int x;
 char y;
 void f() {} //no harm if there's a function
 static std::vector<char> v; //static members do not matter
};

struct AggregateButNotPOD1
{
 int x;
 ~AggregateButNotPOD1(){} //user-defined destructor
};

struct AggregateButNotPOD2
{
 AggregateButNotPOD1 arrOfNonPod[3]; //array of non-POD class
};
```
1.  POD-classes，POD-unions，标量类型和这些类型的数组合成为POD类型，POD类型在很多方面都很特别，我来举几个例子：  
2.  POD类型是最接近于C语言中的结构体类型的。他们都没有改变对象的内存布局，但是，POD类型却可以有自己的成员函数和任意类型的静态成员。所以，如果你想写一个可在C甚至.net平台使用的可移植的动态库，你应该让暴露的所有的方法的返回值和参数都会POD类型。  
3.  非POD类型的对象的生命周期起始于构造函数，结束于析构函数调用完成。而POD类型对象的生命周期却起始于存储对象的空间被占用，结束于空间被释放或被重复利用。  
4.  对于POD类型的对象，C++标准保证当你使用memcpy将对象的内容拷贝到一个char类型或者unsigned char类型的数组中，在使用memcpy拷贝回来的时候，对象会保持不变。特别注意，非POD类型是无法保证这一点的。当然，你也可以安全的在对象之间拷贝POD类型。下面的这个例子假设T为POD类型  

```c++
#define N sizeof(T)
char buf[N];
T obj; // obj initialized to its original value
memcpy(buf, &obj, N); // between these two calls to memcpy,
// obj might be modified
memcpy(&obj, buf, N); // at this point, each subobject of obj of scalar type
// holds its original value
```
5.  goto 语句。你知道，使用goto从一个变量没有声明的点跳转到一个变量已经被声明的点是不合法的（编译器应该会有报错）。这个限制仅仅对非POD类型有效，下面这个例子f()是不合法的，而g()则是合法的。注意到微软的编译器对这条规则过于慷慨了，仅仅给出警告而已。  

```c++
int f() {
    struct NonPOD { NonPOD(){}};
    goto label;
    NonPOD x;
label:
  	return 0;
}

int g(){
    struct POD {int i;  char c;};
    goto label;
    POD x;
label:
  	return 0;
}
```

6.  C++标准保证POD类型的对象在内存起始处没有便宜。也就是说如果一个POD类型A的第一个成员为T，你可以安全的调用reinterpret_cast  从A*转换为T*,得到第一个成员的指针，反过来也成立。  

这个列表还很长很长…  

结论
---

理解POD类型非常重要，因为很多C++语言特性，就像你看到的，针对于他们都会有所不同。希望这篇文章对你有用。  
