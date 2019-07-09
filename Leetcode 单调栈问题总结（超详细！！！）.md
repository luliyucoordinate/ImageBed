---
layout: post
title: Leetcode 单调栈问题总结（超详细！！！）
category : 算法
tags : [python, c, c++]
stickie: true
date: 2019-1-16 00:00:00
---

# 0x00 

单调栈主要回答这样的几种问题

- 比当前元素更大的下一个元素
- 比当前元素更大的前一个元素
- 比当前元素更小的下一个元素
- 比当前元素更小的前一个元素

# 0x01 问题一

维护一个单调递减的栈。

[Leetcode 42：接雨水（超详细的解法！！！）](https://blog.csdn.net/qq_17550379/article/details/84945427)

[ Leetcode 496：下一个更大元素 I（超详细的解法！！！）](https://blog.csdn.net/qq_17550379/article/details/86501664)

[Leetcode 503：下一个更大元素 II（超详细的解法！！！）](https://blog.csdn.net/qq_17550379/article/details/86504595)

[Leetcode 739：每日温度（超详细的解法！！！）](https://blog.csdn.net/qq_17550379/article/details/86494645)

```python
class Solution:
    def nextGreaterElement(self, nums):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """
        stack = list()
        res = [-1]*len(nums)
        for i, n in enumerate(nums):
            while stack and nums[stack[-1]] < n:
                res[stack.pop()] = n
            stack.append(i)
        return res
```

# 0x02 问题二

维护一个单调递减的栈。

[Leetcode 901：股票价格跨度（超详细的解法！！！）](https://blog.csdn.net/qq_17550379/article/details/86498025)

[Leetcode 239：滑动窗口最大值（超详细的解法！！！）](https://blog.csdn.net/qq_17550379/article/details/88911870)(更明确为区间最大元素问题)

```python
class Solution:
    def preGreaterElement(self, nums):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """
        stack = list()
        res = [-1]*len(nums)
        for i, n in enumerate(nums):
            while stack and nums[stack[-1]] < n:
                stack.pop()
            if stack:
                res[i] = nums[stack[-1]]
            stack.append(i)
        return res
```

# 0x03 问题三

维护一个单调递增的栈。

[Leetcode 84：柱状图中最大的矩形（超详细的解法！！！）](https://blog.csdn.net/qq_17550379/article/details/85093224)

```python
class Solution:
    def nextSmallerElement(self, nums):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """
        stack = list()
        res = [-1]*len(nums)
        for i, n in enumerate(nums):
            while stack and nums[stack[-1]] > n:
                res[stack.pop()] = n
            stack.append(i)
        return res
```

# 0x04 问题四

维护一个单调递增的栈。

```python
class Solution:
    def preSmallerElement(self, nums):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """
        stack = list()
        res = [-1]*len(nums)
        for i, n in enumerate(nums):
            while stack and nums[stack[-1]] > n:
                stack.pop()
            if stack:
                res[i] = nums[stack[-1]]
            stack.append(i)
        return res
```

至于最后一点要说的就是，如何确定是使用`严格单调栈`还是`非严格单调栈`？**只要根据题意确定我们栈中是否可以存放相同元素即可。**

**我将该问题的其他语言版本添加到了我的[GitHub Leetcode](https://github.com/luliyucoordinate/Leetcode)**

**如有问题，希望大家指出！！！**