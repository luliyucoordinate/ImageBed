---
layout: post
title: Leetcode 742：Closest Leaf in a Binary Tree（超详细的解法！！！）
category : 算法
tags : [python, c, c++]
stickie: true
date: 2019-2-20 00:00:00
---

Given a binary tree **where every node has a unique value**, and a target key k, find the value of the nearest leaf node to target k in the tree.

Here, nearest to a leaf means the least number of edges travelled on the binary tree to reach any leaf of the tree. Also, a node is called a leaf if it has no children.

In the following examples, the input tree is represented in flattened form row by row. The actual root tree given will be a TreeNode object.

**Example 1:**

```
Input:
root = [1, 3, 2], k = 1
Diagram of binary tree:
          1
         / \
        3   2

Output: 2 (or 3)

Explanation: Either 2 or 3 is the nearest leaf node to the target of 1.
```

**Example 2:**

```
Input:
root = [1], k = 1
Output: 1

Explanation: The nearest leaf node is the root node itself.
```

**Example 3:**

```
Input:
root = [1,2,3,4,null,null,null,5,null,6], k = 2
Diagram of binary tree:
             1
            / \
           2   3
          /
         4
        /
       5
      /
     6

Output: 3
Explanation: The leaf node with value 3 (and not the leaf node with value 6) is nearest to the node with value 2.
```

**Note:**

- `root` represents a binary tree with at least `1` node and at most `1000` nodes.
- Every node has a unique `node.val` in range `[1, 1000]`.
- There exists some node in the given binary tree for which `node.val == k`.

**解题思路**

这是一个树的问题，首先思考是不是可以通过递归解决，发现并不能。接着我们观察到关键字最短路径，那么我们是不是可以使用`BFS`呢？我们首先要将树变成一个无权无向图

```python
def buildGraph(self, node, parent, k):
    if not node:
        return

    if node.val == k:
        self.start = node
    if parent:
        self.graph[node].append(parent)
        self.graph[parent].append(node)
    self.buildGraph(node.left, node, k)
    self.buildGraph(node.right, node, k)
```

接着我们就可以通过`BFS`去遍历这个图看我们的最短路径是谁。

```python
class Solution:
    def findClosestLeaf(self, root: 'List[TreeNode]', k: 'int') -> 'int':
        self.start = None
        self.buildGraph(root, None, k)
        q, visited = [root], set()
        self.graph = collections.defaultdict(list)
        while q:
            for i in range(len(q)):
                cur = q.pop(0)
                visited.add(cur)
                if not cur.left and not cur.right:
                    return cur.val
                for node in self.graph:
                    if node in visited:
                        q.append(node)
```

**我将该问题的其他语言版本添加到了我的[GitHub Leetcode](https://github.com/luliyucoordinate/Leetcode)**

**如有问题，希望大家指出！！！**