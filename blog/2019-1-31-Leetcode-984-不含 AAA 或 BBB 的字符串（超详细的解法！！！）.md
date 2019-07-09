---
layout: post
title: Leetcode 984：不含 AAA 或 BBB 的字符串（超详细的解法！！！）
category : 算法
tags : [python, c, c++]
stickie: true
date: 2019-1-31 00:00:00
---

给定两个整数 `A` 和 `B`，返回**任意**字符串 `S`，要求满足：

- `S` 的长度为 `A + B`，且正好包含 `A` 个 `'a'` 字母与 `B` 个 `'b'` 字母；
- 子串 `'aaa'` 没有出现在 `S` 中；
- 子串 `'bbb'` 没有出现在 `S` 中。

**示例 1：**

```
输入：A = 1, B = 2
输出："abb"
解释："abb", "bab" 和 "bba" 都是正确答案。
```

**示例 2：**

```
输入：A = 4, B = 1
输出："aabaa"
```

**提示：**

1. `0 <= A <= 100`
2. `0 <= B <= 100`
3. 对于给定的 `A` 和 `B`，保证存在满足要求的 `S`。

**解题思路**

这个问题非常简单（其实这是一个数学问题），我们首先想到的解法是贪心算法。我们可以分成如下几种情况去判断

- $A=B$
- $A > B​$
- $A < B$

第一种情况很简单，我们直接返回`'ab'*A`（或`'ab'*B`）即可。对于第二种和第三种情况，我们都按照第二种考虑，对于第三种情况我们交换`A,B`即可。接着我们判断当`A or B`不为空的时候，如果`A>B`的话，我们就添加`aab`，否则我们添加`ab`。

```python
class Solution:
    def strWithout3a3b(self, A, B, a='a', b='b'):
        """
        :type A: int
        :type B: int
        :rtype: str
        """
        if A == B:
            return (a+b)*B
        if B > A: 
            A, B = B, A
            a, b = b, a
        
        res = ''
        while A or B:
            if A: 
                res += a
                A -= 1
            if A > B:
                res += a
                A -= 1
            if B:
                res += b
                B -= 1
        
        return res
```

我们也可以继续优化这个问题，我们可以先计算`dif=abs(A-B)`。我们首先判断`dif`和`B`谁大？如果`B`更大的话，我们首先将`'aab'*(A-B)`添加到`res`中（因为此时`aa`的数量最多为`A-B`），然后再将`'ab'*(B*2-A)`添加到结果中，例如`A=4,B=3`，结果就是`aababab`。如果`dif>B`的话，我们首先将`'aab'*B`添加到`res`中（因为此时`aa`的数量最多为`B`，并且此时我们的`b`也用完了），然后再将`'a'*(A-2*B)`添加到结果中（题设中保证了我们一定会有结果，此时我们通过上面的策略一定是最优的，为什么？），例如`A=4,B=1`，结果就是`aabaa`。

```python
class Solution:
    def strWithout3a3b(self, A, B, a='a', b='b'):
        """
        :type A: int
        :type B: int
        :rtype: str
        """
        if A == B:
            return (a+b)*B
        
        if B > A: 
            A, B = B, A
            a, b = b, a
        if A >= B * 2: 
            return (a + a + b) * B + a * (A - B * 2)
        return (a + a + b) * (A - B) + (a + b) * (B * 2 - A)
```

这个问题使用递归的话，会更加简洁。递归的思路也非常简单，我们同样也只考虑三种情况，我们首先判断`A>B`，如果成立，我们返回`a*2+b+f(A-2,B-1)`，如果`A==B`，我们返回`(a+b)*A`，如果`A<B`的话，我们返回`f(B,A,b,a)`（也就是交换`A,B`顺序）。接着考虑边界情况，也就是`B==0`的话，我们只要返回`A*a`即可。

```python
class Solution:
    def strWithout3a3b(self, A, B, a='a', b='b'):
        """
        :type A: int
        :type B: int
        :rtype: str
        """
        if B > A: 
            return self.strWithout3a3b(B, A, b, a)
        if B == 0:
            return a*A
        if A > B:
            return (a*2+b)+self.strWithout3a3b(A-2, B-1, a, b)
        else:
            return (a+b)+self.strWithout3a3b(A-1, B-1, a, b)
```

reference:

https://leetcode.com/problems/string-without-aaa-or-bbb/discuss/226649/JavaC%2B%2B-(and-Python)-simple-greedy

**我将该问题的其他语言版本添加到了我的[GitHub Leetcode](https://github.com/luliyucoordinate/Leetcode)**

**如有问题，希望大家指出！！！**