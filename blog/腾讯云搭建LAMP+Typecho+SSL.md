---
layout: post
title: 腾讯云Ubuntu 16.04搭建LAMP+Typecho+SSL（超详细！！！）
category : Linux编程
tags : [python, c, c++]
stickie: true
icon: note
date: 2019-4-18 00:00:00
---

# 0x01 搭建LAMP

**安装Apache:**  `sudo apt-get install apache2`

**安装mqsql:**   `sudo apt-get install mysql-server`

**安装php及相关组件:**

`sudo apt install php php-dev php-curl php-pear php-mysql libapache2-mod-php php-mcrypt php-gd php-mbstring php-pdo php-sqlite3`

# 0x02 部署Typecho

首先获取`Typecho`的软件包

```shell
wget -d http://typecho.org/downloads/1.1-17.10.30-release.tar.gz
```

首先解压文件，然后将其中`build`目录下的所有文件拷贝到`/var/www`目录中，注意此时目录中可能有`html`文件夹，我们先将它删除

```shell
cd /var/www
sudo rm -rf html
```

接着修改配置文件

```shell
sudo apt install vim
sudo vim /etc/apache2/sites-available/000-default.conf
```

将其中`DocumentRoot`修改为如下

```shell
<VirtualHost *:80>
...
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www		#alter
```

接着重启`apache2`服务

```shell
sudo service apache2 restart
```

接着创建数据库

```shell
mysql -uroot -p
create database 数据库名;
quit;
```

现在我们就可以通过`http://localhost/install.php `安装`Typecho`了。

<center class="half">
    <img src="https://raw.githubusercontent.com/wiki/luliyucoordinate/ImageBed/LAMPTypecho/2019_7_6_1.png" width="600">
</center>

# 0x03部署SSL

腾讯免费ssl证书获取链接：[https://console.cloud.tencent.com/ssl](https://console.cloud.tencent.com/ssl)
**注意**：申请时若未在腾讯云上进行实名认证，则会先跳转到实名认证。

下面为免费申请页面，默认可以使用1年。

<center class="half">
    <img src="https://raw.githubusercontent.com/wiki/luliyucoordinate/ImageBed/LAMPTypecho/2019_7_6_2.png" width="700">
</center>

点击确定之后，进入如下页面，其中通用名称就是你的域名，申请邮箱就是你申请域名时使用的邮箱。

<center class="half">
    <img src="https://raw.githubusercontent.com/wiki/luliyucoordinate/ImageBed/LAMPTypecho/2019_7_6_3.png" width="700">
</center>

点击下一步，进入到手动DNS验证或者文件验证页面，本文使用的是手动DNS验证，具体的操作步骤可以点击“详细说明”查看。

<center class="half">
    <img src="https://raw.githubusercontent.com/wiki/luliyucoordinate/ImageBed/LAMPTypecho/2019_7_6_4.png" width="700">
</center>

点击“确定”之后，会显示带验证的DNS的基本信息。

<center class="half">
    <img src="https://raw.githubusercontent.com/wiki/luliyucoordinate/ImageBed/LAMPTypecho/2019_7_6_5.png" width="700">
</center>

上图中，主机记录、记录类型TXT，和记录值需要填写到你备案域名的地方。本文的域名是在阿里云申请的，因此需要在阿里云的域名记录中添加一条TXT记录。

本文实验的域名是在阿里云上申请的。进入阿里云控制台，域名列表=》点击对应域名的“解析”

<center class="half">
    <img src="https://raw.githubusercontent.com/wiki/luliyucoordinate/ImageBed/LAMPTypecho/2019_7_6_6.png" width="700">
</center>

进入到“解析设置”页面，添加解析

<center class="half">
    <img src="https://raw.githubusercontent.com/wiki/luliyucoordinate/ImageBed/LAMPTypecho/2019_7_6_7.png" width="700">
</center>

下面记录类型选择**TXT，主机记录、记录值**即为上述生成的内容。然后确定即可。

<center class="half">
    <img src="https://raw.githubusercontent.com/wiki/luliyucoordinate/ImageBed/LAMPTypecho/2019_7_6_8.png" width="700">
</center>

添加TXT记录之后，大概5min之内就能审核通过，然后登陆腾讯云，就可以下载SSL证书了。

<center class="half">
    <img src="https://raw.githubusercontent.com/wiki/luliyucoordinate/ImageBed/LAMPTypecho/2019_7_6_9.png" width="700">
</center>

证书审核通过之后，下载证书文件，解压之后会有以下几种类型web服务器的证书：

<center class="half">
    <img src="https://raw.githubusercontent.com/wiki/luliyucoordinate/ImageBed/LAMPTypecho/2019_7_6_10.png" width="500">
</center>

将下载的证书解压，在`apache`目录中会有三个文件`1_root_bundle.crt 2_xxx.crt 3_xxx.key`

<center class="half">
    <img src="https://raw.githubusercontent.com/wiki/luliyucoordinate/ImageBed/LAMPTypecho/2019_7_6_11.png" width="300">
</center>

将这三个文件上传到服务器的`/etc/httpd/ssl/`目录，如果这个目录没有的话，新建一个

```shell
sudo mkdir -p /etc/httpd/ssl
scp apache name@ip:~/
sudo cp apache/* /etc/httpd/ssl/
```
**注意**：`scp`实在本地操作，需要输入服务器的用户名`name`和外网`ip`。

开启`ssl`模块

```shell
sudo a2enmod ssl
```

查看`/etc/apache2/ports.conf`文件中，是不是包含（没有的话，添加）

```shell
Listen 80
Listen 443
```

接着我们需要创建软连接，同时删除`etc/apache2/sites-enabled/site-enabled`目录下的`000-default.conf`链接文件

```shell
sudo ln -s /etc/apache2/sites-available/default-ssl.conf /etc/apache2/sites-enabled/default-ssl.conf
sudo rm /etc/apache2/sites-enabled/000-default.conf
```

接着配置`default-ssl.conf`这个文件

```shell
sudo vim /etc/apache2/sites-enabled/default-ssl.conf
```

<center class="half">
    <img src="https://raw.githubusercontent.com/wiki/luliyucoordinate/ImageBed/LAMPTypecho/2019_7_6_12.png" width="600">
</center>

修改红框位置。

```
SSLCertificateFile  证书地址/2_xxx.crt
SSLCertificateKeyFile 证书地址/3_xxx.key
SSLCertificateChainFile 证书地址/1_root_bundle.crt
```

其中`证书地址`就是我们建立的文件夹`/etc/httpd/ssl/`

接着我们配置`http`重定向为`https`

```shell
sudo a2enmod rewrite 
```

接着配置`/etc/apache2/apache2.conf`文件，在文件的末尾添加

```
<Directory "/var/www">
# 新增
RewriteEngine on
RewriteCond %{SERVER_PORT} !^443$
RewriteRule ^(.*)?$ https://%{SERVER_NAME}%{REQUEST_URI} [L,R]
</Directory>
```

最后重启`apache2`服务

```shell
sudo service apache2 restart
```

最后设置站点地址为`https://...`即可

<center class="half">
    <img src="https://raw.githubusercontent.com/wiki/luliyucoordinate/ImageBed/LAMPTypecho/2019_7_6_13.png" width="600">
</center>

reference:

https://blog.csdn.net/Victor_zero/article/details/83154519

https://www.jianshu.com/p/ba8eddc73bb2
