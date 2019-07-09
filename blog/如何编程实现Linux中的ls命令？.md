---
layout: post
title: 如何编程实现Linux中的ls命令？
category : linux
tags : [python, c, c++]
stickie: true
date: 2019-4-18 00:00:00
---

# 0x01 ls命令是什么？

我使用的系统环境是`Ubuntu 18.04`，通过`ls`命令我们可以知道当前目录下有哪些文件：

<center class="half">
    <img src="https://raw.githubusercontent.com/wiki/luliyucoordinate/ImageBed/ls/2019_4_19_1.jpg" width="600">
</center>

`ls`命令还有常用的参数：

- `-l`：列出文件的详细信息
- `-a`：列出包含`.`开头的文件
- `-s`：文件大小以块为单位打印
- `-t`：按时间排序输出
- `-F`：显示文件类型
- `-r`：逆序输出
- `-R`：递归输出
- `-q`：不排序输出

# 0x02 使用函数介绍

因为有读写文件操作，我们这里的操作主要有

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

## 0x0205 获取用户的passwd信息

所需的头文件

```c
#include <sys/types.h>
#include <pwd.h>
```

函数原型

```c
    struct passwd *getpwuid(uid_t uid);
```

`uid`就是我们的用户`ID`，返回的是一个`passwd`结构体指针

```c
struct passwd
{
  char *pw_name;                /* Username.  */
  char *pw_passwd;              /* Password.  */
  __uid_t pw_uid;               /* User ID.  */
  __gid_t pw_gid;               /* Group ID.  */
  char *pw_gecos;               /* Real name.  */
  char *pw_dir;                 /* Home directory.  */
  char *pw_shell;               /* Shell program.  */
};
```

## 0x0206 获取组ID信息

所需的头文件

```c
#include <sys/types.h>
#include <grp.h>
```

函数原型

```c
struct group *getgrgid(gid_t gid);
```

`gid`就是我们的组`ID`，返回的是一个`group`结构体指针

```c
struct group
{
    char *gr_name;              /* Group name.  */
    char *gr_passwd;            /* Password.    */
    __gid_t gr_gid;             /* Group ID.    */
    char **gr_mem;              /* Member list. */
};
```

# 0x03 编写一个ls

## 0x0301 第一版

```c
#include <stdio.h>
#include <sys/types.h>
#include <dirent.h>

void do_ls(char []);

void do_ls(char dirname[])
{
    DIR* dir_ptr;
    struct dirent* direntp;
    if ((dir_ptr = opendir(dirname)) == NULL)
    {
        fprintf(stderr, "ls1: cannot open %s\n", dirname);
    }
    else
    {
        while ((direntp = readdir(dir_ptr)) != NULL)
        {
            printf("%s\n", direntp->d_name);
        }
        closedir(dir_ptr);
    }
}

int main(int argc, char *argv[])
{
    if (argc == 1) do_ls(".");
    else
    {
        while (--argc)
        {
            printf("%s:\n", *(++argv));
            do_ls(*argv);
        }
    }
}
```

我们查看我们的版本和实际版本的区别

<center class="half">
    <img src="https://raw.githubusercontent.com/wiki/luliyucoordinate/ImageBed/ls/2019_4_19_2.jpg" width="600">
</center>

功能实现的还不错，输出的格式需要调整一下。我们的输出需要排序一下。`ls`并没有输出`.`开头的文件，需要在`-a`中。我们还要添加一个`-l`功能。

## 0x0302 第二版

我们首先看看`ls -l`会打印哪些信息

> $ ls -l
> total 24
> -rwxr-xr-x 1 lly lly 8568 4月  19 09:54 app
> -rw-r--r-- 1 lly lly  589 4月  19 09:52 ls.c
> -rw-r--r-- 1 lly lly 2256 4月  19 09:54 ls.o
> -rw-r--r-- 1 lly lly  249 4月  19 09:54 Makefile

每行包含`7`个字段，分别是`模式`，`链接数`，`文件所有者`，`文件所有组`，`文件大小`，`最后修改时间`和`文件名`，这些信息可以从`stat`获取。

我们先编写一个函数`show_stat_info`，看看能获取什么信息。

```c
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>

void show_stat_info(char *fname, struct stat* buf);

void show_stat_info(char *fname, struct stat* buf)
{
    printf("mode:%o\n", buf->st_mode);
    printf("links:%d\n", buf->st_nlink);
    printf("user:%d\n", buf->st_uid);
    printf("group:%d\n", buf->st_gid);
    printf("size:%d\n", buf->st_size);
    printf("modtime:%d\n", buf->st_mtime);
    printf("name:%s\n", fname);
}
int main(int argc, char *argv[])
{
    struct stat info;
    if (argc > 1)
    {
        if (stat(argv[1], &info) != -1)
        {
            show_stat_info(argv[1], &info);
            return 0;
        }
        else perror(argv[1]);
    }
    return 1;
}
```

查看我们现在获取的信息和`ls -l`获取的有什么不同

<center class="half">
    <img src="https://raw.githubusercontent.com/wiki/luliyucoordinate/ImageBed/ls/2019_4_19_3.jpg" width="600">
