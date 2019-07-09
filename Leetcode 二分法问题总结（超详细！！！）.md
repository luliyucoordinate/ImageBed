---
layout: post
title: Leetcode 二分法问题总结（超详细！！！）
category : 算法
tags : [python, c, c++]
stickie: true
date: 2019-1-19 00:00:00
---

# 0x00 循环不变式

初始化：它在循环的第一轮迭代开始之前，应该是正确的。

保持：如果在某一次循环迭代开始之前是正确的，那么在下一次迭代开始之前，它也应该保持正确（假设当循环变量等于k时符合，再看执行一遍循环体后是否还符合循环不变式）。

终止：循环能够终止，并且可以得到期望的结果。（这一步是和数学归纳法不同的一点，用循环不变式则更进一步，数学归纳法到这里就得出了一个关系式就结束，而用循环不变式，不但要先确保一个正确的关系式，还要看最后循环结束时，循环变量最后等于多少，根据循环不变式推导是否符合自己的要求。）。

只要保障上述三者成立，那么这个循环就是正确的。下列问题全部是在输入数组是升序的情况下讨论。

# 0x01 准确查找问题

区间为`[a, b)`类型。

初始化：我们假设都给定了正确类型的`nums`和`target`。

保持：当`nums[mid] == target`的时候，显然我们找到了`target`，我们直接返回`mid`即可。当`target > nums[mid]`的时候，此时`[l, mid]`中的元素全部小于`target`，此时`target`只会存在于`[mid+1, r)`这个区间中。当`target < nums[mid]`的时候，此时`[mid, r)`这个区间内的元素全部大于`target`，此时`target`只会存在于`[l, mid-1]`区间内，此时为了保障区间类型的统一，我们将`[l, mid-1]`变成`[l, mid)`。

终止：当`l==r`，此时区间`[l, r)`中没有元素了，那么`target`就不在`nums`中。

```python
class Solution:
    def find(self, nums, target):
        """
        :type nums: List[int]
        :type target: int 
        :rtype: int
        """
        l, r = 0, len(nums)
        while l < r:
            mid = (l + r)//2
            if target == nums[mid]:
                return mid
            elif target > nums[mid]:
                l = mid + 1
            else:
                r = mid
        return -1
```

区间为`[a, b]`类型

初始化：我们假设都给定了正确类型的`nums`和`target`。

保持：当`nums[mid] == target`的时候，显然我们找到了`target`，我们直接返回`mid`即可。当`target > nums[mid]`的时候，此时`[l, mid]`中的元素全部小于`target`，此时`target`只会存在于`[mid+1, r]`这个区间中。当`target < nums[mid]`的时候，此时`[mid, r]`这个区间内的元素全部大于`target`，此时`target`只会存在于`[l, mid-1]`区间内。

终止：当`l > r`，此时区间`[l, r]`中没有元素了，那么`target`就不在`nums`中。

```python
class Solution:
    def find(self, nums, target):
        """
        :type nums: List[int]
        :type target: int 
        :rtype: int
        """
        l, r = 0, len(nums) - 1
        while l <= r:
            mid = (l + r)//2
            if target == nums[mid]:
                return mid
            elif target > nums[mid]:
                l = mid + 1
            else:
                r = mid - 1
        return -1
```

对于后面的问题，我们都按照`[a, b]`这种区间类型分析。

# 0x02 lower_bound & upper_bound问题

<center class="half">
    <img src="http://wx1.sinaimg.cn/mw690/af2d2659ly1fzbytt8md5j207706xt8l.jpg" width="200">
</center>

`lower_bound`回答的问题：在一个有序数组`arr`中, 寻找大于等于`target`的元素的第一个索引，如果存在, 则返回相应的索引`index`，否则, 返回`arr`的元素个数 `n`。

保持：当`nums[mid] == target`的时候，显然我们找到了`target`，但是我们需要找的是**第一个**大于等于`target`的元素，所以我们需要在`[l, mid-1]`中继续寻找。当`target > nums[mid]`的时候，此时`[l, mid]`中的元素全部小于`target`，此时大于等于`target`的元素只会存在于`[mid+1, r]`这个区间中。当`target < nums[mid]`的时候，此时`[mid, r]`这个区间内的元素一定大于`target`，此时`target`只会存在于`[l, mid-1]`这个区间内。

终止：当`l>r`，此时区间`[l, r]`中没有元素了，而`l`是大于等于`target`的第一个位置（很容易分析，假设`l==r`的时候`target == nums[mid]`，此时`r=mid-1`而`l=mid`）。

相关问题：

