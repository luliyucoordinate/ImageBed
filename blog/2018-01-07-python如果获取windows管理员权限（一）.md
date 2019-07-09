---
layout: post
title: python如果获取windows管理员权限（一）
category : python
tags :  [python, windows]
stickie: true
---

我们在运行我们编写好的`python`代码时，会碰到这样的报错问题

> PermissionError: [WinError 5] 拒绝访问。

这是因为我们编写的脚本的权限不够。一种解决办法是在管理员`cmd`中运行我们的脚本（右键以 run as administrator），但是这种办法不够优雅。我们经常看到当我们运行一些需要高权限的软件时，会弹出以下对话框

<center class="half">
<img src="http://wx1.sinaimg.cn/mw690/af2d2659ly1fn8yommimij20df09pab9.jpg" >
</center>

这被称为用户安全控制，简称为UAC。

- **用户帐户控制**（*User Account Control*，简写作UAC)是微软司在其Windows Vista及更高版本操作系统中采用的一种控制机制。其原理是通知用户是否对应用程序使用硬盘驱动器8)和系统文件授权，以达到帮助阻止恶意程序（有时也称为“恶意软件”）损坏系统的效果。

那么我们在写代码的时候怎么添加这个功能呢？

这里我们要用到一个关键的函数`ShellExecute`

```cpp
HINSTANCE ShellExecute(
  _In_opt_ HWND    hwnd,
  _In_opt_ LPCTSTR lpOperation,
  _In_     LPCTSTR lpFile,
  _In_opt_ LPCTSTR lpParameters,
  _In_opt_ LPCTSTR lpDirectory,
  _In_     INT     nShowCmd
);
```

具体细节看微软官方的文档[ShellExecute function](https://msdn.microsoft.com/en-us/library/windows/desktop/bb762153(v=vs.85).aspx)

```python
from __future__ import print_function
import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
if is_admin():
    # 将要运行的代码加到这里
else:
    if sys.version_info[0] == 3:
    	ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:#in python2.x
        ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)
```

要提醒你的是，**不要在IDE中运行**。

如果在非管理员权限下运行的话，其实这里运行了两次代码，第一次肯定是没有管理员权限的，第二次拥有管理员权限。

有的时候我们不希望有这种UAC弹框，我们希望程序偷偷的拥有管理员权限，这要怎么做呢？这其实挺邪恶的。感兴趣的话，可以看这篇[python如果获取windows管理员权限（二）](http://blog.csdn.net/qq_17550379/article/details/79006718)




