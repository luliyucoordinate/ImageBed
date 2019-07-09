---
layout: post
title: Leetcode 325：Maximum Size Subarray Sum Equals k（超详细的解法！！！）
category : 算法
tags : [python, c, c++]
stickie: true
date: 2019-1-13 00:00:00
---

Given an array nums and a target value k, find the maximum length of a subarray that sums to k. If there isn't one, return 0 instead.

**Example 1:**

```
Given nums = [1, -1, 5, -2, 3], k = 3,
return 4. (because the subarray [1, -1, 5, -2] sums to 3 and is the longest)
```

**Example 2:**

```
Given nums = [-2, -1, 2, 1], k = 1,
return 2. (because the subarray [-1, 2] sums to 1 and is the longest)
```

**Follow Up:**

```
Can you do it in O(n) time?
```

**解题思路**

首先想到的做法就是建立累加和数组，和之前的问题[Leetcode 303:区域和检索-数组不可变（超详细解决方案！！！）](https://blog.csdn.net/qq_17550379/article/details/86418490)类似。先建立累加和数组，然后在计算不同区间的差值，比较差值结果是不是`k`，最后记录差值最大的结果即可。

```python
from itertools import accumulate
class Solution:
    def maxSubArrayLen(self, nums, k):
        """
        :type nums: list
        :type k: int
        :rtype: int
        """
        pre_sum = [0]+list(accumulate(nums))
        res = 0
        for i in range(len(pre_sum)):
            for j in range(i, len(pre_sum)):
                if pre_sum[j] - pre_sum[i] == k:
                    res = max(res, j - i)
        return res
```

但是上面这种解法是`O(n^2)`的解法，有没有更快的？可以使用类似于[Leetcode 1:两数之和（最详细解决方案！！！）](https://blog.csdn.net/qq_17550379/article/details/80435039)中的策略，通过建立字典存储`pre_sum`和对应的位置`i`，然后计算当前累加和`k`的差`pre_sum[i]-k`，判断是不是在字典中即可，如果在的话我们就计算长度。这里有一点要注意的是，我们在记录位置`i`的过程中，只记录第一次出现的位置，因为我们需要求的是最大长度。

```python
from itertools import accumulate
class Solution:
    def maxSubArrayLen(self, nums, k):
        """
        :type nums: list
        :type k: int
        :rtype: int
        """
        pre_sum = list(accumulate(nums))
        res, dic = 0, dict()

        for i in range(len(pre_sum)):
            if pre_sum[i] == k:
                res = i + 1
            elif pre_sum[i] - k in dic:
                res = max(res, i - dic[pre_sum[i] - k])
            if pre_sum[i] not in dic:
                dic[pre_sum[i]] = i

        return res
```

我们可以对这个代码继续优化，也就是将累加操作放到循环中去。

```python
class Solution:
    def maxSubArrayLen(self, nums, k):
        """
        :type nums: list
        :type k: int
        :rtype: int
        """
        pre_sum, res = 0, 0
        dic = dict()

        for i in range(len(nums)):
            pre_sum += nums[i]
            if pre_sum == k:
                res = i + 1
            elif pre_sum - k in dic:
                res = max(res, i - dic[pre_sum - k])
            if pre_sum not in dic:
                dic[pre_sum] = i

        return res
```

**我将该问题的其他语言版本添加到了我的[GitHub Leetcode](https://github.com/luliyucoordinate/Leetcode)**

**如有问题，希望大家指出！！！**