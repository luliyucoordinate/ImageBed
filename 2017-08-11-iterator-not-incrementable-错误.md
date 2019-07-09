---
layout: post
title: 	iterator not incrementable 错误
category : cpp
tags : [cpp, error, vector]
stickie: true
---

今天碰到这样一个问题，在对vector容器做删除操作的时候出现了这样的错误`iterator not incrementable` ，这个错误在vector容器运用的时候是个很细微的问题。代码如下

```c++
Direction create_direction(Cards& cards, size_t directin_size)
{
	Direction direction;
	size_t i{};
	while (i < directin_size)
	{
		Distribution choose_card{ 0, cards.size() - 1 };
		Card card = cards[choose_card(gen_value)];
		direction.insert(card);
		for (auto& iter = std::begin(cards); iter != std::end(cards); ++iter)
		{
			if (*iter == card)
			{
				cards.erase(iter);	//complie error 
			}
		}		
		++i;
	}
	return direction;
}
```
第一眼看这个代码确实是没有任何问题，后来查看了`vector`容器后发现，这个错误在于，我们在对容器做了`erase`操作后，`iter`后面的迭代器都失效了，所以再对失效的`iter`操作，自然是错误的。

这里的解决办法也非常的简单，在其后怎加一个`break`即可。

```c++
...
if (*iter == card)
{
	cards.erase(iter);	//complie error 
	break;				//added
}
...
```