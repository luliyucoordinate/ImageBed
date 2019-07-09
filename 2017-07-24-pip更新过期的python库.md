---
layout: post
title: pip更新过期的python库
category : python
tags : [python, pip]
stickie: true
---

查看系统里过期的python库，可以用pip命令

```python
pip list  #列出所有安装的库
pip list --outdated #列出所有过期的库
```

对于列出的过期库，pip更新的命令

```python
pip install --upgrade 库名 
```

在stackoverflow上有人提供了批量更新的办法，一个循环就搞定（注意--upgrade后面的空格）

```python
import pip
from subprocess import call
 
for dist in pip.get_installed_distributions():
    call("pip install --upgrade " + dist.project_name, shell=True)
```

另外的也有人提到用 [pip-review](https://github.com/jgonggrijp/pip-review) 

```python
pip install pip-review
pip-review --local --interactive
```