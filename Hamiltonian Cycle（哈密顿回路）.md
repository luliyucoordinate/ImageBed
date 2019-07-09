---
layout: post
title: Hamiltonian Cycle（哈密顿回路）
category : 算法
tags : [Hamiltonian Cycle, np]
stickie: true
date: 2019-7-6 00:00:00
---

对于无向图来说，哈密顿路径对于图每个顶点只访问一次。 哈密顿回路（或哈密顿循环）是一个哈密顿路径，并且从哈密顿路径的最后一个顶点到第一个顶点存在边缘（也就是可以回到初始位置）。 确定给定图是否包含哈密顿回路。 如果包含，则打印路径。 以下是所需功能的输入和输出。

输入：`2D`阵列`graph[V][V]`(其中V是图中的顶点数，通过邻接矩阵表示)。如果从`i`到`j`存在一条边，则`graph[i][j]`为`1`，否则`graph[i][j]`为`0`。

输出：包含哈密顿回路的`path[V]`。 `path[i]`应该表示哈密顿回路中的第`i`个顶点。 如果图中没有哈密顿回路，代码也应该返回`false`。

例如，下图中的哈密顿回路是`{0,1,2,4,3,0}`。

```
(0)--(1)--(2)
 |   / \   |
 |  /   \  | 
 | /     \ |
(3)-------(4)
```

并且下图不包含任何哈密尔顿回路。

```
(0)--(1)--(2)
 |   / \   |
 |  /   \  | 
 | /     \ |
(3)      (4) 
```

**解题思路**

最简单的思路就是，生成顶点的全排列，然后循环遍历每个排列是不是满足条件。伪代码

```cpp
当存在未遍历到的组合时
{
    if（两个连续顶点之间有边
       并且最后一个顶点和初始点是相连通的）。
   {
       打印这种排列方式。
       break;
   }
}
```

这种算法的时间复杂度是`O(n!)`级别的，显然如果`n`较大的话，那么这种做法是不合理的。我们可以使用回溯法解决这个问题。

我们首先创建一个空的`path`，并且将`0`这个点加入其中。然后我们从`1`开始添加后续顶点。在添加后续顶点之前，我们首先要检查这些顶点是不是与之前添加的顶点相邻并且我们没有添加过。如果找到了这样的点的话，我们就将它添加到`path`中去，接着我们就要判断下一个位置的点，在此之前我们先要判断我们现在`path`中点的数量是不是已经是全部点的个数了，如果是的话我们要判断头结点和尾节点是不是存在边，如果存在的话，我们就输出`path`，如果不存在，我们就要将刚才加入的点给弹出，继续加入下一个有效点测试。

下面是回溯法解决问题的代码：

```python
class Graph: 
    def __init__(self, vertices): 
        self.graph = [[0 for column in range(vertices)]\
                            for row in range(vertices)] 
        self.V = vertices 
  
    '''
    Check if this vertex is an adjacent vertex  
    of the previously added vertex and is not  
    included in the path earlier 
    '''
    def isSafe(self, v, pos, path): 
        # Check if current vertex and last vertex  
        # in path are adjacent 
        if self.graph[ path[pos-1] ][v] == 0: 
            return False
  
        # Check if current vertex not already in path 
        for vertex in path: 
            if vertex == v: 
                return False
  
        return True
  
    # A recursive utility function to solve  
    # hamiltonian cycle problem 
    def hamCycleUtil(self, path, pos): 
        # base case: if all vertices are  
        # included in the path 
        if pos == self.V: 
            # Last vertex must be adjacent to the  
            # first vertex in path to make a cyle 
            if self.graph[ path[pos-1] ][ path[0] ] == 1: 
                return True
            else: 
                return False
  
        # Try different vertices as a next candidate  
        # in Hamiltonian Cycle. We don't try for 0 as  
        # we included 0 as starting point in in hamCycle() 
        for v in range(1,self.V): 
            if self.isSafe(v, pos, path) == True: 
                path[pos] = v 
                if self.hamCycleUtil(path, pos+1) == True: 
                    return True
                # Remove current vertex if it doesn't  
                # lead to a solution 
                path[pos] = -1
  
        return False
  
    def hamCycle(self): 
        path = [-1] * self.V 
        ''' 
        Let us put vertex 0 as the first vertex  
        in the path. If there is a Hamiltonian Cycle,  
        then the path can be started from any point 
        of the cycle as the graph is undirected 
        '''
        path[0] = 0
        if self.hamCycleUtil(path,1) == False: 
            print("Solution does not exist")
            return False
  
        self.printSolution(path) 
        return True
  
    def printSolution(self, path): 
        print("Solution Exists: Following is one Hamiltonian Cycle")
        for vertex in path: 
            print(vertex, end=' ') 
        print(path[0])
  
# Driver Code 
  
'''
 Let us create the following graph 
      (0)--(1)--(2) 
       |   / \   | 
       |  /   \  | 
       | /     \ | 
      (3)-------(4)    
'''
g1 = Graph(5) 
g1.graph = [ [0, 1, 0, 1, 0], [1, 0, 1, 1, 1],  
             [0, 1, 0, 0, 1,],[1, 1, 0, 0, 1],  
             [0, 1, 1, 1, 0], ] 
  
# Print the solution 
g1.hamCycle()
  
'''
Let us create the following graph 
      (0)--(1)--(2) 
       |   / \   | 
       |  /   \  | 
       | /     \ | 
      (3)       (4)
'''
g2 = Graph(5) 
g2.graph = [ [0, 1, 0, 1, 0], [1, 0, 1, 1, 1],  
           [0, 1, 0, 0, 1,], [1, 1, 0, 0, 0],  
           [0, 1, 1, 0, 0], ] 
  
# Print the solution 
g2.hamCycle()
  
# This code is contributed by Divyanshu Mehta 
```

reference:

https://www.geeksforgeeks.org/hamiltonian-cycle-backtracking-6/
