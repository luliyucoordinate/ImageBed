---
layout: post
title: 深度学习主机配置：Ubuntu17.04+1080ti+cuda9+cudnn7+tensorflow1.4/1.3
category : index
tags :  [Dell, Ubuntu, 1080ti, cuda, cudnn, tensorflow]
stickie: true
---

在此之前你应该已经装好了`Ubuntu17.04`，如果你对于装系统有什么疑问的话，请看这篇[Dell Alienware Aurora R6 （1080ti）安装Ubuntu17.04记录](http://blog.csdn.net/qq_17550379/article/details/78546850)

首先我们要先安装pip源

```
sudo apt-get install python-pip
```

接着cd到根目录，使用

```shell
ls -la
```

这个时候应该可以看到`.config`文件夹，进入这个文件夹（`cd .config`），建立一个pip文件夹（mkdir pip），进入pip文件夹（cd pip），接着建立`pip.conf`文件（vim pip.conf），按i（表示输入文本）输入以下内容

```shell
[global] 
index-url = https://pypi.tuna.tsinghua.edu.cn/simple 
```

输入`:wq`（保存并退出）。

以上步骤是要修改pip的源，这样安装会更加的快。

安装cuda9.0和cudnn7
---

去官网下载[cuda9.0安装包](https://developer.nvidia.com/cuda-release-candidate-download)

<a href="http://wx2.sinaimg.cn/mw690/af2d2659ly1fljn2fnj3aj20s90nj75p.jpg" data-lightbox="roadtrip">
<img src="http://wx2.sinaimg.cn/mw690/af2d2659ly1fljn2fnj3aj20s90nj75p.jpg" class="img-fluid">
</a>

按照上面说的安装步骤安装即可。

接着我们对cuda9下面的例子测试一下，以保证我们装好了cuda

现在桌面建立一个文件夹test，进入test文件夹（cd test）。使用下面的命令，将cuda例子文件复制进去

```shell
cp -r /usr/local/cuda-9.0/samples/ .
```

进入samples文件夹（cd samples），输入指令make，进行编译，编译要花很长时间。

编译好后，进入其中一个文件夹，我这里是进入了`cd ./1_Utilities/bandwidthTest`，接着输入

```shell
./bandwidthTest 
```

查看最后结果，如果是`Result = PASS`，那就ok。

接着cd到根目录。编辑`.bashrc文件`（vim  .bashrc，不过新装的系统好像没有这个文件，没有的话跳过这步），在文件结尾添加下面的语句

```shell
#cuda9.0
export PATH=/usr/local/cuda/bin${PATH:+:${PATH}} 
export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}} 
export CUDA_HOME=/usr/local/cuda
```

输入`:wq`（保存退出）。接着在命令窗口输入`source .bashrc`，让文件生效。

接着去官网下载[cudnn7安装文件](https://developer.nvidia.com/cudnn)，但是好像最近无法下载了，我有时间会上传一份。

下载好后输入下列指令将相关文件拷贝到cuda安装目录下即可。

```shell
tar -zxvf cudnn-9.0-linux-x64-v7.tgz 
sudo cp cuda/include/cudnn.h /usr/local/cuda/include/ 
sudo cp -a cuda/lib64/libcudnn* /usr/local/cuda/lib64/ 
sudo chmod a+r /usr/local/cuda/include/cudnn.h 
sudo chmod a+r /usr/local/cuda/lib64/libcudnn*
```

注意上面第二条指令，这里多加了一个`-a`，在官方给的方案里面没有，我建议你这样做，否则会出现连接出错的问题。如果你忘记了，可以参考下面做法

```shell
cd /usr/local/cuda/lib64/
sudo rm -rf libcudnn.so libcudnn.so.7.0  
sudo ln -s libcudnn.so.7.0.64 libcudnn.so.7.0  
sudo ln -s libcudnn.so.7.0 libcudnn.so  
```

其实是相同的道理。

安装tensorflow1.4
---

这是本次安装的重难点，因为tensorflow1.3/1.4对于cuda9并没有支持，所以安装中会出现一些问题。可行的办法有自己编译tensorflow文件进行安装，但是我不推荐你这样去做。

在github找到了别人编译好的cuda9补丁版[tensorflow1.4](https://github.com/mind/wheels/releases/tag/tf1.4-gpu-cuda9)，[**tensorflow-1.4.0-cp27-cp27mu-linux_x86_64.whl**](https://github.com/mind/wheels/releases/download/tf1.4-gpu-cuda9/tensorflow-1.4.0-cp27-cp27mu-linux_x86_64.whl)索性就拿来直接用。

使用这个之前，你要先安装mkl。在此之前你要确认你的cpu是否是以下系列之一

```
Intel Atom(R) processor with Intel(R) SSE4.1 support
4th, 5th, 6th and 7th generation Intel(R) Core processor
Intel(R) Xeon(R) processor E5 v3 family (code named Haswell)
Intel(R) Xeon(R) processor E5 v4 family (code named Broadwell)
Intel(R) Xeon(R) Platinum processor family (code name Skylake)
Intel(R) Xeon Phi(TM) product family x200 (code named Knights Landing)
Future Intel(R) Xeon Phi(TM) processor (code named Knights Mill)
```

如果不是，这个方法就可能不适用了，请使用编译tensorflow源码的办法。

如果cpu是其中的话，我们先要安装`git`

```shell
sudo apt-get install git
```

接着下载mkl的包

```shell
git clone https://github.com/01org/mkl-dnn.git
```

接着安装cmake和doxygen

```shell
sudo apt-get install Cmake
sudo apt-get install Doxygen
```

接着使用下面命令进入文件夹，下载相关文件

```shell
cd scripts && ./prepare_mkl.sh && cd ..
```

- 如果出错的话，你可以在这里[下载](https://github.com/01org/mkl-dnn/releases)，我这里下载的是[**mklml_lnx_2018.0.1.20171007.tgz**](https://github.com/01org/mkl-dnn/releases/download/v0.11/mklml_lnx_2018.0.1.20171007.tgz)

  现在之前下载好的mkl文件夹里面建立一个`external`文件夹。下载好现在的这个文件后解压（双击->提取），将加压后的文件夹里面的内容，copy到`external`文件夹中。

回到mkl目录下，接着建立一个bulid文件夹，进行编译

```shell
mkdir -p build && cd build && cmake .. && make
```

接着测试我们的编译文件是否有效，使用

```shell
sudo make test
```

接着生成doc文件

```shell
sudo make doc
```

最后安装

```shell
sudo make install
```

在此之前如果出现错误的话，可以使用`sudo+命令`再次尝试。

安装完成后，应该会有这样几个文件

共享库 (/*usr/local/lib*)：

- libiomp5.so
- libmkldnn.so
- libmklml_intel.so

标头文件 (/*usr/local/include*)：

- mkldnn.h
- mkldnn.hpp
- mkldnn_types.h

文档 (/*usr/local/share/doc/mkldnn*)：

- 英特尔许可和版权声明
- 构成 HTML 文档的各种文件（在 */reference/html* 之下）

cd到根目录。编辑`.bashrc`文件（vim .bahsrc，没有的话，跳过这步），和之前做法一样。在文件最后添加

```shell
#mkl
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
```

然后输入`:wq`退出，在命令窗口输入`source .bashrc`让文件生效。

接着我们开始安装tensorflow1.4，在此之前，先安装一个`libcupti-dev`库

```shell
sudo apt-get install libcupti-dev
```

接着先回到下载tensorflow的目录，就可以安装了

```shell
sudo pip install tensorflow-1.4.0-cp27-cp27mu-linux_x86_64.whl
```

装好后我们在python中（命令窗口输入python）测试一下

```shell
import tensorflow as tf
```

如果没有报错的话，就可以了。如果报错的话，例如

```python
ImportError: libmklml_intel.so: cannot open shared object file: No such file or directory
```

可能是你的mkl环境没有配置好。

如果有任何问题，请及时指出，我不想我的文章对大家造成误导，谢谢！！！^_^