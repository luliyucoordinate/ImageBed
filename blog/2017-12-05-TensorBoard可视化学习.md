---
layout: post
title: TensorBoard可视化学习
category : 机器学习
tags : [estimator, python, tensorflow]
stickie: true
---


您将使用TensorFlow进行的计算 - 如训练大量的深度神经网络 - 可能会很复杂且令人困惑。 为了便于理解，调试和优化TensorFlow程序，我们包含了一套名为TensorBoard的可视化工具。 您可以使用TensorBoard来显示您的TensorFlow图形，绘制关于图形执行的量化指标，并显示其他数据，如图像。 当完全配置TensorBoard时，看起来像这样：

<center class="half">
<img src="http://wx1.sinaimg.cn/mw690/af2d2659ly1fm4jyazdrfj20pw0dy77c.jpg"  >
</center>


序列化数据
---

TensorBoard通过读取TensorFlow事件文件进行操作，TensorFlow事件文件包含运行TensorFlow时可以生成的摘要数据。以下是TensorBoard中汇总数据的一般生命周期。

首先，创建您希望从中收集摘要数据的TensorFlow图，然后决定使用摘要操作注解哪些节点。

例如，假设您正在训练用于识别MNIST数字的卷积神经网络。您想记录学习率随时间的变化，以及目标函数如何变化。通过将`tf.summary.scalar` 操作分别附加到输出学习率和损失来收集这些信息。然后，给每个标量附上有意义的标签，如“学习率”或“损失函数”。

也许你也想看到特定层的激活分布，或梯度或权重的分布。通过将`tf.summary.histogram`操作附加到梯度输出和保存您权重的变量来收集这些数据。

有关所有可用摘要操作的详细信息，请查看有关摘要操作的文档。

在运行之前，TensorFlow中不会执行任何操作，或者取决于其输出的操作。我们刚刚创建的摘要节点是图形的外围设备：您当前正在运行的操作都不依赖于它们。所以，为了生成摘要，我们需要运行所有这些汇总节点。手工管理它们会很麻烦，所以使用`tf.summary.merge_all`将它们组合成一个单独的操作来生成所有的汇总数据。

然后，您可以运行合并的摘要操作，该操作将在给定的步骤中生成包含所有摘要数据的序列化的protobuf对象。最后，为了将这个总结数据写入磁盘，将总结的protobuf传递给`tf.summary.FileWriter`。

`FileWriter`在其构造函数中使用了一个`logdir` - 这个`logdir`非常重要，它是所有事件将被写出的目录。另外，`FileWriter`可以选择在其构造函数中使用Graph。如果它接收到一个Graph对象，那么TensorBoard会将您的图形与张量形状信息一起可视化。这将使您更好地理解图中流动的情况：请参阅张量形状信息。

现在你已经修改了你的图形，并有一个`FileWriter`，你已经准备好开始运行你的网络！如果你愿意，你可以每一步都运行合并的摘要操作，并记录大量的训练数据，虽然这可能产生更多的数据。所以请考虑每n步运行合并的摘要操作。

下面的代码示例是对简单MNIST教程的修改，我们在其中添加了一些汇总操作，并且每十步执行一次。如果你运行这个程序，然后启动`tensorboard --logdir = /tmp/tensorflow/mnist`，你将可以看到统计数据，例如训练过程中权重或精度的变化。下面的代码是摘录，完整的源代码在[这里](https://github.com/tensorflow/tensorflow/blob/r1.4/tensorflow/examples/tutorials/mnist/mnist_with_summaries.py)。

```python
def variable_summaries(var):
  """Attach a lot of summaries to a Tensor (for TensorBoard visualization)."""
  with tf.name_scope('summaries'):
    mean = tf.reduce_mean(var)
    tf.summary.scalar('mean', mean)
    with tf.name_scope('stddev'):
      stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
    tf.summary.scalar('stddev', stddev)
    tf.summary.scalar('max', tf.reduce_max(var))
    tf.summary.scalar('min', tf.reduce_min(var))
    tf.summary.histogram('histogram', var)

def nn_layer(input_tensor, input_dim, output_dim, layer_name, act=tf.nn.relu):
  """Reusable code for making a simple neural net layer.

  It does a matrix multiply, bias add, and then uses relu to nonlinearize.
  It also sets up name scoping so that the resultant graph is easy to read,
  and adds a number of summary ops.
  """
  # Adding a name scope ensures logical grouping of the layers in the graph.
  with tf.name_scope(layer_name):
    # This Variable will hold the state of the weights for the layer
    with tf.name_scope('weights'):
      weights = weight_variable([input_dim, output_dim])
      variable_summaries(weights)
    with tf.name_scope('biases'):
      biases = bias_variable([output_dim])
      variable_summaries(biases)
    with tf.name_scope('Wx_plus_b'):
      preactivate = tf.matmul(input_tensor, weights) + biases
      tf.summary.histogram('pre_activations', preactivate)
    activations = act(preactivate, name='activation')
    tf.summary.histogram('activations', activations)
    return activations

hidden1 = nn_layer(x, 784, 500, 'layer1')

with tf.name_scope('dropout'):
  keep_prob = tf.placeholder(tf.float32)
  tf.summary.scalar('dropout_keep_probability', keep_prob)
  dropped = tf.nn.dropout(hidden1, keep_prob)

# Do not apply softmax activation yet, see below.
y = nn_layer(dropped, 500, 10, 'layer2', act=tf.identity)

with tf.name_scope('cross_entropy'):
  # The raw formulation of cross-entropy,
  #
  # tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(tf.softmax(y)),
  #                               reduction_indices=[1]))
  #
  # can be numerically unstable.
  #
  # So here we use tf.nn.softmax_cross_entropy_with_logits on the
  # raw outputs of the nn_layer above, and then average across
  # the batch.
  diff = tf.nn.softmax_cross_entropy_with_logits(targets=y_, logits=y)
  with tf.name_scope('total'):
    cross_entropy = tf.reduce_mean(diff)
tf.summary.scalar('cross_entropy', cross_entropy)

with tf.name_scope('train'):
  train_step = tf.train.AdamOptimizer(FLAGS.learning_rate).minimize(
      cross_entropy)

with tf.name_scope('accuracy'):
  with tf.name_scope('correct_prediction'):
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
  with tf.name_scope('accuracy'):
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
tf.summary.scalar('accuracy', accuracy)

# Merge all the summaries and write them out to /tmp/mnist_logs (by default)
merged = tf.summary.merge_all()
train_writer = tf.summary.FileWriter(FLAGS.summaries_dir + '/train',
                                      sess.graph)
test_writer = tf.summary.FileWriter(FLAGS.summaries_dir + '/test')
tf.global_variables_initializer().run()
```

在初始化`FileWriters`之后，我们必须在我们训练和测试模型时将摘要添加到`FileWriters`。

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
    summary, _ = sess.run([merged, train_step], feed_dict=feed_dict(True))
    train_writer.add_summary(summary, i)
```

您现在已经可以使用TensorBoard将这些数据可视化了。

启动TensorBoard
---

要运行TensorBoard，请使用以下命令（或者使用`python -m tensorboard.main`）

```python
tensorboard --logdir=path/to/log-directory
```

其中`logdir`指向`FileWriter`序列化其数据的目录。 如果此`logdir`目录包含来自单独运行的序列化数据的子目录，则TensorBoard将可视化来自所有这些运行的数据。 一旦TensorBoard正在运行，浏览您的Web浏览器到`localhost:6006`以查看TensorBoard。

在看TensorBoard时，您会看到右上角的导航标签。 每个选项卡代表一组可以可视化的序列化数据。