</center>

我们需要将`mode`转化为字符的形式，怎么转化？在`/usr/include/bits/stat.h`中找到下面信息

```c
#define __S_IFDIR       0040000 /* Directory.  */
#define __S_IFCHR       0020000 /* Character device.  */
#define __S_IFBLK       0060000 /* Block device.  */
#define __S_IFREG       0100000 /* Regular file.  */
#define __S_IFIFO       0010000 /* FIFO.  */
#define __S_IFLNK       0120000 /* Symbolic link.  */
#define __S_IFSOCK      0140000 /* Socket.  */
```

在`/usr/include/sys/stat.h`找到下面的一些宏函数

```c
#define S_ISDIR(mode)    __S_ISTYPE((mode), __S_IFDIR)
#define S_ISCHR(mode)    __S_ISTYPE((mode), __S_IFCHR)
#define S_ISBLK(mode)    __S_ISTYPE((mode), __S_IFBLK)
#define S_ISREG(mode)    __S_ISTYPE((mode), __S_IFREG)
#ifdef __S_IFIFO
# define S_ISFIFO(mode)  __S_ISTYPE((mode), __S_IFIFO)
#endif
#ifdef __S_IFLNK
# define S_ISLNK(mode)   __S_ISTYPE((mode), __S_IFLNK)
#endif
```

所以我们现在可以写一个`mode_to_letters`函数

```c
void mode_to_letters(int mode, char str[])
{
    strcpy(str, "----------");
    if (S_ISDIR(mode)) str[0] = 'd';
    if (S_ISCHR(mode)) str[0] = 'c';
    if (S_ISBLK(mode)) str[0] = 'b';

    if (mode & S_IRUSR) str[1] = 'r';
    if (mode & S_IWUSR) str[2] = 'w';
    if (mode & S_IXUSR) str[3] = 'x';

    if (mode & S_IRGRP) str[4] = 'r';
    if (mode & S_IWGRP) str[5] = 'w';
    if (mode & S_IXGRP) str[6] = 'x';

    if (mode & S_IROTH) str[7] = 'r';
    if (mode & S_IWOTH) str[8] = 'w';
    if (mode & S_IXOTH) str[9] = 'x';
}
```

ok，现在我们的`mode`问题解决了。接着我们看`user`和`group`和`bash`输出的不同。

我们知道用户的信息文件是放在了`/etc/passwd`，我们可以通过`getpwuid`获取该文件的信息。对于用户的组信息，我们可以通过`getgrgid`获取。我们可以很快写出两个获取信息的函数

```c
char *uid_to_name(uid_t uid)
{
    struct passwd* pw_ptr;
    static char numstr[10];

    if ((pw_ptr = getpwuid(uid)) == NULL)
    {
        sprintf(numstr, "%d", uid);
        return numstr;
    }else return pw_ptr->pw_name;
}

char *gid_to_name(gid_t gid)
{
    struct group* grp_ptr;
    static char numstr[10];

    if ((grp_ptr = getgrgid(gid)) == NULL)
    {
        sprintf(numstr, "%d", gid);
        return numstr;
    }
    else return grp_ptr->gr_name;
}
```

好的，至此基本功能实现了。我将代码放到了[GitHub Linux](https://github.com/luliyucoordinate/play-linux)上。

但是我们这个代码有一个问题就是没有显示记录总数，并且没有按文件名排序，也不支持选项`-a`。现有的函数也没法显示特殊文件格式`suid`、`sgid`和`sticky`。怎么添加`-R`功能？怎么添加`-r`功能？怎么添加`-q`功能？


## 0x0303 第三版

先处理一个简单的问题，添加特殊文件格式`suid`、`sgid`和`sticky`。

```c
void mode_to_letters(int mode, char str[])
{
    strcpy(str, "----------");
    if (S_ISDIR(mode)) str[0] = 'd';
    if (S_ISCHR(mode)) str[0] = 'c';
    if (S_ISBLK(mode)) str[0] = 'b';
    if (S_ISREG(mode)) str[0] = '-';
    if (S_IFIFO(mode)) str[0] = 'p';
    if (S_IFLNK(mode)) str[0] = 'l';
    if (S_IFSOCK(mode)) str[0] = 's';

    if (mode & S_IRUSR) str[1] = 'r';
    if (mode & S_IWUSR) str[2] = 'w';
    if (mode & S_IXUSR) str[3] = 'x';
    if (mode & S_ISUID) str[3] = 's';

    if (mode & S_IRGRP) str[4] = 'r';
    if (mode & S_IWGRP) str[5] = 'w';
    if (mode & S_IXGRP) str[6] = 'x';
    if (mode & S_ISGID) str[6] = 's';

    if (mode & S_IROTH) str[7] = 'r';
    if (mode & S_IWOTH) str[8] = 'w';
    if (mode & S_IXOTH) str[9] = 'x';
    if (mode & S_ISVTX) str[9] = 't';
}
```

**我将该问题的其他语言版本添加到了我的[GitHub Linux](https://github.com/luliyucoordinate/play-linux)**

**如有问题，希望大家指出！！！**
