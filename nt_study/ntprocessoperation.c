#include "ntddk.h"

NTSTATUS 
  ZwAllocateVirtualMemory(
    HANDLE  ProcessHandle,
    PVOID  *BaseAddress,
    ULONG  ZeroBits,
    PSIZE_T  RegionSize,
    ULONG  AllocationType,
    ULONG  Protect
    ); 

NTSTATUS MyOpenProcess(){
	NTSTATUS			Status;
	HANDLE				handle;
	OBJECT_ATTRIBUTES	ObjAttr;
	CLIENT_ID			ClientId;
	
	PVOID				AllocateAddr = NULL;
	size_t				RegionSize;
	
	memset(&ObjAttr,0,sizeof(OBJECT_ATTRIBUTES));
	
	ClientId.UniqueProcess = (HANDLE)1672;//test
	ClientId.UniqueThread  = 0;
	Status = ZwOpenProcess(
		&handle,
		FILE_ALL_ACCESS,
		&ObjAttr,
		&ClientId
	);
	if(!NT_SUCCESS(Status)){
		KdPrint(("openprocess failed."));
		return Status;
	}
	
	KdPrint(("addr:%X,vaddr:%X",(ULONG)handle,(ULONG)&AllocateAddr));

	RegionSize = 0xff;
	Status = ZwAllocateVirtualMemory(
		handle,
		&AllocateAddr,
		(ULONG_PTR)0,
		&RegionSize,
		MEM_COMMIT,
		PAGE_EXECUTE_READWRITE
	);
	if(!NT_SUCCESS(Status)){
		KdPrint(("allocate failed. code:%X",Status));
		return Status;
	}
	
	KdPrint(("addr:%X,size:%d",AllocateAddr,RegionSize));
	
	ZwClose(handle);
	return Status;
}

VOID MyDriverUnload(PDRIVER_OBJECT pDriverObject){
	KdPrint(("unload success."));
}

NTSTATUS DriverEntry(PDRIVER_OBJECT pDriverObject,PUNICODE_STRING pRegistryPath){
	MyOpenProcess();
    pDriverObject->DriverUnload = MyDriverUnload;
    return STATUS_SUCCESS;
}
