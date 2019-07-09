---
layout: post
title: 理解std::move和std::forward
category : cpp
tags : [cpp, 转载, move, forward]
stickie: true
---

转自[Effective Modern C++ 条款23 理解std::move和std::forward](http://blog.csdn.net/big_yellow_duck/article/details/52371164)

首先我要提一下右值与左值，我觉得本书中的一句话说的非常好：

A useful heuristic to determine whether an expression is an lvalue is to ask if you can take its address. If you can, it typically is. If you can’t, it’s usually an rvalue. A nice feature of this heuristic is that it helps you remember that the type of an expression is independent of whether the expression is an lvalue or an rvalue. That is, given a type T, you can have lvalues of type T as well as rvalues of type T. It’s especially important to remember this when dealing with a parameter of rvalue reference type, because the parameter itself is an lvalue:

有效了解std::move和std::forward的方法是，了解它们做不了的事情。std::move不会移动任何东西，std::forward不会转发任何东西，在运行期间，它们什么事情都不会做，不会生成一个字节的可执行代码。

std::move和std::forward仅仅是表现为转换类型的函数（实际上是模板函数），std::move无条件地把参数转换为右值，而std::forward在满足条件下才会执行std::move的转换。这个说明导致了一系列问题，但是从根本上，那是一个完整的故事。

为了让故事更具体，这里是C++11的std::move的简单实现，它没有完全覆盖标准库的细节，不过很接近了。

```c++
template <typename T>              // 在std命名空间里`
typename remove_reference<T>::type&&
move(T&& param)
{
    using ReturnType = typename remove_reference<T>::type&&;
    return static_cast<ReturnType>(param);
}
```
其实函数的本质就是类型转换，就如你所见，std::move接收一个对象的引用（准确地说，是通用引用，具体看条款24），然后返回相同对象的引用。

返回类型中的“&&”暗示着std::move返回的是一个右值引用，不过，就像条款28讲述那样，如果T的类型是个左值引用，T&&将会变成左值引用。为了防止这种事发生，我们对T使用了remove_reference（去除引用语义），因此确保了使用“&&”的类型不是引用类型，那就保证了std::move返回的是右值引用，这是很重要的，因为函数返回的右值引用是右值。因此，std::move把参数转换为一个右值，那就是它做的全部事情。

说点题外话，std::move在c++14的实现就没那么夸张了，返回类型推断（看条款3）和标准库的别名模板std::remove_reference_t（看条款9），std::move可以这样写：

```c++
template <typename T>             // C++14，依然在std命名空间
decltype(auto) move(T&& param)
{
    using ReturnType = remove_reference_t<T>&&;
    return static_cast<ReturnType>(param);
}
```
是不是容易看多了？

因为std::move除了把参数转换为右值，没做其他事情，这表明类似rvalue_cast这样的名字或许更适合它。话虽如此，但我们用的名字是std::move，所以记住std::move做了什么和没做什么是重要的，它做的是转换，不是移动。

当然，右值会成为可移动的候选者，因此对一个对象使用std::move是告诉编译器，这个对象符合被移动的条件。那就是为什么std::move会有这个名字：很容易指出可能被移动的对象。

事实上，右值在通常情况下是唯一的可移动候选者。假如你要写一个代表注释的类，这个类的构造函数接受一个std::string参数（含有注释），然后把参数拷贝到成员变量，根据条款41，你声明的是值传递的参数：

```c++
class Annotation {
public:
    explicit Annotation(std::string text);        // 参数会被拷贝，值传递
    ...
};
```
不过因为注释类只是需要读text的值，不需要修改它，根据尽可能使用const这个悠久的历史，你修改了声明，把text修改成const：

```c++
class Annotation {
public:
    explicit Annotation(const std::string text);
    ...
};
```
为了避免拷贝text到成员变量的开销，你根据条款41的建议，对text使用std::move，由此产生一个右值：

```c++
class Annotation {
public:
    explicit Annotation(const std::string text)
    : value(std::move(text))  // 把text"移动"成右值
    { ... }                   // 但这代码的行为跟你看到的不一样
    ...
private:
    std::string value;
};
```
代码编译，链接，运行，把成员变量value设置为text的内容。唯一把这代码和你眼中的完美实现分离的事情是text不是被移动到value的，它只是被拷贝。当然，text被std::move转换为右值了，但是text是被声明为const std::string，所以在转换之前，text是一个const std::string左值，转换后，是一个const std::string右值，在整个过程中，const的性质是一支存在的。

当编译器选择std::string构造函数时，有两个可能：

```c++
class string {  // std::string实际上是std::basic_string<char>的typedef
public:
    ...
    string(const string& rhs);   //拷贝构造
    string(string&& rhs);     //移动构造
    ...
};
```
在Annotation构造函数的初始化列表中，std::move(text)的结果是一个类型为const std::string的右值，这个右值不能传递给std::string的移动构造函数，因为移动构造函数接受的是non-const std::string的右值引用。不过这右值，可以传递给拷贝构造函数，因为一个lvalue-reference-to-const（const的左值引用）可以绑定const右值。所以，成员初始化列表调用了std::string的拷贝构造函数，即使text被转换成右值！这种行为对于维护const的正确性是必不可少的。把一个值搬离对象通常都会改变这个对象，所以C++不允许把const对象传递给会改变它们（对象）的函数（例如移动构造）。

在这个例子中我们可以得到两个教训。第一，如果你想要有能力移动对象，不要把它们声明为const。向一个const对象请求移动操作会默默转换为拷贝操作。第二，std::move不仅不会移动东西，还不能保证转换出来的对象有被移动的资格。你唯一能确保的事情是：对一个对象使用std::move，那个对象就被转换为右值。

std::forward的故事就比std::move简单多了，不过std::move是无条件把参数转换为右值，而std::forward在特定情况下才会这样做。std::forward是个有条件的类型转换。为了理解它什么时候转换，回忆一下std::forward一般是怎样使用的。最常见用法是一个模板函数接受全局引用，然后用std::forward把参数传递给另一个函数：

```c++
void process(const Widget& lvalArg);    // 处理左值
void process(Widget&& rvalArg);         // 处理右值

template<typename T>
void logAndProcess(T&& param)      // 把参数传递给process的模板
{
     auto now = std::chrono::system_clock::now();   // 获取当前时间           

     makeLogEntry("Calling 'process'", now);
     process(std::forward<T>(param));
}
```
考虑logAndProcess的两次调用，一次左值，一次右值：

```c++
Widget w;

logAndProcess(w);             // 左值参数调用
logAndProcess(std::move(w));  // 右值参数调用
```
在logAndProcess里面，参数param被传递给process函数，而process函数为了左值参数和右值参数进行重载。当我们用左值调用logAndProcess的时候，我们自然是希望把左值转发给process，而当我们用右值调用logAndProcess时，我们希望调用的是右值重载的process。

但是param，和所有的函数参数一样，是个左值。在logAndProcess里每次调用process都会使用左值重载的process。为了防止这样的事情，我们需要一项技术，当且仅当初始化param的参数——即传递给logAndProcess的参数——是右值时，在logAndProcess把param转换为右值。这就是std::forward干的事情了，这也是为什么说std::forward是个有条件的类型转换：仅当参数是用右值初始化时，才会把它转换为右值。

你可能想要知道std::forward是如何知道参数是否用右值初始化的。举个例子，上面的代码中，std::forward是怎样知道初始化param的，是左值还是右值呢？简短的答案是信息会被编码到logAndProces的模板参数T中。这个参数传递给std::forward模板，然后恢复编码的信息。具体细节看条款28。

倘若把std::move和std::forward把归结为类型转换，那么它们的差别是std::move总是会转换，std::forward只会在某些时刻转换，你可以会问我们是否可以摒弃std::move，只是用std::forward。从纯粹的技术角度看，答案是可以的：std::forward可以应付所有场景，std::move不是必须的。当然，没有一个函数是真的必须的，因为我们可以自己写转换，不过如果那样的话，是很恶心的。

std::move吸引人的地方在于它的方便，减少可能的错误，还有更简洁。试想在一个类中，我们要记录移动构造函数被调用了多少次。我们所需要的是个static计数器，它在移动构造中递增。假如类中的非static成员变量只有一个std::string，这里有个十分方便的方法（即使用std::move）实现我们的移动构造：

```c++
class Widget {
public:
    Widget(Widget&& rhs)
    : s(std::move(rhs.s))
    { ++moveCtorCalls; }
    ...
private:
    static std::size_t moveCtorCalls;
    std::string s;
};
```
用std::forward实现相同的效果，代码是这样的：

```c++
class Widget {
public:
     Widget(Widget&& rhs)
     :s(std::forward<std::string>(rhs.s))
    { ++moveCtorCalls; }
    ...
};
```
首先要注意到的是std::move只需要一个函数参数（rhs.s），而std::forward既需要一个函数参数（rhs.s）又需要一个模板类型参数（std::string）。然后需要注意的是我们一般传递给std::forward的参数类型是不带引用的，那是因为这会很方便把参数编码成右值（看条款28）。结合起来，意味着std::move比起std::forward需要更少的类型，不用传递类型参数可以减少编码的麻烦。它还可以消除我们可能传递的类型错误（例如，std::string&， 使用std::forward的话，会导致成员变量拷贝构造，而不是移动构造，具体原因可以看这篇[理解引用折叠](http://www.coordinate.wang/cpp/2017/07/08/%E7%90%86%E8%A7%A3%E5%BC%95%E7%94%A8%E6%8A%98%E5%8F%A0.html)）。

最重要的是，std::move是无条件转换，而std::forward只会将绑在右值上的参数转换为右值。这两个操作不一样，第一个操作通常会造成移动，而第二个操作只是传递——转发——一个对象给另一个函数，而保持原来的左值性质或者右值性质。因为这两个行为是不一样的，所以用两个不同的函数（和函数名）区分它们是很好的设计。

总结
===
需要记住的3点：

1.  std::move表现为无条件的右值转换，就其本身而已，它不会移动任何东西。
2.  std::forward仅当参数被右值绑定时，才会把参数转换为右值。
3.  std::move和std::forward在运行时不做任何事情。