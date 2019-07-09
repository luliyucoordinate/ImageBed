---
layout: post
title: Leetcode 253：Meeting Rooms II（超详细的解法！！！）
category : 算法
tags : [python, c, c++]
stickie: true
date: 2019-6-23 00:00:00
---

Given an array of meeting time intervals consisting of start and end times `[[s1,e1],[s2,e2],...] (si < ei)`, find the minimum number of conference rooms required.

For example,

```
Given [[0, 30],[5, 10],[15, 20]],
return 2.
```

**解题思路**

这个问题有一个非常简单的处理思路，我们可以先将上述的区间在坐标轴上画好，然后通过垂直于`x`轴的线从左向右移动，移动的过程中，记录这根线和区间相交的最大交点个数，这个最大交点个数就是相交的最大区间个数。

<center class="half">
    <img src="https://raw.githubusercontent.com/wiki/luliyucoordinate/ImageBed/253/2019_6_23_1.png" width="300">
</center>

算法的实现上我们有一个`trick`，我们遍历`intervals`中的每一项`it`，然后对于左边的坐标用`[it[0], 1]`表示（表示我们进入一个线段），右边的坐标用`[it[1], -1]`表示（表示我们退出了一个线段），然后将这些新得到的区间加入到一个`tmp`数组中，对这个数组排序，接着遍历这个数组，遍历的过程中累加我们建立的标记位（也就是前面建立的`1`和`-1`）记录累加的最大值即可。


```python
class Solution:
    def minMeetingRooms(self, intervals):
        if not intervals:
            return 0
        tmp = sorted(x for i, j in intervals for x in [[i, 1], [j, -1]])
        res, n = 0, 0
        for i, v in tmp:
            n += v
            res = max(res, n)
        return res
```

**我将该问题的其他语言版本添加到了我的[GitHub Leetcode](https://github.com/luliyucoordinate/Leetcode)**

**如有问题，希望大家指出！！！**