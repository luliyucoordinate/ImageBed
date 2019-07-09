---
layout: post
title: TensorBoard计算图可视化
category : 机器学习
tags : [estimator, python, tensorflow]
stickie: true
---

TensorFlow计算图功能强大但复杂。 图表可视化可以帮助您理解和调试它们。 这是一个可视化工作的例子。

<center class="half">
<img src="http://wx2.sinaimg.cn/large/af2d2659ly1fm4kh0mnwug21040iw7wj.gif"  >
</center>


命名空间和节点
---

典型的TensorFlow图可能有成千上万个节点 - 太多的节点很难一次看到，甚至无法使用标准的图形工具进行布局。 为简化起见，变量名声明在作用域内，可视化使用这些信息来定义图中节点上的层次结构。 默认情况下，只显示该层次结构的顶部。 下面是一个使用`tf.name_scope`在`hidden`名称范围下定义三个操作的示例：

```python
import tensorflow as tf

with tf.name_scope('hidden') as scope:
  a = tf.constant(5, name='alpha')
  W = tf.Variable(tf.random_uniform([1, 2], -1.0, 1.0), name='weights')
  b = tf.Variable(tf.zeros([1]), name='biases')
```
这产生了以下三个操作名称：

- `hidden/alpha`

- `hidden/weights`

- `hidden/biases`

默认情况下，可视化文件将全部折叠为标记为隐藏的节点。 额外的细节不会丢失。 你可以双击，或者点击右上角的橙色`+`符号来展开节点，然后你会看到三个子节点，分别是`alpha`，`weight`和`bias`。

这是一个复杂节点在其初始状态和扩展状态的例子。

<center class="half">
<img src="http://wx2.sinaimg.cn/mw690/af2d2659ly1fm4kgw1iifj20tr0f30u2.jpg"  >
</center>

按命名空间对节点进行分组对于制作清晰的图形至关重要。如果您正在构建模型，则命名空间可以控制生成的可视化图像。你的命名空间越好，你的可视化就越好。

上图说明了可视化的第二个方面。 TensorFlow图有两种连接：数据相关性和控制相关性。数据相关性显示两个操作符之间的张量流，并用实线箭头显示，而控制相关性使用虚线。在扩展视图（上图右侧）中，除了连接`CheckNumerics`和`control_dependency`的虚线外，所有连接都是数据依赖关系。

还有一个简化布局的技巧。大多数TensorFlow图有几个与其他节点连接的节点。例如，许多节点可能对初始化步骤具有控制依赖性。绘制`init`节点及其依赖关系之间的所有边将创建一个非常混乱的视图。

为了减少混乱，可视化将所有高度节点分隔到右侧的辅助区域，并不画线来表示其边缘。我们绘制小节点图标来代替连线。分离出的辅助节点通常不会去除关键信息，因为这些节点通常与簿记功能相关。有关如何在主图形和辅助区域之间移动节点的信息，请参阅交互。

<center class="half">
<img src="http://wx1.sinaimg.cn/mw690/af2d2659ly1fm4kgwn70jj20ts09rmyj.jpg"  >
</center>

最后一个结构简化是*series collapsing*连续图案 - 也就是说，名称相差最后一个数字并具有同构结构的节点 - 会折叠成一堆节点，如下所示。 对于长序列的网络，这大大简化了视图。 与分层节点一样，双击将扩展该系列。 请参阅交互以了解如何为特定节点集禁用/启用系列折叠。

<center class="half">
<img src="http://wx1.sinaimg.cn/mw690/af2d2659ly1fm4kgx2inuj20tm04twez.jpg"  >
</center>

最后，作为易读性的最后一个帮助，可视化对常量和汇总节点使用特殊的图标。 总结为下面的节点符号表：

<center class="half">
<img src="http://wx1.sinaimg.cn/mw690/af2d2659ly1fm4kgxhputj20tq0fbjsq.jpg"  >
</center>


交互
---

通过平移和缩放导航图形。 点击并拖动以平移，并使用滚动手势进行缩放。 双击某个节点，或单击其`+`按钮，展开一个代表一组操作的命名空间。 为了在放大和平移时轻松跟踪当前视点，右下角会有一个小地图。

要关闭打开的节点，请再次双击它或单击其`- `按钮。 您也可以单击一次以选择一个节点， 它会变成一个较深的颜色，并且关于它的详细信息以及它所连接的节点将出现在右上角的可视化对象信息卡中。

