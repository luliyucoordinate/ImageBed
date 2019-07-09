---
layout: post
title: Leetcode 69：Sqrt(x)（超详细的解法！！！）
category : 算法
tags : [python, c, c++]
stickie: true
date: 2018-12-11 00:00:00
---

实现 `int sqrt(int x)` 函数。

计算并返回 *x* 的平方根，其中 *x* 是非负整数。

由于返回类型是整数，结果只保留整数的部分，小数部分将被舍去。

**示例 1:**

```
输入: 4
输出: 2
```

**示例 2:**

```
输入: 8
输出: 2
说明: 8 的平方根是 2.82842..., 
     由于返回类型是整数，小数部分将被舍去。
```

**解题思路**

首先可以想到的最简单的处理思路就是遍历`[1,x]`的所有元素`i`，计算相应的平方值，如果大于`x`的话，我们返回`i-1`即可。

```python
class Solution:
    def mySqrt(self, x):
        """
        :type x: int
        :rtype: int
        """
        for i in range(x+1):
            if i**2 > x:
                return i - 1
        return x
```

但是这显然太过随意，时间复杂度太高。这个问题在数学上已经有很明确的解法了，就是大名鼎鼎的牛顿法。

首先，选择一个接近函数$f(x)$零点的$x_0$，计算相应的$f(x_0)$和切线斜率$f^{'}(x_0)$(这里$f^{'}$表示函数$f$的导数)。然后我们计算穿过点$(x_0,f(x_0))$并且斜率为$f^{'}(x_0)$的直线和$x$轴的交点$x$坐标，也就是求如下方程的解：

- $0=(x-x_0)*f^{'}(x_0)+f(x_0)$

我们将新求得的点的$x$坐标名为$x_1$，通常$x_1$会比$x_0$更接近方程$f(x)=0$的解。因此我们现在利用$x_1$开始下一轮迭代。迭代公式可以简化为下面表示：

- $x_{n+1}=x_n-\frac{f(x_n)}{f^{'}(x_n)}$

<center class="half">
    <img src="https://raw.githubusercontent.com/wiki/luliyucoordinate/ImageBed/69/2018_12_11_1.gif" width="400" hegiht="400">
</center>

对于本题我们要求解的就是$x^2=n$的解，也就是$f(x)=x^2-n$，对应的$f^{'}(x)=2x$。

- $x_{i+1}=x_i-\frac{x_i^2-n}{2x_i}=\frac{x_i^2+n}{2x_i}=\frac{x_i+\frac{n}{x_i}}{2}$

```python
class Solution:
    def mySqrt(self, x):
        """
        :type x: int
        :rtype: int
        """
        res = x
        while res**2 > x:
            res = (res + x//res)//2
            
        return res
```

reference:

https://zh.wikipedia.org/wiki/%E7%89%9B%E9%A1%BF%E6%B3%95

**我将该问题的其他语言版本添加到了我的[GitHub Leetcode](https://github.com/luliyucoordinate/Leetcode)**

**如有问题，希望大家指出！！！**