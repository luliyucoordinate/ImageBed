---
layout: post
title: RefineDet论文笔记
category : 机器学习
tags : [YOLO, python, c, darknet]
stickie: true
date: 2018-01-15 00:00:00
---

论文地址：[Single-Shot Refinement Neural Network for Object Detection](https://arxiv.org/pdf/1711.06897.pdf)

项目地址：[RefineDet](https://github.com/sfzhang15/RefineDet)

# 0x01 Abstract

当前的目标检测网络主要分为两大类：

- `single-stage`：SSD、YOLO、YOLO9000
- `two-stage`：Faster RCNN 、 R-FCN、Mask R-CNN

`single-stage`通过对位置，比例和长宽进行规则和密度采样来检测对象。`two-stage`首先选取目标区域，然后对目标分类。`single-stage`方法速度快，但是检测精度比`two-stage`低。

因此作者提出了`RefineDet`方法，同行继承了`two-stage`和`single-stage`两者的优点。它有两个模块构成，一个是anchor细化模块（ARM）一个是目标检测模块（ODM）。

<center class="half">
<img src="http://wx2.sinaimg.cn/mw690/af2d2659ly1fniigbskepj20qw0eomzg.jpg" >
</center>

ARM模块用来减小分类器的搜索空间，粗略地描述anchor的位置和大小。通过连接模块（TCB）将ARM中的特征，传输给ODM模块，以获取更加准确的目标位置和大小。

其实这里我们可以知道，这个网络的好处就是将那个原来two-stage的串行结构转化成了并行结构。很不错的思想！！！

# 0x02 网络结构

和SSD一样，`RefineDet`采用前馈网络，该网络产生固定数量的框，并且区分框中的不同类别对象，最后非极大值抑制输出最终结果。

`RefineDet`有两个互相连接的模块ARM和ODM组成。这两个模块之间通过TCB模块连接

<center class="half">
<img src="http://wx2.sinaimg.cn/mw690/af2d2659ly1fnijb7g8a4j20c50d53z8.jpg" >
</center>

而且这里的TCB是将不同层次的ARM特征转化为ODM，它这里有一个回传的操作，将高层次的特征通过去卷机操作（实际是一种转置卷积），使特征图之间的尺寸匹配，然后与低层次的特征相加。

针对小目标的识别，作者这里采用了两步级联回归。在ARM中先调整anchor的位置和大小，然后用这种粗略的操作作为ODM的输入，最后ODM再进一步检测和识别物体，这种做法会有更加精确的检测结果。

`single-stage`精度落后于`two-stage`的一个主要原因是类别不平衡问题。为了解决这种问题，作者采用了`Negative anchor`过滤。在训练阶段，针对ARM中的anchor，如果`negative confidence`大于一个阈值$\theta$（$\theta=0.99$），那么在训练ODM时将它舍弃。也就是通过`hard Negative anchor`和ARM anchor来训练ODM。

RefineDet的损失函数由两部分组成，即ARM中的损失和ODM中的损失。损失函数定义为

- $L(\{p_i\},\{x_i\},\{c_i\},\{t_i\}) = \frac{1}{N_{arm}}(\sum_iL_b(p_i, [l_i^* \geq1])+\sum_i[l_i^* \geq1]L_r(x_i,g_i^*)+\frac{1}{N_{odm}}(\sum_iL_m(c_i,l_i^*)+\sum_i[l_i^*\geq1]L_r(t_i,g_i^*))$

其中`i`表示一个batch中的第几个anchor，$l_i^*$表示`anchor_i`的ground truth的类别 ，$g_i^*$表示`anchor_i`的ground truth位置和大小，$p_i$b表示置信度，$x_i$表示ARM中anchor的坐标。$c_i$表示预测类别，$t_i$表示ODM中的预测框坐标信息。$N_{arm}$和$N_{odm}$分别表示ARM和ODM中的`positive anchor`数量。$L_b$表示二值分类损失（有目标\没有目标），$L_m$表示多类别损失，$L_r$表示回归损失。$[l_i^*\geq1]$就表示如果`negative confidence`大于一个阈值$\theta$，那么返回1，否则返回0。如果$N_{arm}=0$，设置$L_b(p_i, [l_i^* \geq1])=0$和$L_r(x_i,g_i^*)=0$；如果$N_{odm}=0$，那么设置$L_m(c_i,l_i^*)=0$和$L_r(t_i,g_i^*)=0$。

# 0x03 训练结果


<center class="half">
<img src="http://wx3.sinaimg.cn/mw690/af2d2659ly1fnjdf3ssb7j20r80f40x2.jpg" >
</center>


<center class="half">
<img src="http://wx1.sinaimg.cn/mw690/af2d2659ly1fnjdf7d3wrj20ru0j97ay.jpg" >
</center>

