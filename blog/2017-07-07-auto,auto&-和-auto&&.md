---
layout: post
title: auto,auto& 和 auto&&
category : cpp
tags : [cpp, 转载, auto, auto&, auto&&]
stickie: true
---



auto and auto&& cover most of the cases:  

1.  Use auto when you need a local copy. This will never produce a reference. The copy (or move) constructor must exist, but it might not get called, due to the copy elision optimization.
2.  Use auto&& when you don't care if the object is local or not. Technically, this will always produce a reference, but if the initializer is a temporary (e.g., the function returns by value), it will behave essentially like your own local object.

Also, auto&& doesn't guarantee that the object will be modifiable, either. Given a constobject or reference, it will deduce const. However, modifiability is often assumed, given the specific context.  

auto& and auto const & are a little more specific:  

1.  auto& guarantees that you are sharing the variable with something else. It is always a reference and never to a temporary.
2.  auto const & is like auto&&, but provides read-only access.

What about for primitive/non-primitive types?  
There is no difference.  

Does this also apply to range based for loops?  
Yes. Applying the above principles,  

1.  Use auto&& for the ability to modify and discard values of the sequence within the loop. (That is, unless the container provides a read-only view, such as std::initializer_list, in which case it will be effectively an auto const &.)
2.  Use auto& to modify the values of the sequence in a meaningful way.
3.  Use auto const & for read-only access.
4.  Use auto to work with (modifiable) copies.

You also mention auto const with no reference. This works, but it's not very commonly used because there is seldom an advantage to read-only access to something that you already own.  


