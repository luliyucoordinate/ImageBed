---
layout: post
title: Leetcode 240：搜索二维矩阵 II（超详细的解法！！！）
category : 算法
tags : [python, c, c++]
stickie: true
date: 2019-3-8 00:00:00
---

编写一个高效的算法来搜索 *m* x *n* 矩阵 matrix 中的一个目标值 target。该矩阵具有以下特性：

- 每行的元素从左到右升序排列。
- 每列的元素从上到下升序排列。

**示例:**

现有矩阵 matrix 如下：

```
[
  [1,   4,  7, 11, 15],
  [2,   5,  8, 12, 19],
  [3,   6,  9, 16, 22],
  [10, 13, 14, 17, 24],
  [18, 21, 23, 26, 30]
]
```

给定 target = `5`，返回 `true`。

给定 target = `20`，返回 `false`。

**解题思路**

这个问题和之前的问题[Leetcode 74：搜索二维矩阵（最详细的解法！！！）](https://blog.csdn.net/qq_17550379/article/details/83306381)类似，都是二分法的变种问题。那么这个问题该怎么做呢？其实很容易想到，我们看**左下角的那个点**，这个点有什么性质？它大于上面的所有点，并且小于右边的所有点。┗|｀O′|┛ 嗷~~这不就是中心点吗？问题就很容易了

我们每次遍历都和最下角的点判断大小是不是为`target`，如果是的话返回`True`；如果小于`target`，那么我们很明显要到上面的行找；如果大于`target`的话，我们就需要到右边的列找。

```python
class Solution:
    def searchMatrix(self, matrix, target):
        """
        :type matrix: List[List[int]]
        :type target: int
        :rtype: bool
        """
        if not matrix:
            return False
        r, c = len(matrix), len(matrix[0])
        i, j = r-1, 0
        while i >= 0 and j < c:
            if matrix[i][j] == target:
                return True
            elif matrix[i][j] < target:
                j += 1
            else:
                i -= 1
        return False
```

**我将该问题的其他语言版本添加到了我的[GitHub Leetcode](https://github.com/luliyucoordinate/Leetcode)**

**如有问题，希望大家指出！！！**