[Leetcode 35：搜索插入位置（最详细的解法！！！）](https://blog.csdn.net/qq_17550379/article/details/83036528)

```python
class Solution:
    def lower_bound(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        l, r = 0, len(nums)-1
        while l <= r:
            mid = (l + r)//2
            if target <= nums[mid]:
                r = mid - 1
            else:
                l = mid + 1
        return l
```

`upper_bound`回答的问题：在一个有序数组`arr`中, 寻找大于`target`的元素的第一个索引，如果存在, 则返回相应的索引`index`，否则, 返回`arr`的元素个数 `n`。

初始化：我们假设都给定了正确类型的`nums`和`target`。

保持：当`nums[mid] == target`的时候，显然我们找到了`target`，但是我们需要找的是**第一个**大于`target`的元素，所以我们需要在`[mid+1, r]`中继续寻找。当`target > nums[mid]`的时候，此时`[l, mid]`中的元素全部小于`target`，此时大于等于`target`的元素只会存在于`[mid+1, r]`这个区间中。当`target < nums[mid]`的时候，此时`[mid, r]`这个区间内的元素一定大于`target`，此时`target`只会存在于`[l, mid]`这个区间内。

终止：当`l>r`，此时区间`[l, r]`中没有元素了，而`l`是大于`target`的第一个位置（分析同上）。

```python
class Solution:
    def lower_bound(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        l, r = 0, len(nums)-1
        while l <= r:
            mid = (l + r)//2
            if target >= nums[mid]:
                l = mid + 1
            else:
                r = mid - 1
        return l
```

# 0x03 floor & ceil 问题

<center class="half">
    <img src="http://wx3.sinaimg.cn/mw690/af2d2659ly1fzbytr0dpqj207g0703yf.jpg" width="200">
</center>

`floor`回答的问题：如果找到`target`，返回第一个`target`相应的索引`index`；如果没有找到`target`, 返回比`target`小的最大值相应的索引， 如果这个最大值有多个， 返回最大索引；如果这个`target`比整个数组的最小元素值还要小, 则不存在这个`target`的`floor`值, 返回`-1`。

其实这就是一个`upper_bound`问题，我们最后只要判断`target==nums[l]`（需要保证`l<len(nums)`），如果成立返回`l`，否则返回`l-1`。

相关问题：

[Leetcode 34：在排序数组中查找元素的第一个位置和最后一个位置（最详细的解法！！！）](https://blog.csdn.net/qq_17550379/article/details/83214428)

```python
class Solution:
    def floor(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        l, r = 0, len(nums)-1
        while l <= r:
            mid = (l + r)//2
            if target <= nums[mid]:
                r = mid - 1
            else:
                l = mid + 1
                
        if l < len(nums) and nums[l] == target:
            return l
        
        return l-1
```

`ceil`回答的问题：如果找到`target`，返回最后一个`target`相应的索引`index`；如果没有找到`target`，返回比`target`大的最小值相应的索引，如果这个最小值有多个，返回最小的索引；如果这个`target`比整个数组的最大元素值还要大，则不存在这个`target`的`ceil`值, 返回整个数组元素个数`n`。

其实这就是一个`upper_bound`问题，我们最后只要判断`target==nums[l-1]`，如果成立返回`l-1`，否则返回`l`（需要保证`l<len(nums)`）。

相关问题：

[Leetcode 34：在排序数组中查找元素的第一个位置和最后一个位置（最详细的解法！！！）](https://blog.csdn.net/qq_17550379/article/details/83214428)

```python
class Solution:
    def ceil(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        l, r = 0, len(nums)-1
        while l <= r:
            mid = (l + r)//2
            if target >= nums[mid]:
                l = mid + 1
            else:
                r = mid - 1
                
        if nums[l-1] == target:
            return l-1
        if l < len(nums):
            return l
        return -1
```

其实很多变种问题都是通过`lower_bound`和`upper_bound`变化而来，所以一定要先理解基础问题。

# 0x04 python 中的库

```python
import bisect
def index(a, x):
    'Locate the leftmost value exactly equal to x'
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    raise ValueError

def find_lt(a, x):
    'Find rightmost value less than x'
    i = bisect_left(a, x)
    if i:
        return a[i-1]
    raise ValueError

def find_le(a, x):
    'Find rightmost value less than or equal to x'
    i = bisect_right(a, x)
    if i:
        return a[i-1]
    raise ValueError

def find_gt(a, x):
    'Find leftmost value greater than x'
    i = bisect_right(a, x)
    if i != len(a):
        return a[i]
    raise ValueError

def find_ge(a, x):
    'Find leftmost item greater than or equal to x'
    i = bisect_left(a, x)
    if i != len(a):
        return a[i]
    raise ValueError
```

# 0x05 cpp中的库

```cpp
std::vector<int> data = { 1, 1, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 6 };
auto lower = std::lower_bound(data.begin(), data.end(), 4);
auto upper = std::upper_bound(data.begin(), data.end(), 4);
```

**我将该问题的其他语言版本添加到了我的[GitHub Leetcode](https://github.com/luliyucoordinate/Leetcode)**

**如有问题，希望大家指出！！！**

reference:

http://www.cnblogs.com/wuyuegb2312/archive/2013/05/26/3090369.html

https://github.com/liuyubobobo/Play-with-Algorithms

https://blog.csdn.net/mountzf/article/details/51866342

https://segmentfault.com/a/1190000016825704

https://docs.python.org/3/library/bisect.html

https://zh.cppreference.com/w/cpp/algorithm/lower_bound

https://zh.cppreference.com/w/cpp/algorithm/upper_bound