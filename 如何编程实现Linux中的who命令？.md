---
layout: post
title: 如何编程实现Linux中的who命令？
category : linux
tags : [python, c, c++]
stickie: true
date: 2019-4-18 00:00:00
---

# 0x00 who命令是什么？

我使用的系统环境是`Ubuntu 18.04`，通过`who`命令我们可以知道谁在使用系统：

<center class="half">
    <img src="https://raw.githubusercontent.com/wiki/luliyucoordinate/ImageBed/who/2019_4_18_1.png" width="600">
</center>

`who`命令还有其他`3`种形式：

- `who am i`，`who am I`，`whoami`

# 0x01 who命令是如何工作的？

我们可以从`unix`的帮助文档中（`man who`）找到**登录用户信息**

> If FILE is not specified, use /var/run/utmp.  /var/log/wtmp as FILE  is common.   If  ARG1  ARG2  given, -m presumed: 'am i' or 'mom likes' are usual.

从上述内容中，可以得知相关内容在`/var/run/utmp`文件中，不同的操作系统不一样。

我们可以在`/usr/include/bits/utmp.h`文件中查看到相关的文件信息。

```c
struct utmp
{
  short int ut_type;            /* Type of login.  */
  pid_t ut_pid;                 /* Process ID of login process.  */
  char ut_line[UT_LINESIZE]
    __attribute_nonstring__;    /* Devicename.  */
  char ut_id[4];                /* Inittab ID.  */
  char ut_user[UT_NAMESIZE]
    __attribute_nonstring__;    /* Username.  */
  char ut_host[UT_HOSTSIZE]
    __attribute_nonstring__;    /* Hostname for remote login.  */
  struct exit_status ut_exit;   /* Exit status of a process marked
                                   as DEAD_PROCESS.  */
/* The ut_session and ut_tv fields must be the same size when compiled
   32- and 64-bit.  This allows data files and shared memory to be
   shared between 32- and 64-bit applications.  */
#if __WORDSIZE_TIME64_COMPAT32
  int32_t ut_session;           /* Session ID, used for windowing.  */
  struct
  {
    int32_t tv_sec;             /* Seconds.  */
    int32_t tv_usec;            /* Microseconds.  */
  } ut_tv;                      /* Time entry was made.  */
#else
  long int ut_session;          /* Session ID, used for windowing.  */
  struct timeval ut_tv;         /* Time entry was made.  */
#endif

  int32_t ut_addr_v6[4];        /* Internet address of remote host.  */
  char __glibc_reserved[20];            /* Reserved for future use.  */
};
```

# 0x02 使用函数介绍

因为有读写文件操作，我们这里的操作主要有

## 0x0201 文件打开

所需要的头文件

```c
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
```

函数的格式

```c
int open(const char *pathname, int flags);
int open(const char *pathname, int flags, mode_t mode);
```

`pathname`参数是要打开或创建的文件名，和`fopen`一样，`pathname`既可以是相对路径也可以是绝对路径。`flags`参数有一系列常数值可供选择，可以同时选择多个常数用按位或运算符连接起来，所以这些常数的宏定义都以`O_`开头，表示`or`。`mode`表示我们创建文件时，赋予该文件的访问权限。常用`flags`选项

- `O_RDONLY`只读打开
- `O_RDWR`可读可写打开
- `O_WRONLY`只写打开
- `O_APPEND`表示追加。如果要打开的文件已有内容，那么此次打开文件写入的数据追加到文件末尾，不进行覆盖。
- `O_CREAT`表示如果文件不存在则创建它。要注意的是，使用该选项的话，我们需要同时提供第三个参数`mode`，也就是需要提供该文件的访问权限。
- `O_EXCL`常和`O_CREAT`一起使用（单独使用无意义），也就是打开文件的时候，如果文件已经存在，那么出错返回。
- `O_TRUNC`如果文件已经存在，并且以**只写**或**可读可写**方式打开，则将其长度截断为`0`。
- `O_NONBLOCK`对于设备文件，以`O_NONBLOCK`方式打开为非阻塞I/O。

## 0x0202 文件的读写操作

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

## 0x0203 文件的关闭操作

所需的头文件

```c
#include <unistd.h>
```

函数原型

```c
int close(int fd);
```

`fd`表示我们需要关闭文件的文件描述符，打开后的文件一定要关闭。关闭的过程中出现错误返回`-1`。

## 0x0204 关于时间的操作

所需头文件

```c
#include <time.h>
```

用到的函数

```c
struct tm *localtime(const time_t *timep);
```

`timep`是一个指向`time_t`类型的指针，而`time_t`实际上是一个整形数据。返回的是一个`tm`结构体指针

