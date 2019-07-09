---
layout: post
title: malloc/free
category : cpp
tags : [cpp, stl]
stickie: true
---

SBH(small block heap)
===
_heap_init() 和__sbh_heap_init()
---
CRT为自己建立一个__crtheap，然后从中配置SBH所需的headers，regions作为管理用。

```c++
int _cdecl_heap_init(int mtflag)
{
	if(( _crtheap = HeapCreate( mtflag?0: HEAP_NO_SERIALIZE,
					BYTES_PER_PAGE, 0 )) == NULL)
	{
		return 0;
	}
	if( __sbh_heap_init() == 0)
	{
		HeapDestory(_crtheap);
	}
	return 1;
}

#define nNoMansLandSize 4
typedef struct _CrtMemBlockHeader
{
	struct _CrtMemBlockHeader *pBlockHeaderNext;
	struct _CrtMemBlockHeader *pBlockHeaderPrev;
	char *szFilename;//指向的文件名ioinit.c
	int nLine;//上面文件的第几行,81行
	size_t nDataSize;//客户要的内存大小
	int nBlockUse;//memory block
	long IRequest;
	unsigned char gap[nNoMansLandSize];
	/*followed by:
	*unsigned char data[nDataSize];
	*unsigned char anothergap[nNoMansLandSize];
	*/
}_CrtMemBlockHeader;
```
至此我们终于知道了，在debug模式下，分配的内存块中多出来的部分

关于第一块内存的分配
---
```c++
typedef struct tagRegion
{
	int indGroupUse;//0xffffffff，用于分割
	char cntRegionSize[64];
	BITVEC bitvGroupHi[32];
	BITVEC bitvGroupLo[32];
	struct tagGroup grpHeadList[32];
}REGION, *PREGION;
typedef struct tagGroup
{
	int cntEntries; //记录分配次数，每分配一次加一，回收减一
	struct tagListHead listHead[64];
}GROUP, *PGROUP;
typedef struct tagListHead
{
	struct tagEntry *pEntryNext;
	struct tagEntry *pEntryPrev;
}LISTHEAD, *PLISTHEAD;
typedef struct tagEntry
{
	int sizeFront;
	struct tagEntry *pEntryNext;
	struct tagEntry *pEntryPrev;
}ENTRY, *PENTRY;
```

归还操作系统
---
__sbh_pHeaderDefer是一个指针，指向一个全回收group所属的Header。这个group原本应被释放，但暂时保留。当再有第二个全回收group出现时，SBH才释放Defer group，并将新出现的全回收group设为defer。如果尚未出现第二个group而又从Defer group取出block完成分配，Defer指针会被取消(设为NULL);  
__sbh_indGroupDefer是个索引，指出Region中哪个group是Defer。

```c++
int __cdecl__sbh_heap_init(void)
{
	if(! (__sbh_pHeaderList = HeapAlloc(crtheap,0,16*sizeof(HEADER)))
		return FALSE;
	__sbh_pHeaderScan = __sbh_pHeaderList;
	__sbh_pHeaderDefer = NULL;
	__sbh_cntHeaderList = 0;
	__sbh_sizeHeaderList = 16;
 	
    return TRUE;
}
```