<center class="half">
<img src="http://wx4.sinaimg.cn/mw690/af2d2659ly1fm4kgy45psj20tr0c4mzt.jpg"  >
</center>

TensorBoard提供了几种方法来改变图形的视觉布局。这不会改变图的计算语义，但是它可以使网络的结构变得清晰。通过右键单击某个节点或按该节点信息卡底部的按钮，可以对其布局进行以下更改：

- 节点可以在主图表和辅助区域之间移动。
- 可以将一系列节点取消分组，使得该系列中的节点不会出现在一起。未分组的序列也可以重新组合。

`Selection `也可以帮助理解高层次节点。选择任何高层次节点，其他连接的相应节点图标也将被选中。这可以很容易地看到哪些节点正在保存 - 哪些不是。

点击信息卡中的节点名称将选择它。如有必要，视点将自动平移，以便节点可见。

最后，您可以使用图例上方的颜色菜单为图形选择两种配色方案。默认的显示结构：当两个高层节点具有相同的结构时，它们以相同颜色出现。结构独特的节点是灰色的。第二个视图，它显示了不同操作运行的设备。名称范围与其内部操作的设备成比例。

下面的图片给出了例子。

<center class="half">
<img src="http://wx1.sinaimg.cn/mw690/af2d2659ly1fm4kgyk7epj20tq0h777t.jpg"  >
</center>


张量形状信息
---

当序列化的`GraphDef`包含张量形状时，图形可视化器将张量标注为边缘，边缘厚度反映总张量大小。 要在`GraphDef`中包含张量形状，在序列化图形时将实际图形对象（如`sess.graph`）传递给`FileWriter`。 下面的图片显示了具有张量形状信息的CIFAR-10模型：

<center class="half">
<img src="http://wx1.sinaimg.cn/mw690/af2d2659ly1fm4kgz1b12j20az050mxt.jpg"  >
</center>


运行时统计
---

收集运行时元数据通常是非常有用的，例如总内存使用量，总计算时间和节点的张量形状。 下面的代码示例是简单的MNIST教程的修改的训练和测试部分的一个片段，其中我们记录了摘要和运行时统计信息。 有关如何记录摘要的详细信息，请参阅摘要教程。 完整的源代码在这里。

```python
 # Train the model, and also write summaries.
  # Every 10th step, measure test-set accuracy, and write test summaries
  # All other steps, run train_step on training data, & add training summaries

  def feed_dict(train):
    """Make a TensorFlow feed_dict: maps data onto Tensor placeholders."""
    if train or FLAGS.fake_data:
      xs, ys = mnist.train.next_batch(100, fake_data=FLAGS.fake_data)
      k = FLAGS.dropout
    else:
      xs, ys = mnist.test.images, mnist.test.labels
      k = 1.0
    return {x: xs, y_: ys, keep_prob: k}

  for i in range(FLAGS.max_steps):
    if i % 10 == 0:  # Record summaries and test-set accuracy
      summary, acc = sess.run([merged, accuracy], feed_dict=feed_dict(False))
      test_writer.add_summary(summary, i)
      print('Accuracy at step %s: %s' % (i, acc))
    else:  # Record train set summaries, and train
      if i % 100 == 99:  # Record execution stats
        run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
        run_metadata = tf.RunMetadata()
        summary, _ = sess.run([merged, train_step],
                              feed_dict=feed_dict(True),
                              options=run_options,
                              run_metadata=run_metadata)
        train_writer.add_run_metadata(run_metadata, 'step%d' % i)
        train_writer.add_summary(summary, i)
        print('Adding run metadata for', i)
      else:  # Record a summary
        summary, _ = sess.run([merged, train_step], feed_dict=feed_dict(True))
        train_writer.add_summary(summary, i)
```

此代码将从步骤99开始每100步发出运行时统计信息。

当启动tensorboard并转到图表选项卡时，您将在“会话运行”下看到与添加运行元数据的步骤相对应的选项。 选择其中一个运行将显示在该步骤的网络快照，淡出未使用的节点。 在左侧的控件中，您可以通过总内存或总计算时间对节点着色。 此外，单击节点将显示确切的总内存，计算时间和张量输出大小。

<center class="half">
<img src="http://wx3.sinaimg.cn/mw690/af2d2659ly1fm4kgzet29j20tt0g2dja.jpg"  >
</center>