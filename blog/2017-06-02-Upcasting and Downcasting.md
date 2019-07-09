---
layout: post
title: Upcasting and Downcasting
category : cpp
tags : [cpp, 转载]
stickie: true
---


Upcasting
---
Upcasting is converting a derived-class reference or pointer to a base-class. In other words, upcasting allows us to treat a derived type as though it were its base type. It is always allowed for public inheritance, without an explicit type cast. This is a result of the is-a relationship between the base and derived classes.  
Here is the code dealing with shapes. We created Shape class, and derived Circle, Square, and Triangle classes from the Shape class. Then, we made a member function that talks to the base class:  

```c++
void play(Shape& s) 
{
   s.draw();
   s.move();
   s.shrink();
   ....
}
```
The function speaks to any Shape, so it is independent of the specific type of object that it's drawing, moving, and shrinking. If in some other part of the program we use the play( ) function like below:  

```c++
Circle c;
Triangle t;
Square sq;
play(c);
play(t);
play(sq);
```
Let's check what's happening here. A Triangle is being passed into a function that is expecting a Shape. Since a Triangle is a Shape, it can be treated as one by play(). That is, any message that play() can send to a Shape a Triangle can accept.  
Upcasting allows us to treat a derived type as though it were its base type. That's how we decouple ourselves from knowing about the exact type we are dealing with.  
Note that it doesn't say "If you're a Triangle, do this, if you're a Circle, do that, and so on." If we write that kind of code, which checks for all the possible types of a Shape, it will soon become a messy code, and we need to change it every time we add a new kind of Shape. Here, however, we just say "You're a Shape, I know you can move(), draw(), and shrink( ) yourself, do it, and take care of the details correctly."  
The compiler and runtime linker handle the details. If a member function is virtual, then when we send a message to an object, the object will do the right thing, even when upcasting is involved.  
Note that the most important aspect of inheritance is not that it provides member functions for the new class, however. It's the relationship expressed between the new class and the base class. This relationship can be summarized by saying, "The new class is a type of the existing class."

```c++
class Parent {
public:
  void sleep() {}
};

class Child: public Parent {
public:
  void gotoSchool(){}
};

int main( ) 
{ 
  Parent parent;
  Child child;

  // upcast - implicit type cast allowed
  Parent *pParent = &child; 

  // downcast - explicit type case required 
  Child *pChild =  (Child *) &parent;

  pParent -> sleep();
  pChild -> gotoSchool();
    
  return 0; 
}
```
A Child object is a Parent object in that it inherits all the data members and member functions of a Parent object. So, anything that we can do to a Parent object, we can do to a Child object. Therefore, a function designed to handle a Parent pointer (reference) can perform the same acts on a Child object without any problems. The same idea applies if we pass a pointer to an object as a function argument. Upcasting is transitive: if we derive a Child class from Parent, then Parent pointer (reference) can refer to a Parent or a Child object.  
Upcasting can cause object slicing when a derived class object is passed by value as a base class object, as in foo(Base derived_obj).

Downcasting
--

The opposite process, converting a base-class pointer (reference) to a derived-class pointer (reference) is called downcasting. Downcasting is not allowed without an explicit type cast. The reason for this restriction is that the is-a relationship is not, in most of the cases, symmetric. A derived class could add new data members, and the class member functions that used these data members wouldn't apply to the base class.
As in the example, we derived Child class from a Parent class, adding a member function, gotoSchool(). It wouldn't make sense to apply the gotoSchool() method to a Parent object. However, if implicit downcasting were allowed, we could accidentally assign the address of a Parent object to a pointer-to-Child

```c++
Child *pChild =  &parent; // actually this won't compile
        // error: cannot convert from 'Parent *' to 'Child *'
```
and use the pointer to invoke the gotoSchool() method as in the following line.

```c++
pChild -> gotoSchool();
```
Because a Parent isn't a Child (a Parent need not have a gotoSchool() method), the downcasting in the above line can lead to an unsafe operation.  
C++ provides a special explicit cast called dynamic_cast that performs this conversion. Downcasting is the opposite of the basic object-oriented rule, which states objects of a derived class, can always be assigned to variables of a base class.  
One more thing about the upcasting:   
Because implicit upcasting makes it possible for a base-class pointer (reference) to refer to a base-class object or a derived-class object, there is the need for dynamic binding. That's why we have virtual member functions.  
Pointer (Reference) type: known at compile time.  
Object type: not known until run time.  

Dynamic Casting
---

The dynamic_cast operator answers the question of whether we can safely assign the address of an object to a pointer of a particular type.  
Here is a similar example to the previous one.  

```c++
#include <string>

class Parent {
public:
  void sleep() {
  }
};

class Child: public Parent {
private:
  std::string classes[10];
public:
  void gotoSchool(){}
};

int main( ) 
{ 
  Parent *pParent = new Parent;
  Parent *pChild = new Child;
    
  Child *p1 = (Child *) pParent;  // #1
  Parent *p2 = (Child *) pChild;  // #2
  return 0; 
}
```
Let look at the lines where we do type cast.  

```c++
Child *p1 = (Child *) pParent;  // #1
Parent *p2 = (Child *) pChild;  // #2
```
Which of the type cast is safe?   
The only one guaranteed to be safe is the ones in which the pointer is the same type as the object or else a base type for the object.  
Type cast #1 is not safe because it assigns the address of a base-class object (Parent) to a derived class (Child) pointer. So, the code would expect the base-class object to have derived class properties such as gotoSchool() method, and that is false. Also, Child object, for example, has a member classes that a Parent object is lacking.  
Type case #2, however, is safe because it assigns the address of a derived-class object to a base-class pointer. In other words, public derivation promises that a Child object is also a Parent object.  
The question of whether a type conversion is safe is more useful than the question of what kind of object is pointed to. The usual reason for wanting to know the type is so that we can know if it's safe to invoke a particular method.  
Here is the syntax of dynamic_cast.  

```c++
Child *p = dynamic_cast<Child *>(pParent);
```
This code is asking whether the pointer pParent can be type cast safely to the type Child *.

It returns the address of the object, if it can.  
It returns 0, otherwise.  
How do we use the dynamic_cast?  

```c++
void f(Parent* p) {
  Child *ptr = dynamic_cast<Child*>(p);
   if(ptr) { 
    // we can safely use ptr
  } 
}
```
In the code, if (ptr) is of the type Child or else derived directly or indirectly from the type Child, the dynamic_cast converts the pointer p to a pointer of type Child. Otherwise, the expression evaluates to 0, the null pointer.  
In other words, we want to check if we can use the passed in pointer p before we do some operation on a child class object even though it's a pointer to base class.  
"The need for dynamic_cast generally arises because we want perform derived class operation on a derived class object, but we have only a pointer-or reference-to-base." -Scott Meyers
