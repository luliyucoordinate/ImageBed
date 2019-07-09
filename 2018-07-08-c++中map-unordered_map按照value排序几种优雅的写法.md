---
layout: post
title: c++中map unordered_map按照value排序几种优雅的写法
category : 算法
tags : [c++]
stickie: true
date: 2018-07-08 00:00:00
---

我们首先假设我们要操作的`map`、`unordered_map`对象是`m`。

第一种做法是先建立一个`vector<pair<type, type>>`的容器。

```c++
std::vector<std::pair<int, int>> tmp;
for (auto& i : m)
    tmp.push_back(i);

std::sort(tmp.begin(), tmp.end(), 
          [=](std::pair<int, int>& a, std::pair<int, int>& b) { return a.second < b.second; });
```

第二种写法更加符合现代`c++`。首先建立一个临时`map`，然后通过`transform`函数将`m`中的元素`inserter`进`tmp`中。通过将`map`中元素的`first`和`second`交换达到，对`value`排序的目的。

```c++
std::map<int, int> tmp;
std::transform(m.begin(), m.end(), std::inserter(tmp, tmp.begin()), 
               [](std::pair<int, int> a) { return std::pair<int, int>(a.second, a.first); });
```

不过第二种写法要加头文件`#include <algorithm>`和`#include <iterator>`。`c++`中的`transform`有点类似于`python`中的`map`。