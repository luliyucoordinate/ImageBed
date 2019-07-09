---
layout: post
title: Leetcode 927：Three Equal Parts（最详细的解法！！！）
category : 算法
tags : [python, c, c++]
stickie: true
date: 2018-10-31 00:00:00
---

Given an array `A` of `0`s and `1`s, divide the array into 3 non-empty parts such that all of these parts represent the same binary value.

If it is possible, return **any** `[i, j]` with `i+1 < j`, such that:

- `A[0], A[1], ..., A[i]` is the first part;
- `A[i+1], A[i+2], ..., A[j-1]` is the second part, and
- `A[j], A[j+1], ..., A[A.length - 1]` is the third part.
- All three parts have equal binary value.

If it is not possible, return `[-1, -1]`.

Note that the entire part is used when considering what binary value it represents.  For example, `[1,1,0]` represents `6` in decimal, not `3`.  Also, leading zeros are allowed, so `[0,1,1]` and `[1,1]` represent the same value.

**Example 1:**

```
Input: [1,0,1,0,1]
Output: [0,3]
```

**Example 2:**

```
Input: [1,1,0,1,1]
Output: [-1,-1]
```

**Note:**

1. `3 <= A.length <= 30000`
2. `A[i] == 0` or `A[i] == 1`

**解题思路**

我们首先想到的解法就是暴力破解，通过建立`i`和`j`两个指针，然后不断遍历`A`找到我们的区间。这样做的主要难点在于怎么判断`A[i]`和`A[j]`的关系。

```python
class Solution:
    def threeEqualParts(self, A):
        """
        :type A: List[int]
        :rtype: List[int]
        """
        i, j, x, y = 0, 2, -1, -1
        while j < len(A):
            l = ''.join(str(i) for i in A[0:i+1])
            m = ''.join(str(i) for i in A[i+1:j])
            r = ''.join(str(i) for i in A[j:])
            if self.theSame(l, m):
                if self.theSame(l, r):
                    x, y = i, j
                    break

            if self.less(l, m):
                i += 1
            else:
                j += 1
            
        return [x, y]

    def less(self, A, B):
        A = A.lstrip('0')
        B = B.lstrip('0')
        if len(A) == len(B):
            return A < B
        else:
            if len(A) > len(B):
                return False
            else:
                return True

    def theSame(self, A, B):
        A = A.lstrip('0')
        B = B.lstrip('0')
        return A == B
```

上面这个做法思路很清晰，但是看上去太烂了。有没有什么更好的方法呢？我们可以先统计`A`中的`1`的个数`ones`，如果不能被`3`整除，那么返回`[-1,-1]`，因为我们如果将`A`分成相等的三份，那么这三份包含`1`的个数一定是相同的。如果`ones==0`，我们返回`[0,len(A)-1]`（题目中没有提，应该是受数据约束）。接着我们看其他情况，现在问题就变得容易了许多，例如

```
1 0 1 0 1
i     j   
```

我们只要`[0,i]`这个区间内包含`ones/3`个`1`，`[i+1, j-1]`这个区间内包含`ones/3`个`1`，剩余区间内包含`ones/3`个`1`即可。最后我们只要判断这三个区间内的二进制数是否一致即可。

所以我们现在的问题就是`i`和`j`的位置。`i`在第一个`1`出现的位置，而`j`在第`ones/3+1`个`1`出现的位置。因为我们需要判断三个区间中的二进制数是否一致，所以我们需要第三个参数`k`，指向`ones*2/3+1`个`1`出现的位置。

现在我们只要判断`A[i]==A[j] and A[j]==A[k] `，并且每次`i++;j++;k++`，我们最后只要判断`k==len(A)`即可。例如

```
ones=18
1 1 1 0 1 0 0 1 0 1 0 0 1 1 1 0 1 0 0 1 0 1 0 0 0 0 1 1 1 0 1 0 0 1 0 1 0 0
i                       j                           k
```

然后不断判断`i`、`j`、`k`对应元素。

```
1 1 1 0 1 0 0 1 0 1 0 0 1 1 1 0 1 0 0 1 0 1 0 0 0 0 1 1 1 0 1 0 0 1 0 1 0 0
                        i                       j                           k
```

我们最后的返回区间就变成了`[i-1,j]`。

```python
class Solution:
    def threeEqualParts(self, A):
        """
        :type A: List[int]
        :rtype: List[int]
        """
        ones = A.count(1)
        i, j, k, x, y, A_len = 0, 0, 0, -1, -1, len(A)
        if not ones:
            return [0, A_len - 1]
        if ones%3 != 0:
            return [x, y]
        
        step1, step2 = ones//3+1, ones*2//3+1

        for p, num in enumerate(A):
            if num == 1:
                i = p
                break

        for p, num in enumerate(A):
            if num == 1:
                step1 -= 1
            if 0 == step1:
                j = p
                break

        for p, num in enumerate(A):
            if num == 1:
                step2 -= 1
            if 0 == step2:
                k = p
                break

        while k < A_len and A[i] == A[j] and A[j] == A[k]:
            i += 1
            j += 1
            k += 1

        if k == A_len:
            return [i-1,j]

        return [-1,-1]
```

我们可以将之写得更为简洁

```python
class Solution:
    def threeEqualParts(self, A):
        """
        :type A: List[int]
        :rtype: List[int]
        """
        ones = A.count(1)
        A_len = len(A)
        if not ones:
            return [0, A_len - 1]
        if ones%3 != 0:
            return [-1, -1]
        
        step = ones//3
        p, cnt = [0]*3, 0
        for i, num in enumerate(A):
            if num == 1:
                if cnt % step == 0:
                    p[cnt//step] = i
                cnt += 1

        while p[2] < A_len and A[p[0]] == A[p[1]] and A[p[1]] == A[p[2]]:
            p[0] += 1
            p[1] += 1
            p[2] += 1

        if p[2] == A_len:
            return [p[0]-1,p[1]]

        return [-1, -1]
```

但是速度上会慢上一些，有没有更好的写法呢？

reference:

https://leetcode.com/problems/three-equal-parts/discuss/183922/C++-O(n)-time-O(1)-space-12-ms-with-explanation-and-comments

**我将该问题的其他语言版本添加到了我的[GitHub Leetcode](https://github.com/luliyucoordinate/Leetcode)**

**如有问题，希望大家指出！！！**