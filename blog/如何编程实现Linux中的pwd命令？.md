---
layout: post
title: 如何编程实现Linux中的pwd命令？
category : linux
tags : [python, c, c++]
stickie: true
date: 2019-4-20 00:00:00
---

# 0x00 pwd命令是什么？

`pwd`用来显示到达当前目录的路径。

# 0x01 pwd命令是如何工作的？

我们知道一个目录下包含了两个特殊的目录`.`和`..`分别表示当前目录和上一个目录。我们可以先找到`.`的`inode`节点编号，然后回到上一级目录，通过`inode`节点编号获取该目录的名字。

什么时候递归结束呢？当然是到达目录树的顶端了。当到达树的顶端的时候，`.`和`..`的`inode`编号相同。

# 0x02 使用函数介绍

我们这里的操作主要有

## 0x0201 目录打开

所需要的头文件

```c
#include <sys/types.h>
#include <dirent.h>
```

函数的格式

```c
DIR *opendir(const char *name);
```

`name`指向我们需要打开的目录，返回的是一个`DIR`结构体指针（可以理解为“目录描述符”）。

## 0x0202 目录的读操作

所需要的头文件

```c
#include <dirent.h>
```

函数的格式

```c
struct dirent *readdir(DIR *dirp);
```

`dirp`指向我们的目录描述符，返回的是一个`dirent`结构体。

```c
struct dirent {
    ino_t          d_ino;       /* Inode number */
    off_t          d_off;       /* Not an offset; see below */
    unsigned short d_reclen;    /* Length of this record */
    unsigned char  d_type;      /* Type of file; not supported
                                              by all filesystem types */
    char           d_name[256]; /* Null-terminated filename */
};
```

我们可以通过`d_name`获取目录中的文件信息。

## 0x0203 目录的关闭操作

所需的头文件

```c
#include <sys/types.h>
#include <dirent.h>
```

函数原型

```c
int closedir(DIR *dirp);
```

`dirp`指向我们的目录描述符，关闭的过程中出现错误返回`-1`。

## 0x0204 获取文件信息

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

## 0x0205 改变目录位置

所需的头文件

```c
#include <unistd.h>
```

函数原型

```c
int chdir(const char *path);
```

`path`指向我们需要改变的目录位置。

# 0x03 编写一个pwd

## 0x0301 第一版

```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <string.h>
#include <unistd.h>

void printpathto(ino_t);
void inum_to_name(ino_t inode_to_find, char *namebuf, int buflen);
ino_t get_inode(char *filename);

void printpathto(ino_t this_inode)
{
    ino_t my_inode;
    char its_name[BUFSIZ];
    if (get_inode("..") != this_inode)
    {
        chdir("..");
        inum_to_name(this_inode, its_name, BUFSIZ);
        my_inode = get_inode(".");
        printpathto(my_inode);
        printf("/%s", its_name);
    }
}

void inum_to_name(ino_t inode_to_find, char *namebuf, int buflen)
{
    DIR *dir_ptr;
    struct dirent *direntp;
    dir_ptr = opendir(".");
    if (dir_ptr == NULL)
    {
        perror(".");
        exit(1);
    }

    while ((direntp = readdir(dir_ptr)) != NULL)
    {
        if (direntp->d_ino == inode_to_find)
        {
            strncpy(namebuf, direntp->d_name, buflen);
            namebuf[buflen - 1] = '\0';
            closedir(dir_ptr);
            return;
        }
    }    
    fprintf(stderr, "error looking for inum %ld\n", inode_to_find);
    exit(1);
}

ino_t get_inode(char *filename)
{
    struct stat info;
    if (stat(filename, &info) == -1)
    {
        fprintf(stderr, "Cannot stat");
        perror(filename);
        exit(1);
    }
    return info.st_ino;
}
int main()
{
    printpathto(get_inode("."));
    putchar('\n');
    return 0;
}
```

我们查看我们的版本和实际版本的区别

<center class="half">
    <img src="https://raw.githubusercontent.com/wiki/luliyucoordinate/ImageBed/pwd/2019_4_20_1.png" width="700">
</center>

功能实现的还不错，但是我们没有递归到`home`目录。是代码问题吗？不是，因为`unix`允许一个磁盘的存储由多棵树构成，每个磁盘或磁盘上的每个分区都包含一颗目录树。

**我将该问题的其他语言版本添加到了我的[GitHub Linux](https://github.com/luliyucoordinate/play-linux)**

**如有问题，希望大家指出！！！**
