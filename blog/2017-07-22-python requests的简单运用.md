---
layout: post
title: python requests的简单运用
category : python
tags : [python, requests]
stickie: true
---

0x01 无参数请求
---

```python
import requests
r = requests.get('http://www.baidu.com')
r = requests.post("http://httpbin.org/post")
r = requests.put("http://httpbin.org/put")
r = requests.delete("http://httpbin.org/delete")
r = requests.head("http://httpbin.org/get")
r = requests.options("http://httpbin.org/get")
```

0x02 在URL中传递参数
---

有时候我们要在URL中添加参数，例如百度搜索时word后面添加的搜索词

```python
payload = {'word': '黄皮子坟'}
r = requests.get("http://www.baidu.com/s", params=payload)
print r.url
```

结果为 http://www.baidu.com/s?word=%E9%BB%84%E7%9A%AE%E5%AD%90%E5%9D%9F

可以通过`r.text`来获取网页的内容

```python
print r.text
```

内容太多，这里就不打出来了，读者可以自己尝试。

可以通过`r.headers`来获取响应头内容。

```python
print r.headers
```

结果为{'BDQID': '0x8582eb7400002a8b', 'X-Powered-By': 'HPHP', 'Transfer-Encoding': 'chunked',...}

请求头内容可以用`r.request.headers`来获取

```
print r.request.headers
```
结果为{'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'User-Agent': 'python-requests/2.18.2'}

0x03 使用session
---

先初始化一个`session`对象，`s = requests.Session()`，然后使用这个`session`对象来进行访问，`r = s.post(url,data = user)`。

下面这个例子用来模拟登陆[V2EX](https://www.v2ex.com/)，问题的关键在于抓取post数据包

```python
import requests
from bs4 import BeautifulSoup

url = r"https://www.v2ex.com/signin"
v2ex_session = requests.Session()

f = v2ex_session.get(url)
soup = BeautifulSoup(f.content,"html.parser")
once = soup.find('input',{'name':'once'})['value']
u = soup.find('input',{'placeholder':'用户名或电子邮箱地址'})['name']
p = soup.find('input',{'type':'password'})['name']

user = {u:'username', p:'password', 'once': once, 'next': '/'}
v2ex_session.headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50"}
v2ex_session.headers.update({'referer': url})	#要注意这里referer
v2ex_session.post(url, data = user)
f = v2ex_session.get('http://www.v2ex.com/settings')
print f.content
```
0x04 cookie的使用
---

使用cookies解决登录问题

```python
cookies={}  
line = 'cookie的内容'	#抓包获取
for line in raw_cookies.split(';'):  
    key,value=line.split('=',1)	#1代表只分一次，得到两个数据  
    cookies[key]=value
url = r"https://www.v2ex.com/signin"
v2ex_session = requests.Session()
v2ex_session.headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50"}
v2ex_session.headers.update({'referer': url})	#要注意这里referer
f = v2ex_session.get(url,cookies=cookies)  
f = v2ex_session.get('http://www.v2ex.com/settings')
print f.content
```
但是貌似有出现了问题，因为网站使用的https连接

`http`和`https`的区别：

1.  url的前面是`https://`而不是`http://`，使用`ssl`进行加密/身份认证，并且`http`的默认端口是80，`https`的默认端口是443。
2.  因为有ssl的认证和加密，所以具体的底层的通信过程中会有不同，`https`的这一层在建立连接的时候，需要设置`socket`属性，`socket`属性的生成需要使用具体的方法调用，方法调用的参数需要指定：`ca_certs`=服务器端给提供的公钥证书即可。

然后如果还有客户端认证的话，那客户端也可以提供出自己的`key_file`，`cert_file`。

什么是ssl？

ssl的全称是(Secure Sockets Layer)安全套接层，另外还有TLS（Transport Layer Secure，传输层安全），这两种协议都是为网络提供安全和数据完整性的一种安全协议，在传输层对网络连接进行加密。

为什么要用这个？

防止数据以及网络连接的传输内容被截获，所以涉及到个人或者重要的信息等，都需要进行建立ssl连接，通过https的请求方式加密处理。