---
layout: post
title: Iterative Visual Reasoning Beyond Convolutions论文笔记
category : 机器学习
tags : [Li Fei Fei, Google]
stickie: true
date: 2018-04-07 00:00:00
---

论文地址：[Iterative Visual Reasoning Beyond Convolutions](https://arxiv.org/abs/1803.11189v1)

# 0x00 论文简述

我们碰到过很多这样的问题：如果一个物体很小，或者目标很模糊，或者这个物体被遮住一部分，那么我们在做目标检测时，我们现在的算法会忽略这些目标。但是人类可以通过周边的事物以及物体的大致形状推断出这个目标的类型。如图：

<center class="half">
<img src="http://wx1.sinaimg.cn/mw690/af2d2659ly1fq4c4qlwkwj20fy0lidta.jpg"  width="300" height="400">
</center>

上图左上角中的窗户，从左往右第一个窗户，由于被电线杆遮住一部分，变得很难辨认，但是我们可以从后面的窗户去推测出这是一个窗户。我们还可以看到，中间的车中坐着一个人（但是这是经过我们推测出来的），但是图像上很模糊。

<center class="half">
<img src="http://wx1.sinaimg.cn/mw690/af2d2659ly1fq4c4tt7ezj214709cn5x.jpg" >
</center>

这篇文章主要提出了一种空间推理和语义推理的通用框架。算法核心有两个部分构成。

- 基于空间记忆的局部模块，通过卷积网络进行像素级的局部推理
- 基于图结构的全局模块，用于全局推理

# 0x01 局部模块 

局部模块中：

- 空间存储器$s_i$，该模块用于存储先前的并行更新认知。该模块是一个三维张量（高度H，宽度W和深度D=512）
- 推理模块卷积网络C，由三个`3*3`的卷积核和两个4096的全连接层组成。

给定一个未更新的图像区域r，先通过特征提取，然后使用双线性插值将其调整为大小（`7*7`）的方阵h。因为高层的特征是覆盖整个区域的向量，所以我们将这个向量附加到所有位置，通过`1*1`的卷积核来提取特征，并且输出$f_r$。记忆存储器$s_i$中的相同区域也提取出来，调整为`7*7`，标记为$s_r$。这一步后，我们使用GRU：

- $s_r' = u\circ s_r + (1-u)\circ \sigma(W_f f_r+W_s(z\circ s_r)+b)$

其中，$s_r'$是$r$更新后的记忆，$u$是更新后的门，$z$是重置门，$W_f$，$W_s$和$b$分别是卷积的权重和偏向，$\circ$表示`entry-wise`矩阵内积，$\sigma$表示激活函数。更新后，$s_r'$通过提取特征和尺寸调整重新放回$S$

# 0x02 全局模块

全局模块由三部分组成：

- 我们将不同的类别表示为节点，建立边来获取他们之间的联系，这部分称为知识图
- 每个节点代表图像的某个区域，这部分称为区域图
- 将不同的区域分配给不同的类，这部分称为分配图

对于每个节点之间，定义三条边，分别表示：

- 相对位置
- 一个区域是否属于某个类。
- 构建类间的关系。“is-kind-of”蛋糕和食物。"is-part-of"车轮和车。"相似" 豹和猎豹。

<center class="half">
<img src="http://wx2.sinaimg.cn/mw690/af2d2659ly1fq4c4wkpesj209h066dgj.jpg" >
</center>

如图所示，四个节点之间通过不同的边连接。每个节点表示一个输入特征向量$M_i$。中间的$A_j$表示连接矩阵，用来描述各边$M_i$之间的关系，我们通过训练学习到一组权重$W$。最后的输出为$G$。

接着就是推理的过程。我们假设输入是$M_r$和$M_c$（类别），它们的深度D=512。

<center class="half">
<img src="http://wx3.sinaimg.cn/mw690/af2d2659ly1fq4c4zoodnj20ak04eq3n.jpg" >
</center>

输出$G^{spatial}_r$可以表示为

- $G^{spatial}_r = \sum_{e \in \epsilon_{r \rightarrow r}} {A_e M_r W_e}$

$A_e$就是前面的连接矩阵，$M_r$是输入矩阵，$W_e$就是前面的权重矩阵。

将不同区域映射到不同类得到矩阵$A_{e \rightarrow c}$ 和矩阵$W_{e \rightarrow c}$

- $G^{semantic}_r = \sum_{e \in \epsilon_{c \rightarrow c}} {A_e \sigma (A_{e_{r \rightarrow c}}M_rW_{e_{r \rightarrow c}} +M_cW_c)W_e}$

最后的输出

- $G_r = \sigma(G^{spatial}_r+\sigma(A_{e_{c \rightarrow r}}G^{semantic}_cW_{e_{c \rightarrow r}}))$


# 0x03 融合

通过加入`cross-feed`连接。将局部特征和全局特征连接，并且利用`GRU`更新输出$S_i$和$M_i$

<center class="half">
<img src="http://wx2.sinaimg.cn/mw690/af2d2659ly1fq4c52kqq0j202n05odfq.jpg" >
</center>

文章使用了attention（注意力机制），通过attention值（也就是图中的$a_i$）表示当前预测与其他模块预测的相对置信度。通过$a_i$和$f$的融合，实际上是一种加权表示。最后的输出表示为

- $f = \sum_n{w_nf_n} $     where    $w_n=\frac{exp(-a_n)}{\sum_{n'} exp(-a'_n)}$


<center class="half">
<img src="http://wx3.sinaimg.cn/mw690/af2d2659ly1fq4c5awm1aj204q087aaf.jpg" >
</center>

# 0x04 结果

通过这种结构获得的收益远高于增加网络的深度。


<center class="half">
<img src="http://wx3.sinaimg.cn/mw690/af2d2659ly1fq4c5d7lo6j20hl0ep41b.jpg" width="300" height="300" >
</center>