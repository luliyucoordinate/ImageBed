---
layout: post
title: 	Centos6升级Python2.7安装setuptools及pip
category : python
tags : [python, pip, 转载]
stickie: true
---

转自[Centos6升级Python2.7安装setuptools及pip](http://blog.csdn.net/future_ins/article/details/53198717)

yum install -y zlib-devel bzip2-devel xz-libs xz wget git tar gcc gcc-c++ openssl openssl-devel pcre-devel python-devel libevent automake autoconf libtool make git
wget http://www.python.org/ftp/python/2.7.9/Python-2.7.9.tar.xz
xz -d Python-2.7.9.tar.xz
tar -xvf Python-2.7.9.tar
cd Python-2.7.9
./configure --prefix=/usr/local
make && make altinstall
mv /usr/bin/python /usr/bin/python2.6.6
ln -s /usr/local/bin/python2.7 /usr/bin/python

wget --no-check-certificate https://pypi.python.org/packages/source/s/setuptools/setuptools-1.4.2.tar.gz
tar -xvf setuptools-1.4.2.tar.gz
cd setuptools-1.4.2
python2.7 setup.py install

wget --no-check-certificate https://pypi.python.org/packages/source/p/pip/pip-6.0.7.tar.gz
tar zxvf pip-6.0.7.tar.gz
cd pip-6.0.7
python setup.py install
