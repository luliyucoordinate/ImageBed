---
layout: post
title: Dell Alienware Aurora R6（1080ti）安装Ubuntu17.04记录
category : index
tags :  [Dell, Ubuntu]
stickie: true
---

写这篇文章的时候，我内心是非常舒畅的，电脑是昨天下午到的，今天终于把Ubuntu17.04配置好了。希望我这篇文章对各位有一些启发。

首先我要强调，网络上的一些指导性教程都是有时限的，也就是说可能对你的机器不适用，但是如果你理解了其中的原理的话，万变不离其宗！！！

bios的设置
---

先说一下第一个比较头疼的问题，bios的设置（我这里是F2打开）。`secure boot`选项要设置为`disabled`，至少我是这样做的，我后来也没有测试设置成`enabled`会有什么问题。这一点我保留意见，大家可以自己尝试一下。

接下来是关于`uefi`和`legacy`的问题，很多教程中都是使用`legacy`，但是经过我的尝试，我这里选择`uefi`，`uefi`是一种新的装机手法，而`legacy`是老的。所以对于那些10年之后的电脑，我强烈推荐你使用`uefi`。

接着是`AHCI`和`RAID`的问题，对于双硬盘的主机都可能会面对的问题。如果你要安装`ubuntu`的话，必须使用`AHCI`。

别的都不变，save and reset。


做`ubuntu`系统盘
---

因为我在bios中设置了`uefi`，所以我这里使用[rufus](http://rufus.akeo.ie/)这个工具。如果你使用`legacy`（我不推荐你这样去做），可以使用软碟通这个工具。

<a href="http://wx3.sinaimg.cn/mw690/af2d2659ly1fliw4p6r5lj20cs0hztbb.jpg" data-lightbox="roadtrip">
<img src="http://wx3.sinaimg.cn/mw690/af2d2659ly1fliw4p6r5lj20cs0hztbb.jpg" class="img-fluid">
</a>

这里主要的问题之第二个选项，按照图上去选就可以了。为什么？这里我要说一说`GPT`分区和`MBR`分区，如果你前面选择的是`uefi`，那么这里就是用`GPT`。具体区别看[这篇](http://www.chinaz.com/server/2016/1017/595444.shtml)。

我这里是使用`winPE`工具把两个硬盘都设置为`GPT`分区（如果使用`winPE`的话，你要先把`uefi`改为`legacy`。然后`save and reset`后，在bios中就可以看到启动顺序，将u盘设置为第一启动）

接着再改回`uefi` 并且`save and reset`，进bios设置u盘第一启动。如果这个时候你看不到u盘选项的话，我这里是按F12打开一个类似于bios的东西（不同电脑不同），它里面有bios选项，也有u盘选项，选中u盘，然后回车装机。

安装ubuntu17.04
---

我推荐你使用新版本的`Ubuntu`，因为在硬件驱动方面，它会好很多。

首先你要把下你的独立显卡，一定要这样做，当然网上有用`nomodeset`这种方式的，我也尝试了，但是由于某些问题，一开始没弄好，所以如果你的电脑是有`核心显卡`的或者有亮机卡，我推荐你就我的方法这样做吧。

先将显示器插在`核心显卡`上，接着装系统。这个时候我们面对一个问题，系统是装在机械硬盘上还是固态硬盘上。我一开始把系统装在固态上，但是开机总是出现`boot failure`的问题。为什么？`PCIe M.2`固态硬盘目前驱动方面会有问题，我查到有人在这种固态上成功了安装`ubuntu17.04`（装[NVME drive is by Liteon](https://community.dell.com/thread/24162-alienware-aurora-r6-booting-linux-on-pcie-m2)，但我不知道怎么去做），但是当时我整个人都很不好，所以没有去尝试。所以你也不想尝试的话，就装在机械上吧。

装`Linux`系统，如果不清楚各个分区的作用的话，你就选择默认安装选项吧，不要自己去设置各个分区了。接着很顺利的装好了`Ubuntu17.04`。

进入系统后，你应该先在系统选项中，选择更新中设置更新源是中国服务器，我选择了`aliyun`。我不推荐你，通过编辑文件的方式修改源（当然你可以这样做），还是让问题更加的简单吧！！！

我推荐你先安装`vim`，因为我觉得`vi`不怎么好用

```shell
sudo apt-get install vim
```

接着去禁用nouveau驱动（这是一个开源的驱动，对nvidia显卡不支持）

```shell
sudo vim /etc/modprobe.d/blacklist-nouveau.conf
```

在后面添加

```shell
blacklist nouveau
```

接着更新一下

```shell
sudo update-initramfs -u
```

**修改之后需要重启系统**。

重启后可以使用以下命令： 

```shell
lsmod | grep nouveau
```

如果什么都没有的话，禁用成功。我这里要说的是，大家都这样做了，所以我这样做了，但是如果不禁用会不会有问题，我不知道（有人说没问题）。

先进入文本模式（Ctrl+Alt+F1），接着使用这条指令，添加一个源

```shell
sudo add-apt-repository ppa:graphics-drivers/ppa
```

关闭图形化窗口

```shell
sudo service lightdm stop
```

先更新一下，因为我们添加了一个源

```shell
sudo apt-get update
```

使用这个命令下载安装驱动（我的显卡是1080ti所以使用384，具体数字自己去查查）

```shell
sudo apt-get install nvidia-384
```

安装过程中，可能下载会出现一些问题（突然中断），这个时候，你要等他结束，然后根据错误提示操作（我这里不记得当时的操作是什么了），然后再次使用上面的指令`sudo apt-get install nvidia-384`。如果没有发生，那就更好了。

装好后，恢复图形环境

```shell
sudo service lightdm start
```

Ctrl+Alt+F7进入图形界面，关机。

将独立显卡插上，将视屏线插在独显上，开机，这个时候你会发现，系统可以打开了，不再是黑屏。

进入系统后，输入下面指令

```shell
nvidia-smi
```

如果没有出现报错，那么恭喜你ubuntu装好了。

我这里还有一个小问题，就是在关机的时候，会卡死在关机界面，关不了机，只能长按电源键关机。怎么解决这个问题，等我搞定了再写。

下一篇讲介绍[深度学习主机配置：Ubuntu17.04+1080ti+cuda9+cudnn7+tensorflow1.4/1.3]()

如果有任何问题，请及时指出，我不想我的文章对大家造成误导，谢谢！！！^_^