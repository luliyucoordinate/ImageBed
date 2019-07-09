---
layout: post
title: Kolakoski sequence 
category : cpp
tags : [cpp, Kolakoski]
stickie: true
---

题目描述
---

Kolakoski序列是个自生成的无限序列。

例如，当给定的整数组为[1,2]时，Kolakoski序列是这样的：

[1,2,2,1,1,2,1,2,2,1,2,2,1,1,2......]

如果我们将相邻的相同的数字分成一组，那么将会得到：

[[1],[2,2],[1,1],[2],[1],[2,2],[1],[2,2],[1,1],[2]........]

可以看出，每组数字交替由1，2组成。

接下来对每个分组求他的长度，得到：

[1,2,2,1,1,2,1,2,2,1,2,2,1,1,2......]

输入描述
---

输入有两行组成：

第一行包括两个整数n，m

第二行包括m个正整数a[]

数据规模限制：

0 < n < 10000    1 < m < 1000    0 < a[i] < 1000

a[i] != a[i+1]     a[0] != a[m-1]

输出描述
---

每行一个数字，共n行

整数组a生成的Kolakoski序列的前n项

问题的解决
---

我觉得下面这个解法还不错

```c++
#include <iostream>
#include <vector>
#include <iterator>
#include <algorithm>			//adjacent_find

int main()
{
	int m, n;
	std::cout << "Enter number n,m:\n";
	std::cin >> n >> m;
	if (n <= 0 || n >= 10000 || m <= 1 || m >= 1000)
	{
		std::cout << "input error";
		return -1;
	}
	std::vector<int> a(m);
	std::cout << "Enter m numbers:\n";
	for (int i = 0; i < m; i++) {
		int temp;
		std::cin >> temp;
		a[i] = temp;
	}
	if (a[0] == a[m - 1])
	{
		std::cout << "input error : a[0] == a[m - 1]";
         return -1;
	}
	//查找相邻元素有很多做法，我这里使用的标准库里的做法
	auto&& pan = std::adjacent_find(std::begin(a), std::end(a));
	if (pan != a.end())
	{
		std::cout << "input error : have the same adjacent element";
         return -1;
	}
	std::vector<int> result{};
	for (int i = 0, j = 0; i < n && j < n; ++i, ++j)
	{
		int curNum = a[i % m];
		result.push_back(curNum);
		for (int count = 1; count < result[i] && j < n; ++count, ++j)
		{
			result.push_back(curNum);
		}		
	}
	std::copy(std::begin(result), std::end(result), std::ostream_iterator<int>(std::cout, "\n"));
	system("pause");
}
```
由于现在的大部分平台还没有支持C++14:( ，所以我写了下面这个版本