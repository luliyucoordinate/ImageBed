---
layout: post
title: loki::allocator
category : cpp
tags : [cpp, stl]
stickie: true
---

Chunk
===

```c++
pData_: unsigned char*
firstAvailableBlock_: unsigned char//第一个可用的编号
blocksAvailable_: unsigned char//剩余可用的数目
```
```c++
void FixedAllocator::Chunk::Init(std::size_t blockSize,unsigned char blocks)
{
	pData = new unsigned char[blockSize * blocks];
	Reset(blockSize, blocks);
}
void FixedAllocator::Chunk::Reset(std::size_t blockSize,unsigned char blocks)
{
	firstAvailableBlock_ = 0;
	blocksAvailable_ = blocks;
	
	unsigned char i = 0;
	unsigned char* p = pData_;
	for(; i!=blocks; p+=blockSize)
		*p =++i;
}
void FixedAllocator::Chunk::Release()
{ 
	delete[] pData;
}
void FixedAllocator::Chunk::Allocate(std::size_t blockSize)
{
	if(!blocksAvailable_) return 0;
	unsigned char* pResult = 
		pData_ + (firstAvailableBlock_ * blockSize);
	firstAvailableBlock_ = *pResult;
	--blocksAvailable_;
	return pResult;
}
void FixedAllocator::Chunk::Deallocate(void* p,std::size_t blockSize)
{
	unsigned char * toRelease = static_cast<unsigned char*>(p);
	*toRelease = firstAvailableBlock_;
	firstAvailableBlock_ = static_cast<unsigned char>(
						(toRelease - pData_)/blockSize);
	++blocksAvailable_;		
}
```

FixedAllocator
===

```c++
chunks_:vector<Chunk>
allocChunk_: Chunk*
deallocChunk_: Chunk*
```
```c++
void *FixedAllocator::Allocate()
{
	if(allocChunk == 0 || allocChunk_->blocksAvailable_ == 0)
	{
		Chunks::iterator i = chunks_.begin();
		for(;; ++i)
		{
			if(i == chunks_.end())
			{
				chunks_.push_back(Chunk());
				Chunk& newChunk = chunks_.back();
				newChunk.Init(blockSize_, numBlocks_);
				allocChunk_ = &newChunk;//指向上次给出去的chunk
				deallocChunk_ = &chunks_.front();//指向上一次的回收
				break;
			}
			if(i->blocksAvailable_> 0)
			{
				allocChunk_ = &*i;
				break;
			}
		}
	}
	return allocChunk_->Allocate(blockSize_);
}
void FixedAllocator::Deallocate(void *p)
{
	deallocChunk_ = VicinityFind(p);
	DoDealllocate(p);
}
FixedAllocator::Chunk* FixedAllocator::VicinityFind(void *p)
{
	const std::size_t chunkLength = numBlocks_ * blockSize_;
	
	Chunk* lo = deallocChunk_;
	Chunk* hi = deallocChunk_ + 1;
	Chunk* loBound = &chunks_.front();
	Chunk* hiBound = &chunks_.back() + 1;
	for(;;)
	{
		if(lo)
		{
			if(p >= lo->pData_ && p< lo->pData_ + chunkLength)
			{
				return lo;
			}
			if(lo == loBound) lo = 0;
			else --lo;
		}
		if(hi)
		{
			if(p >= hi->pData_&& p <hi->pData_ + chunkLength)
			{
				return hi;
			}
			if( ++ hi == hiBound) hi = 0;
		}
	}
	return 0;
}
void FixedAllocator::DoDeallocate(void *p)
{
	deallocChunk_->Deallocate(p, blockSize_);
//是否等于开始的登记值
	if(deallocChunk_->blocksAvailable == numBlocks)
	{
		Chunk& lastChunk == chunks_.back();
//这里的做法与vc SBH defer类似
//__sbh_pHeaderDefer是一个指针，指向一个全回收group所属的Header。这个group原
//本应被释放，但暂时保留。当再有第二个全回收group出现时，SBH才释放Defer 
//group，并将新出现的全回收group设为defer。如果尚未出现第二个group而又从Defer 
//group取出block完成分配，Defer指针会被取消(设为NULL);
//__sbh_indGroupDefer是个索引，指出Region中哪个group是Defer。

		if(&lastChunk == deallocChunk_)
		{
			if(chunks_.size() >1 &&
				deallocChunk_[-1].blocksAvailable_ == numBlocks)
			{
				lastChunk.Release();
				chunks_.pop_back();
				allocChunk_ = deallocChunk_ = &chunks_.front();
			}
			return;
		}
		if(lastChunk.blocksAvailable == numBlocks)
		{
			lastChunk.Release();
			chunks_.pop_back();
			allocChunk_ = deallocChunk_;
		}
		else
		{
			std::swap(*deallocChunk_, lastChunk);
			allocChunk_ = &chunks_.back();
		}
	}
}
```

SmallObjAllocator
===
```c++
pool_: vector<FixedAllocator>
pLastAlloc: FixedAllocator
pLastDealloc: FixedAllocator
chunkSize: size_t
maxObjectSize: size_t
```