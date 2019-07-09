---
layout: post
title: c++中的static member
category : cpp
tags : [cpp]
stickie: true
---

关于static member要注意的几个问题

- 静态数据成员仅仅在初始化时不受访问权限的约束

- 静态数据成员最好不要在.h文件中进行定义(初始化)，而是放在.cpp文件中定义(初始化)

   静态数据成员实际上是类域中的全局变量。所以，静态数据成员的定义(初始化)不应该被放在头文件中。 
    其定义方式与全局变量相同。举例如下： 

    xxx.h文件 

    ```c++
    class base
    { 
        private: 
            static const int _i; //声明，标准c++支持有序类型在类体中初始化,但vc6不支持。 
    }; 
    ```

    xxx.cpp文件 

    ```c++
    const int base::_i=10;//仅仅在定义(初始化)时不受private和protected访问限制. 
    ```

- 静态数据成员被类的所有对象所共享，包括类的派生类的所有对象，即派生类和基类共享一个静态成员

    ```c++
    class base
    { 
    	public : 
    		static int _num;         //声明 
    }; 
    int base::_num=0;                   //静态数据成员的真正定义 
    class derived:public base{ }; 
    main() 
    { 
        base a; 
        derived b; 
        a._num++;
        cout<<"base class static data number _num is"<<a._num<<endl; 
        b._num++; 
        cout<<"derived class static data number _num is"<<b._num<<endl; 
    } 
    // 结果为1,2;可见派生类与基类共用一个静态数据成员。
    ```

- 静态数据成员的类型可是所属类自己，即在一个类中可以声明该类自己的类型的静态成员对象，但是，不可以定义普通的成员对象(指针可以)

    ```c++
    class base{ 
    public : 
        static base _object1;    //正确，静态数据成员 
        base _object2;           //错误 
        base *pObject;           //正确，指针 
        base &mObject;           //正确，引用 
    };
    ```

    这个类要能创建对象，需要定义带有参数初始化列表的构造函数，如下：

    ```c++
    class base{ 
    public : 
        static base _object1; //正确，静态数据成员 
        base *pObject;            //正确，指针 
        base &mObject;         //正确，引用
        base():mObject(*this){}                
    };
    ```

- 在const成员函数中，可以修改static成员变量的值。普通成员变量的值，是不能修改的

    ```c++
    #include <iostream>
    using namespace std;

    class Student
    {
    private:
    	static int a;
    	int b;
    public:
        void change() const;
        void setB(int b);
        int getB();
        static int getA();
    };

    void Student::change() const
    {
        a++;          //这个可以，因为a是static成员变量。
        b++;          //不可以，因为b是普通成员变量(如果b不是成员变量(是全局变量，普通参数，函数内部定义的临时变量)也可以别修改)
    }
    int Student::getA()
    {
    	return a;
    }
    void Student::setB(int b)
    {
    	this->b = b;
    }
    int Student::getB()
    {
    	return b;
    }
    int Student::a = 5;

    int main(int argc,char *argv[])
    {
        Student stu;
        stu.setB(10);
        stu.change();
        cout<<Student::getA()<<endl; 
        cout<<stu.getB()<<endl;
        return 0;
    }
    ```
    这里我们要注意的是const放在函数后面，从本质上来说是修饰*this，也就是说这个对象本身是不可以被修改的，但是这里有一个例外就是上面提到的static member，我认为可以修改的原因是，static 变量是存储在这个类的外面的，而不是存储在这个类的内部，虽然它是一个内部变量

- static成员函数只能访问static成员，不能访问非static成员，并且static成员函数不能定义为virtual、const、volatile 函数