```c
struct tm {
               int tm_sec;    /* Seconds (0-60) */
               int tm_min;    /* Minutes (0-59) */
               int tm_hour;   /* Hours (0-23) */
               int tm_mday;   /* Day of the month (1-31) */
               int tm_mon;    /* Month (0-11) */
               int tm_year;   /* Year - 1900 */
               int tm_wday;   /* Day of the week (0-6, Sunday = 0) */
               int tm_yday;   /* Day in the year (0-365, 1 Jan = 0) */
               int tm_isdst;  /* Daylight saving time */
           };

```

通过`tm`结构体我们可以获取时间数据。

```c
size_t strftime(char *s, size_t max, const char *format,
                       const struct tm *tm);
```

`s`指向我们格式化时间字符串后的存储空间，`max`为该存储空间的大小。`format`表示我们按照什么格式进行转化，`tm`就是上面说的结构体。

## 0x03 编写一个who

## 0x0301 第一版

```c
#include <stdio.h>
#include <stdlib.h>
#include <utmp.h>
#include <fcntl.h>
#include <unistd.h>

int main()
{
    struct utmp current_record;
    int utmpfd;
    int reclen = sizeof current_record;
    if ((utmpfd = open(UTMP_FILE, O_RDONLY)) == -1)
    {
        perror(UTMP_FILE);
        exit(1);
    }

    while (read(utmpfd, &current_record, reclen) == reclen)
    {
        show_info(&current_record);
    }
    close(utmpfd);
    return 0;
}
```

我们需要写一个打印信息的函数`show_info`

```c
#define SHOWHOST

void show_info(struct utmp* utbufp)
{
    printf("%-8.8s", utbufp->ut_name);
    printf(" ");
    printf("%-8.8s", utbufp->ut_line);
    printf(" ");
#ifdef SHOWHOST
    printf("(%s)", utbufp->ut_host);
#endif
    printf("\n");
}
```

此时我们的结果是

> reboot   ~        (4.15.0-47-generic)
> lly      :0       (:0)
> runlevel ~        (4.15.0-47-generic)

而使用系统函数`who`的结果是

> lly      :0           2019-04-18 15:31 (:0)

我们需要完善我们的程序，也就是在打印函数`show_info`部分添加打印时间的功能。

## 0x0302 第二版

我使用的机器是`64`位的操作系统，通过查看`struct utmp`，我们知道时间是存在`struct timeval ut_tv; `中，我们现在需要查看`timeval`是个什么东西？`linux`不同版本位置不同，我是在`/usr/include/bits/types/struct_timeval.h`位置下找到的这个文件

```c
struct timeval
{
  __time_t tv_sec;              /* Seconds.  */
  __suseconds_t tv_usec;        /* Microseconds.  */
};
```

我们常用的时间操作类型是`time_t`，所以我们需要将`timeval`转化为`time_t`，然后通过调用`ctime`函数就可以得到真实时间。

我们可以写出`show_time`函数

```c
void show_time(struct timeval* utimep)
{
   struct tm* lt = localtime((time_t*)&(utimep->tv_sec));
   char str_time[100];
   strftime(str_time, sizeof str_time, "%Y-%m-%d %H:%M:%S", lt);
   printf("%s", str_time);
}
```

但是我们上面的代码依旧不好，因为我们每次值是读取一条数据，这显然非常低效率，怎么快速高效的读取多条记录呢？添加缓冲机制。

## 0x0303 第三版

我们可以编写一个缓冲区，设置缓冲区的大小可以容纳`16`个`utmp`结构体。

```c
#define NRECS 16
#define NULLUT ((struct utmp *)NULL)
#define UTSIZE (sizeof(struct utmp))

static char utmpbuf[NRECS * UTSIZE];
static char num_recs;
static int cur_rec;
static int fd_utmp = -1;

utmp_open(char *filename)
{
    fd_utmp = open(filename, O_RDONLY);
    cur_rec = num_recs = 0;
    return fd_utmp;
}

struct utmp* utmp_next()
{
    if (fd_utmp == -1) return NULLUT;
    if (cur_rec == num_recs && utmp_reload() == 0) return NULLUT;

    struct utmp* recp = (struct utmp*)&utmpbuf[cur_rec * UTSIZE];
    ++cur_rec;
    return recp;
}

int utmp_reload()
{
    int amt_read = read(fd_utmp, utmpbuf, NRECS * UTSIZE);
    num_recs = amt_read/UTSIZE;
    cur_rec = 0;
    return num_recs;
}

void utmp_close()
{
    if (fd_utmp != -1) close(fd_utmp);
}
```

我们的主函数需要稍加修改

```c
int main()
{
    struct utmp *utbufp, *utmp_next();

    if (utmp_open(UTMP_FILE) == -1)
    {
        perror(UTMP_FILE);
        exit(1);
    }

    while ((utbufp = utmp_next()) != NULL)
    {
        show_info(utbufp);
    }
    utmp_close();
    return 0;
}
```

**我将该问题的其他语言版本添加到了我的[GitHub Linux](https://github.com/luliyucoordinate/play-linux)**

**如有问题，希望大家指出！！！**
