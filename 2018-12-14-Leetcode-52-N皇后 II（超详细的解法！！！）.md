---
layout: post
title: Leetcode 52：N皇后 II（超详细的解法！！！）
category : 算法
tags : [python, c, c++]
stickie: true
date: 2018-12-14 00:00:00
---

*n* 皇后问题研究的是如何将 *n* 个皇后放置在 *n*×*n* 的棋盘上，并且使皇后彼此之间不能相互攻击。

<center class="half">
    <img src="https://assets.leetcode.com/uploads/2018/10/12/8-queens.png" width="300" hegiht="313">
</center>

上图为 8 皇后问题的一种解法。

给定一个整数 *n*，返回 *n* 皇后不同的解决方案的数量。

**示例:**

```
输入: 4
输出: 2
解释: 4 皇后问题存在如下两个不同的解法。
[
 [".Q..",  // 解法 1
  "...Q",
  "Q...",
  "..Q."],

 ["..Q.",  // 解法 2
  "Q...",
  "...Q",
  ".Q.."]
]
```

**解题思路**

使用之前问题的方法[Leetcode 51：N皇后（最详细的解法！！！）](https://blog.csdn.net/qq_17550379/article/details/82770400)，稍加修改即可。

```python
class Solution:
    def totalNQueens(self, n):
        """
        :type n: int
        :rtype: int
        """
        row = [0 for i in range(n)]
        def generateBoard(m, row):
            board = [str() for i in range(n)]
            for i in range(m):
                board[i] = row[i]*'.' + 'Q' + (m-row[i]-1)*'.'
                
            return board
        
        def isValid(k, row):
            for i in range(k):
                if row[i] == row[k] or abs(row[i] - row[k]) == k - i:
                    return False
                
            return True
        
        k, res = 0, 0
        while k >= 0:
            while row[k] < n and not isValid(k, row):
                row[k] += 1
                
            if row[k] < n:
                if k == n - 1:
                    res += 1
                    row[k] += 1
                else:
                    k += 1
            else:
                row[k] = 0
                k -= 1
                row[k] += 1
                
        return res  
```

由于这个问题和之前问题不一样，我们只需要知道最后结果有多少个就可以了，并不需要知道具体的皇后摆放情况，所以我们可以通过建立`set`的方式记录`两个对角线`、`行`上摆放皇后的情况，具体操作和之前[Leetcode 51：N皇后（最详细的解法！！！）](https://blog.csdn.net/qq_17550379/article/details/82770400)计算坐标的方法一致。

```python
class Solution:
    def totalNQueens(self, n):
        """
        :type n: int
        :rtype: int
        """
        cols, diag1, diag2 = set(), set(), set()
        
        def getResult(n, diag1, diag2, cols, row):
            if row == n:
                return 1
            
            res = 0
            for col in range(n):
                d1 = row + col
                d2 = row - col
                if d1 in diag1 or d2 in diag2 or col in cols:
                    continue
                    
                diag1.add(d1)
                diag2.add(d2)
                cols.add(col)
                res += getResult(n, diag1, diag2, cols, row + 1)
                diag1.remove(d1)
                diag2.remove(d2)
                cols.remove(col)
                
            return res
        
        return getResult(n, diag1, diag2, cols, 0)
```

**我将该问题的其他语言版本添加到了我的[GitHub Leetcode](https://github.com/luliyucoordinate/Leetcode)**

**如有问题，希望大家指出！！！**
