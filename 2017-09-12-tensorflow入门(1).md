---
layout: post
title: tensorflow入门
category : 机器学习
tags : [深度学习, tensorflow]
stickie: true
---

占位符
--

```python
x = tf.placeholder("float", shape=[None, 784])
y_ = tf.placeholder("float", shape=[None, 10])
```

这里的`x`和`y`是一个`占位符`，可以在TensorFlow运行某一计算时根据该占位符输入具体的值。

输入`x`是一个2维的浮点数张量。这里，分配给它的`shape`为`[None, 784]`，`None`表示其值大小不定，在这里作为第一个维度值。输出类别值`y_`也是一个2维张量，其中每一行为一个10维的向量。

变量
---

```python
import tensorflow as tf
sess = tf.InteractiveSession()
W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))
```

我们在调用`tf.Variable`的时候传入初始值。在这个例子里，我们把`W`和`b`都初始化为零向量。`W`是一个784x10的矩阵（因为我们有784个特征和10个输出值）。`b`是一个10维的向量（因为我们有10个分类）。

变量需要通过seesion初始化后，才能在session中使用。这一初始化步骤为，为初始值指定具体值（本例当中是全为零），并将其分配给每个变量,可以一次性为所有变量完成此操作。

```python
sess.run(tf.initialize_all_variables())
```

**在tensorflow最新版本中变为了**

```python
sess.run(tf.global_variables_initializer())
```

 卷积和池化
 ---

```python
def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')
```

我们的卷积使用1步长（stride size），这里的stride包含四个参数\[batch, height ,width, channels\](即样本数目，样本的高度，样本的宽度，样本的通道数)。0边距（padding size）的模板，这里padding有两个参数。

- `"VALID"` = without padding:

  ```
     inputs:         1  2  3  4  5  6  7  8  9  10 11 (12 13)
                    |________________|                dropped
                                   |_________________|
  ```

- `"SAME"` = with zero padding:

  ```
                 pad|                                      |pad
     inputs:      0 |1  2  3  4  5  6  7  8  9  10 11 12 13|0  0
                 |________________|
                                |_________________|
                                               |________________|
  ```

保证输出和输入是同一个大小。我们的池化用简单传统的2x2大小的模板做max pooling。



`tf.nn.conv2d(input, filter, strides, padding, use_cudnn_on_gpu=None, name=None)`

除去name参数用以指定该操作的name，与方法有关的一共五个参数：

- 第一个参数input：指需要做卷积的输入图像，它要求是一个Tensor，具有 `[batch, in_height, in_width, in_channels]` 这样的shape，具体含义是[训练时一个batch的图片数量, 图片高度, 图片宽度, 图像通道数]，注意这是一个4维的Tensor，要求类型为float32和float64其中之一
- 第二个参数filter：相当于CNN中的卷积核，它要求是一个Tensor，具有 `[filter_height, filter_width, in_channels, out_channels]` 这样的shape，具体含义是[卷积核的高度，卷积核的宽度，图像通道数，卷积核个数]，要求类型与参数input相同，有一个地方需要注意，第三维in_channels，就是参数input的第四维
- 第三个参数strides：卷积时在图像每一维的步长，这是一个一维的向量，长度4
- 第四个参数padding：string类型的量，只能是"SAME","VALID"其中之一，这个值决定了不同的卷积方式（后面会介绍）
- 第五个参数：`use_cudnn_on_gpu:bool` 类型，是否使用cudnn加速，默认为true

结果返回一个Tensor，这个输出，就是我们常说的feature map



`tf.nn.max_pool(value, ksize, strides, padding, name=None)`

参数是四个，和卷积很类似：

- 第一个参数value：需要池化的输入，一般池化层接在卷积层后面，所以输入通常是feature map，依然是`[batch, height, width, channels]这样的shape`
- 第二个参数ksize：池化窗口的大小，取一个四维向量，一般是`[1, height, width, 1]，因为我们不想在batch和channels上做池化，所以这两个维度设为了1`
- 第三个参数strides：和卷积类似，窗口在每一个维度上滑动的步长，一般也是`[1, stride,stride, 1]`
- 第四个参数padding：和卷积类似，可以取'VALID' 或者'SAME'

返回一个Tensor，类型不变，shape仍然是`[batch, height, width, channels]`这种形式