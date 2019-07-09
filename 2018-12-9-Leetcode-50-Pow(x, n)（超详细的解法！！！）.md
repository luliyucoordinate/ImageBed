---
layout: post
title: Leetcode 50：Pow(x, n)（超详细的解法！！！）
category : 算法
tags : [python, c, c++]
stickie: true
date: 2018-12-9 00:00:00
---

实现 [pow(*x*, *n*)](https://www.cplusplus.com/reference/valarray/pow/) ，即计算 x 的 n 次幂函数。

**示例 1:**

```
输入: 2.00000, 10
输出: 1024.00000
```

**示例 2:**

```
输入: 2.10000, 3
输出: 9.26100
```

**示例 3:**

```
输入: 2.00000, -2
输出: 0.25000
解释: 2^{-2} = 1/2^2 = 1/4 = 0.25
```

**说明:**

- -100.0 < *x* < 100.0
- *n* 是 32 位有符号整数，其数值范围是 [$−2^{31}$, $2^{31} − 1$] 。

**解题思路**

我们首先想到的做法就是区分`n`是正数还是负数。如果是正数的话，我们就不断的乘`x`。如果是负数的话，我们就不断的除`x`。乘和除的次数都是`n`即可。

```python
class Solution:
    def myPow(self, x, n):
        """
        :type x: float
        :type n: int
        :rtype: float
        """
        res = 1.0
        for _ in range(abs(n)):
            if n > 0:
                res *= x
            else:
                res /= x
        return res
```

很显然问题没这么简单，我们提交结果超时了。当`n`非常大的时候我们乘积的次数太多了。这个问题我们很容易联想到之前的一个问题[Leetcode 29：两数相除（超详细的解法！！！）](https://blog.csdn.net/qq_17550379/article/details/84863011)。我们可以使用相同的思路，通过增量式的思路来处理。对于输入`x=3`和`n=1000`来说，可以变为

- $3^{1000} = 3^{2^9}*3^{2^8}*3^{2^7}*3^{2^6}*3^{2^5}*3^{2^3}$

现在我们的问题就变成了编程去实现这样的拆解。我们首先想到的做法就是先找到小于`1000`的`2`的最大幂指数`512`，接着我们继续找小于`1000-512=488`的`2`的最大幂指数`256`，以此类推。所以可以想到的思路就是建立一个`32`维的数组空间存放`2`的幂指数。

其实还有一种更好的办法，如果你观察到这样的规律话

<center class="half">
    <img src="https://raw.githubusercontent.com/wiki/luliyucoordinate/ImageBed/50/2018_12_10_1.png" width="200" hegiht="400">
</center>

观察每次数字是不是奇数，如果是奇数的话我们保留对应的`2`的幂次即可。

```python
class Solution:
    def myPow(self, x, n):
        """
        :type x: float
        :type n: int
        :rtype: float
        """
        m = -n if n < 0 else n
        p, q = 1, x
        while m > 0:
            if (m & 1) == 1:
                p *= q
            m //= 2
            q *= q
            
        return 1/p if n < 0 else p
```

对于这个问题通过递归来处理思路会更加清晰，我们定义函数$f(x,n)$返回$x^n$值，那么

- $f(x,n)=f(x,n/2)^2\ (n\ is\ even)$
- $f(x,n)=f(x,n/2)^2*x\ (n\ is\ odd)$

我们定义的上述函数只能处理`n`为正数的情况。对于边界问题，我们要分开考虑

- $n=0$
- $n=1$
- $n<0$

```python
class Solution:
    def myPow(self, x, n):
        """
        :type x: float
        :type n: int
        :rtype: float
        """
        if n == 0:
            return 1.0
        
        if n == 1:
            return x
        
        m = n // 2
        if n < 0:
            m = -m
            x = 1/x
            
        res = self.myPow(x, m)
        
        if (n & 1) == 0:
            return res * res
        return res * res * x
```

**我将该问题的其他语言版本添加到了我的[GitHub Leetcode](https://github.com/luliyucoordinate/Leetcode)**

**如有问题，希望大家指出！！！**