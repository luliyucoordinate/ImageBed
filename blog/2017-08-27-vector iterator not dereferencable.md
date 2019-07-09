---
layout: post
title: vector iterator not dereferencable
category : cpp
tags : [cpp, error]
stickie: true
---

今天碰到这样一个问题，在对如下问题编译时出现了这样的报错信息 `vector iterator not dereferencable`，这个报错信息非常的常见。以下是程序的出错片段：

```c++
void show_hands(Hands& hands, Deck& deck)
{
	auto d = dist();
	//每个人输出一个牌，最后全部放在deck中
	while (deck.size() != 52)
	{
		std::vector<Card> tempHand;
		Card maxCard{};
	
		for (auto& iter = std::begin(hands); iter < std::end(hands); ++iter)
		{
			size_t max_index = (*iter).size() - 1;
			d.param(Range{ 0, max_index });
			auto tIter = std::begin(*iter);
			std::advance(tIter, d(rng()));
			deck.push_back(*tIter);
			tempHand.push_back(*tIter);
			std::cout << *tIter << std::endl;
			(*iter).erase(tIter);			//注意的是erase是传入的指针变量
          	 Card tempCard = *tIter;		//报错位置
			maxCard = std::max(maxCard, tempCard, [](const auto& crd1, const auto& crd2) {
				return crd1.first < crd2.first || (crd1.first == crd2.first && crd1.second < crd2.second);
			});
		}
		std::cout << "最大的牌是：" << maxCard << std::endl << std::endl;
	}	
}
```
其实这个问题很不应该，很明显可以看出我是在对 `tIter`做了 `erase` 操作后，又使用`*tIter` 。原因在于 `erase` 操作后原来的指针就不存在了，自然再去访问就会报错。

还有一种情况就是访问越界，它也会造成这样的问题。