---
layout: post
title: YOLOv2源码分析--reorg layer
category : python
tags :  [python, yolo]
stickie: true
---

文章全部[YOLOv2源码分析](http://blog.csdn.net/column/details/18380.html)

reorg layer中最关键的代码如下

```c
void reorg_cpu(float *x, int w, int h, int c, int batch, int stride, int forward, float *out)
{
    int b,i,j,k;
    int out_c = c/(stride*stride);

    for(b = 0; b < batch; ++b){
        for(k = 0; k < c; ++k){
            for(j = 0; j < h; ++j){
                for(i = 0; i < w; ++i){
                    int in_index  = i + w*(j + h*(k + c*b));
                    int c2 = k % out_c;
                    int offset = k / out_c;
                    int w2 = i*stride + offset % stride;
                    int h2 = j*stride + offset / stride;
                    int out_index = w2 + w*stride*(h2 + h*stride*(c2 + out_c*b));
                    if(forward) out[out_index] = x[in_index];
                    else out[in_index] = x[out_index];
                }
            }
        }
    }
}
```

这一部分表述为数学公式就是

- $in\_index=W_1+W*stride*(H_1+H*(C_1+C*B))$


- $C_2=C_1\%C_{out}$
- $offset = C_1/C_{out}$
- $W_2=W_1*stride+offset\%stride$
- $H_2=H_1*stride+offset/stride$
- $out\_index = W_2+W*stride*(H_2+H*stride*(C_2+C_{out}*B))$

对于前向传播，想要表达的意思就是下面这个图

<center class="half">
<img src="http://wx2.sinaimg.cn/mw690/af2d2659ly1fn1yyl8fnfj20rg0eaq3f.jpg" >
</center>

那么我们知道，矩阵运算可以更加简洁的表示上面的代码中的循环，我这里给出pytorch下的代码示例

```python
B,C,H,W = input.size()
input = input.view(B, C, H/stride, stride, W/stride, stride).transpose(3,4).contiguous()
input = input.view(B, C, H/stride*W/stride, stride*stride).transpose(2,3).contiguous()
input = input.view(B, C, stride*stride, H/stride, W/stride).transpose(1,2).contiguous()
input = input.view(B, stride*stride*C, H/stride, W/stride)
```

非常简洁的就解决了上述的问题，但是简洁背后的数学原理你要明白。

首先我先说一下这里的参数含义:

- `B`:`batch`
- `C`:通道数目
- `H`:高
- `W`:宽

按照论文中的做法，我们这里`stride`取2

```python
input = input.view(B, C, H/stride, stride, W/stride, stride).transpose(3,4).contiguous()
```

这里的`view`函数的意义，我么可以理解为“看成”

这个式子想要表达的含义如下图：

<center class="half">
<img src="http://wx2.sinaimg.cn/mw690/af2d2659ly1fn20wg6nflj20cd0ewweh.jpg" >
</center>

```python
input = input.view(B, C, H/stride*W/stride, stride*stride).transpose(2,3).contiguous()
```

这个式子想要表达的含义如下图：

<center class="half">
<img src="http://wx1.sinaimg.cn/mw690/af2d2659ly1fn212t4l1fj20o20d8q2x.jpg" >
</center>

从第一个式子到第二个式子的过程我们可以抽象为

<center class="half">
<img src="http://wx4.sinaimg.cn/mw690/af2d2659ly1fn1zy29yxej20bq0h9dfz.jpg" >
</center>

```python
input = input.view(B, C, stride*stride, H/stride, W/stride).transpose(1,2).contiguous()
```

这个式子想要表达的含义如下图：

<center class="half">
<img src="http://wx3.sinaimg.cn/mw690/af2d2659ly1fn21bwz88oj20vp0fv74c.jpg" >
</center>

最后抽象为

<center class="half">
<img src="http://wx1.sinaimg.cn/mw690/af2d2659ly1fn21j8ocyxj20o60cajra.jpg" >
</center>

**觉得不错，点个赞吧b(￣▽￣)d**

由于本人水平有限，文中有不对之处，希望大家指出，谢谢^_^!