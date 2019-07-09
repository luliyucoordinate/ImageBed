---
layout: post
title: lvalue,rvalue,xlvalue,glvalue,prvalue
category : cpp
tags : [cpp, lvalue, rvalue, xlvalue, glvalue, prvalue]
stickie: true
---


Value categories
===

Each C++ expression (an operator with its operands, a literal, a variable name, etc.) is characterized by two independent properties: a type and a value category. Each expression has some non-reference type, and each expression belongs to exactly one of the three primary value categories: prvalue, xvalue, lvalue, defined as follows:
1.  a glvalue is an expression whose evaluation determines the identity of an object, bit-field, or function;
2.  a prvalue is an expression whose evaluation either
  1.  computes the value of the operand of an operator (such prvalue has no result object), or
  2.  initializes an object or a bit-field (such prvalue is said to have a result object). All class and array prvalues have a result object even if it is discarded. In certain contexts, temporary materialization occurs to create a temporary as the result object;
3.  an xvalue is a glvalue that denotes an object or bit-field whose resources can be reused;
4.  an lvalue is a glvalue that is not an xvalue;
5.  an rvalue is a prvalue or an xvalue.

Note: this taxonomy went through significant changes with past C++ standard revisions, see History below for details.

Primary categories
===

lvalue
---
The following expressions are lvalue expressions:
1.  the name of a variable or a function in scope, regardless of type, such as std::cin or std::endl. Even if the variable's type is rvalue reference, the expression consisting of its name is an lvalue expression;
2.  a function call or an overloaded operator expression of lvalue reference return type, such as std::getline(std::cin, str), std::cout << 1, str1 = str2, or ++it;
3.  a = b, a += b, a %= b, and all other built-in assignment and compound assignment expressions;
4.  ++a and --a, the built-in pre-increment and pre-decrement expressions;
5.  *p, the built-in indirection expression;
6.  a[n] and p[n], the built-in subscript expressions, except where a is an array rvalue (since C++11);
7.  a.m, the member of object expression, except where m is a member enumerator or a non-static member function, or where a is an rvalue and m is a non-static data member of non-reference type;
8.  p->m, the built-in member of pointer expression, except where m is a member enumerator or a non-static member function;
9.  a.*mp, the pointer to member of object expression, where a is an lvalue and mp is a pointer to data member;
10.  p->*mp, the built-in pointer to member of pointer expression, where mp is a pointer to data member;
11.  a, b, the built-in comma expression, where b is an lvalue;
12.  a ? b : c, the ternary conditional expression for some a, b, and c;
13.  a string literal, such as "Hello, world!";
14.  a cast expression to lvalue reference type, such as static_cast<int&>(x);
15.  a function call or an overloaded operator expression of rvalue reference to function return type;
16.  a cast expression to rvalue reference to function type, such as static_cast<void (&&)(int)>(x).
   (since C++11)

Properties:
1.  Same as glvalue (below).
2.  Address of an lvalue may be taken: &++i[1] and &std::endl are valid expressions.
3.  A modifiable lvalue may be used as the left-hand operand of the built-in assignment and compound assignment operators.
4.  An lvalue may be used to initialize an lvalue reference; this associates a new name with the object identified by the expression.

prvalue
---

The following expressions are prvalue expressions:
1.  a literal (except for string literal), such as 42, true or nullptr;
2.  a function call or an overloaded operator expression of non-reference return type, such as str.substr(1, 2), str1 + str2, or it++;
3.  a++ and a--, the built-in post-increment and post-decrement expressions;
4.  a + b, a % b, a & b, a << b, and all other built-in arithmetic expressions;
5.  a && b, a || b, !a, the built-in logical expressions;
6.  a < b, a == b, a >= b, and all other built-in comparison expressions;
7.  &a, the built-in address-of expression;
8.  a.m, the member of object expression, where m is a member enumerator or a non-static member function[2], or where a is an rvalue and m is a non-static data member of non-reference type (until C++11);
9.  p->m, the built-in member of pointer expression, where m is a member enumerator or a non-static member function[2];
10.  a.*mp, the pointer to member of object expression, where mp is a pointer to member function[2], or where a is an rvalue and mp is a pointer to data member (until C++11);
11.  p->*mp, the built-in pointer to member of pointer expression, where mp is a pointer to member function[2];
12.  a, b, the built-in comma expression, where b is an rvalue;
13.  a ? b : c, the ternary conditional expression for some a, b, and c;
14.  a cast expression to non-reference type, such as static_cast<double>(x), std::string{}, or (int)42;
15.  the this pointer;
16.  a lambda expression, such as [](int x){ return x * x; }.(since C++11)

