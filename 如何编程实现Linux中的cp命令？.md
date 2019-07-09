---
layout: post
title: 如何编程实现Linux中的cp命令？
category : linux
tags : [python, c, c++]
stickie: true
date: 2019-4-18 00:00:00
---

# 0x01 cp命令是什么？

`cp`最简单的操作就是复制文件。例如

```c
cp source target
```

如果`target`文件不存在，那么就创建它，如果已经存在就覆盖，最后`target`内容和`source`一致。

# 0x02 使用函数介绍

因为有读写文件操作，我们这里的操作主要有

## 0x0201 文件的读写操作

所需的头文件

```c
#include <unistd.h>
```

函数原型

```c
ssize_t read(int fd, void *buf, size_t count);
ssize_t write(int fd, const void *buf, size_t count);
```

`fd`表示我们读写操作对应的文件描述符，`buf`用来存放数据的缓冲区，`count`要读取和写入的字节数。返回值为实际读取和写入的字节数，出错返回`-1`。

## 0x0202 文件的创建

所需的头文件

```c
#include <fcntl.h>
```

函数原型

```c
int creat(const char *pathname, mode_t mode);
```

该函数等效于`open(pathname, O_WRONLY | O_CREAT | O_TRUNC, mode)`。

## 0x0203 获取文件信息

所需的头文件

```c
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
```

函数原型

```c
int stat(const char *pathname, struct stat *statbuf);
```

`pathname`指向我们需要获取的文件，`stat`是一个结构体包含文件信息。

```c
struct stat {
    dev_t     st_dev;         /* ID of device containing file */
    ino_t     st_ino;         /* Inode number */
    mode_t    st_mode;        /* File type and mode */
    nlink_t   st_nlink;       /* Number of hard links */
    uid_t     st_uid;         /* User ID of owner */
    gid_t     st_gid;         /* Group ID of owner */
    dev_t     st_rdev;        /* Device ID (if special file) */
    off_t     st_size;        /* Total size, in bytes */
    blksize_t st_blksize;     /* Block size for filesystem I/O */
    blkcnt_t  st_blocks;      /* Number of 512B blocks allocated */

    /* Since Linux 2.6, the kernel supports nanosecond
                  precision for the following timestamp fields.
                  For the details before Linux 2.6, see NOTES. */

    struct timespec st_atim;  /* Time of last access */
    struct timespec st_mtim;  /* Time of last modification */
    struct timespec st_ctim;  /* Time of last status change */

#define st_atime st_atim.tv_sec      /* Backward compatibility */
#define st_mtime st_mtim.tv_sec
#define st_ctime st_ctim.tv_sec
};
```

获取信息出错的话返回`-1`。

## 0x03 编写一个cp

## 0x0301 第一版

```c
include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

#define BUFFERSIZE 4096
#define COPYMODE   0644

void oops(char *, char *);

void oops(char *s1, char *s2)
{
    fprintf(stderr, "Error: %s", s1);
    perror(s2);
    exit(1);
}

int main(int argc, char *argv[])
{
    int in_fd, out_fd, n_chars;
    char buf[BUFFERSIZE];
    if (argc != 3)
    {
        fprintf(stderr, "usage: %s source destination\n", *argv);
        exit(1);
    }

    if ((in_fd = open(argv[1], O_RDONLY)) == -1)
    {
        oops("Cannot open", argv[1]);
    }

    if ((out_fd = creat(argv[2], COPYMODE)) == -1)
    {
        oops("Cannot creat". argv[2]);
    }

    while ((n_chars = read(in_fd, buf, BUFFERSIZE)) > 0)
    {
        if (write(out_fd, buf, n_chars) != n_chars)
        {
            oops("Write error to", argv[2]);
        }
    }

    if (n_chars == -1) oops("Read error from", argv[1]);

    if (close(in_fd) == -1 || close(out_fd) == -1)
    {
        oops("Error closing files", "");
    }
}
```

但是我们实现的这个`cp`非常简单，如果第二个参数是一个目录怎么办？

## 0x0302 第二版

如何解决第二个参数是一个目录的问题？问题具体为如何判断文件是一个目录？我们可以`stat`去查看`st_mode`

在`/usr/include/bits/stat.h`中找到下面信息

```c
#define __S_IFDIR       0040000 /* Directory.  */
```

在`/usr/include/sys/stat.h`找到下面的一些宏函数

```c
#define S_ISDIR(mode)    __S_ISTYPE((mode), __S_IFDIR)
```



**我将该问题的其他语言版本添加到了我的[GitHub Linux](https://github.com/luliyucoordinate/play-linux)**

**如有问题，希望大家指出！！！**
