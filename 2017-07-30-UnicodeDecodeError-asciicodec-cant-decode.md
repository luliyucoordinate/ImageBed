---
layout: post
title: UnicodeDecodeError 'ascii' codec can't decode
category : python
tags : [python, re]
stickie: true
---

string本身是不能encode的，如果想要encode，先要转化成unicode，此时采用默认的ascii进行转化，所以就出错了。

解决办法

1. 指明str转化成unicode的编码方式：

   ```python
   #! /usr/bin/env python     
   # -*- coding: utf-8 -*-     
       
   s = '中文'     
   s.decode('utf-8').encode('gbk') 
   ```

2.  重置变量 sys.defaultencoding 

   ```python
   import sys     
   reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入     
   sys.setdefaultencoding('utf-8')     
       
   str = '中文'     
   str.encode('gbk')  
   ```