Properties:
1.  Same as rvalue (below).
2.  A prvalue cannot be polymorphic: the dynamic type of the object it identifies is always the type of the expression.
3.  A non-class non-array prvalue cannot be cv-qualified. (Note: a function call or cast expression may result in a prvalue of non-class cv-qualified type, but the cv-qualifier is immediately stripped out.)
4.  A prvalue cannot have incomplete type (except for type void, see below, or when used in decltype specifier).

xvalue
---

The following expressions are xvalue expressions:
1.  a function call or an overloaded operator expression of rvalue reference to object return type, such as std::move(x);
2.  a[n], the built-in subscript expression, where one operand is an array rvalue ;
3.  a.m, the member of object expression, where a is an rvalue and m is a non-static data member of non-reference type;
4.  a.*mp, the pointer to member of object expression, where a is an rvalue and mp is a pointer to data member;
5.  a ? b : c, the ternary conditional expression for some a, b, and c;
6.  a cast expression to rvalue reference to object type, such as static_cast<char&&>(x);
7.  any expression that designates a temporary object, after temporary materialization.(since C++17)

Properties:
1.  Same as rvalue (below).
2.  Same as glvalue (below).

In particular, like all rvalues, xvalues bind to rvalue references, and like all glvalues, xvalues may be polymorphic, and non-class xvalues may be cv-qualified.

Mixed categories
===

glvalue
---

A glvalue expression is either lvalue or xvalue.
Properties:
1.  A glvalue may be implicitly converted to a prvalue with lvalue-to-rvalue, array-to-pointer, or function-to-pointer implicit conversion.
2.  A glvalue may be polymorphic: the dynamic type of the object it identifies is not necessarily the static type of the expression.
3.  A glvalue can have incomplete type, where permitted by the expression.

rvalue
---

An rvalue expression is either prvalue or xvalue.
Properties:
1.  Address of an rvalue may not be taken: &int(), &i++[3], &42, and &std::move(x) are invalid.
2.  An rvalue can't be used as the left-hand operand of the built-in assignment or compound assignment operators.
3.  An rvalue may be used to initialize a const lvalue reference, in which case the lifetime of the object identified by the rvalue is extended until the scope of the reference ends.
4.  An rvalue may be used to initialize an rvalue reference, in which case the lifetime of the object identified by the rvalue is extended until the scope of the reference ends.
5.  When used as a function argument and when two overloads of the function are available, one taking rvalue reference parameter and the other taking lvalue reference to const parameter, an rvalue binds to the rvalue reference overload (thus, if both copy and move constructors are available, an rvalue argument invokes the move constructor, and likewise with copy and move assignment operators).

```c++
struct S {
    S () = default ;
    S (const S &) = delete ;
    S &operator= (const S &) = delete ;
    S (S &&) = default ;
    S &operator= (S &&) = default ;
} ;

struct A {
    S p0 ;
    S p1[2] ;
} ;

int main () {
    S p0 = A ().p0 ;
    S p1 = A ().p1[0] ;
    return 0 ;
}
```
p1哪里是编译不通过的，A ().p1[0]不是右值  
好像不满足xvalue的描述  

A().p1[0] 的意思是（实际上也是这么运作的）先计算A().p1（这是一个lvalue，而不是xvalue，因为 3）的要求是m为非引用，当然也就是非指针了。 ）， 再取它的第1个元素（根据lvalue的性质，这当然也是一个左值了）。  
一言以蔽之，A().p1[0] 的运算顺序是(A().p1)[0]，是一个lvalue，而不是xvalue（在C++11中）。   
PS： ‘.’的优先级和[]一样，因此，从左到右计算。
