---
layout: post
title: ASP Eval、Execute、ExecuteGlobal区别分析
category : asp
tags : [asp, Eval, Execute, ExecuteGlobal]
stickie: true
---

Eval 计算一个表达式的值并返回结果。 

语法：[result = ]eval_r(expression_r) 

expression_r 为任意有效 VBScript 表达式的字符串 

示例： 

```asp
response.Write(eval_r("3+2")) '输出 5 
```
"3+2" 使用引号括起来，表示是一个字符串，但是在 Eval “眼里”，把它当作一个表达式 3+2 来执行。 



Execute 执行一个或多个指定的语句。多个语句间用冒号（:）隔开。 

语法：Execute statements 

示例： 

```asp
Execute "response.Write(""abc"")" '输出 abc 
```

"response.Write(""abc"")" 使用引号括起来，表示是一个字符串 

但是在 Execute “眼里”，把它当作一个语句 response.Write("abc") 来执行。 



ExecuteGlobal 在全局名字空间中执行一个或多个指定的语句。 

语法：ExecuteGlobal statement 

示例： 

```asp
dim c 
c = "全局变量" 
sub S1() 
dim c 
c = "局部变量" 
Execute "response.Write(c)" '输出 局部变量 
ExecuteGlobal "response.Write(c)" '输出 全局变量 
end sub 
Execute "response.Write(c)" '输出 全局变量 
call S1() 
```
变量 c 既在全局范围内定义，也在函数范围内定义，Execute 按自己所处的位置来决定使用局部变量还是全局变量，而 ExecuteGlobal 则始终只认全局范围的 c。

 
总结： 

1.  Eval　只执行一个语句　语句可以有也可以没有返回值 
2.  Execute 执行一个或多个语句　忽略语句的返回值 
3.  ExecuteGlobal 执行一个或多个语句　忽略语句的返回值　全局变量和局部变量同名时总是使用全局变量 

注意：

在 VBScript 中“赋值”与“比较”都是使用“=”，比如“a=b”既可以说是将 b 值赋予 a，也可以说是判断 a 与 b 是否相等，那么 eval_r("a=b") 是表示赋值还是比较运算呢？ 

这里有个约定，在 Eval 中，“a=b”总是表示比较运算，在 Execute 和 ExecuteGlobal 中，总是表示赋值。