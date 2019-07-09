---
layout: post
title: AttributeError 'NoneType' object has no attribute 'bands'
category : python
tags : [python, PIL]
stickie: true
---



今天做一个验证码检测的测试，出现这样的错误`AttributeError: 'NoneType' object has no attribute 'bands'`

<a href="http://wx2.sinaimg.cn/mw690/af2d2659gy1fi4dur47tij20yo06cjru.jpg" data-lightbox="roadtrip">
<img src="http://wx2.sinaimg.cn/mw690/af2d2659gy1fi4dur47tij20yo06cjru.jpg" class="img-fluid">
</a>

原因在于Image库中的一个bug

<a href="http://wx4.sinaimg.cn/mw690/af2d2659gy1fi4dus6o89j20ik0653yr.jpg" data-lightbox="roadtrip">
<img src="http://wx4.sinaimg.cn/mw690/af2d2659gy1fi4dus6o89j20ik0653yr.jpg" class="img-fluid">
</a>

解决办法

```python
def split(self):
        "Split image into bands"

        self.load()	#移到这个位置，还要注意一点是，前面如果是空8个，就老老实实的打空格，不要按tab键，会报错的！！！
        if self.im.bands == 1:
            ims = [self.copy()]
        else:
            #self.load()
            ims = [] 
            for i in range(self.im.bands):
                ims.append(self._new(self.im.getband(i)))
        return tuple(ims)
```
