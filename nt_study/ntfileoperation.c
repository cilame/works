#include "ntddk.h"

NTSTATUS MyCreateFile(wchar_t *strpath){
	HANDLE				hFile;
	UNICODE_STRING		FileName;
	OBJECT_ATTRIBUTES	FileObjAttr;
	IO_STATUS_BLOCK		IoStatusBlock;
	
	NTSTATUS			Status;
	
	RtlInitUnicodeString(&FileName,strpath);
	memset(&FileObjAttr,0,sizeof(OBJECT_ATTRIBUTES));
	InitializeObjectAttributes(&FileObjAttr,&FileName,OBJ_CASE_INSENSITIVE,NULL,NULL);
	
	Status = ZwCreateFile(
		&hFile,
		GENERIC_ALL,
		&FileObjAttr,
		&IoStatusBlock,
		NULL,
		FILE_ATTRIBUTE_NORMAL,
		FILE_SHARE_READ,
		FILE_OPEN_IF,
		FILE_NON_DIRECTORY_FILE,
		NULL,
		0
	);
	if (!NT_SUCCESS(Status)){
		return Status;
	}
	KdPrint(("createfile success."));
	ZwClose(hFile);
	return Status;
}

NTSTATUS MyCreateKey(wchar_t *regkey){
	HANDLE				hReg;
	UNICODE_STRING		FileName;
	OBJECT_ATTRIBUTES	ObjAttr;
	NTSTATUS			Status;
	ULONG				Disposition;
	
	RtlInitUnicodeString(&FileName,regkey);
	memset(&ObjAttr,0,sizeof(OBJECT_ATTRIBUTES));
	InitializeObjectAttributes(&ObjAttr,&FileName,OBJ_CASE_INSENSITIVE,NULL,NULL);
	
	Status = ZwCreateKey(
		&hReg,
		KEY_ALL_ACCESS,
		&ObjAttr,
		0,
		NULL,
		REG_OPTION_NON_VOLATILE,
		&Disposition
	);
	if (!NT_SUCCESS(Status)){
		KdPrint(("createkey failed. code:%X",Status));
		return Status;
	}
	KdPrint(("createkey success"));
	ZwClose(hReg);
	return Status;
}

HANDLE MyOpenKey(wchar_t *regkey){
	HANDLE				hReg;
	UNICODE_STRING		FileName;
	OBJECT_ATTRIBUTES	ObjAttr;
	NTSTATUS			Status;
	ULONG				Disposition;
	
	RtlInitUnicodeString(&FileName,regkey);
	memset(&ObjAttr,0,sizeof(OBJECT_ATTRIBUTES));
	InitializeObjectAttributes(&ObjAttr,&FileName,OBJ_CASE_INSENSITIVE,NULL,NULL);
	
	Status = ZwOpenKey(
		&hReg,
		GENERIC_ALL,
		&ObjAttr
	);
	if (!NT_SUCCESS(Status)){
		KdPrint(("openkey failed. code:%X",Status));
		return (HANDLE)0;
	}
	KdPrint(("openkey success"));
	return hReg;
}

NTSTATUS MySetValueKey(wchar_t *regkey,wchar_t *regname,PVOID value){
	HANDLE				hReg;
	UNICODE_STRING		RegKey,RegName;
	OBJECT_ATTRIBUTES	ObjAttr;
	NTSTATUS			Status;
	ULONG				Disposition;
	
	RtlInitUnicodeString(&RegKey,regkey);
	RtlInitUnicodeString(&RegName,regname);
	memset(&ObjAttr,0,sizeof(OBJECT_ATTRIBUTES));
	InitializeObjectAttributes(&ObjAttr,&RegKey,OBJ_CASE_INSENSITIVE,NULL,NULL);
	
	Status = ZwOpenKey(
		&hReg,
		GENERIC_ALL,
		&ObjAttr
	);
	if (!NT_SUCCESS(Status)){
		KdPrint(("openkey failed. code:%X",Status));
		return Status;
	}
	
	Status = ZwSetValueKey(
		hReg,
		&RegName,
		0,
		REG_DWORD,
		&value,
		sizeof(ULONG)
	);
	if (!NT_SUCCESS(Status)){
		KdPrint(("setkey failed. code:%X",Status));
		return Status;
	}

	KdPrint(("setkeyvalue success"));
	ZwClose(hReg);
	return Status;
}

NTSTATUS MyQueryValueKey(HANDLE handle,wchar_t *regname){
	NTSTATUS						Status;
	UNICODE_STRING					RegName;
	KEY_VALUE_BASIC_INFORMATION		*pKeyValueBaseInfo;
	ULONG							ResultLength;

	RtlInitUnicodeString(&RegName,regname);
	Status = ZwQueryValueKey(
		handle,
		&RegName,
		KeyValueBasicInformation,
		0,
		0,
		&ResultLength
	);
	if (!NT_SUCCESS(Status)&&Status!=STATUS_BUFFER_TOO_SMALL){
		KdPrint(("queryvaluekey failed1. code:%X",Status));
		return Status;
	}
	pKeyValueBaseInfo = ExAllocatePool(NonPagedPool,ResultLength);
	if (pKeyValueBaseInfo==0){
		KdPrint(("exallocatepool failed."));
		return STATUS_UNSUCCESSFUL;
	}
	
	Status = ZwQueryValueKey(
		handle,
		&RegName,
		KeyValueBasicInformation,
		pKeyValueBaseInfo,
		ResultLength,
		&ResultLength
	);
	if (!NT_SUCCESS(Status)){
		KdPrint(("queryvaluekey failed2. code:%X",Status));
		return Status;
	}

	KdPrint(("Name:%S,Type:%d",pKeyValueBaseInfo->Name,pKeyValueBaseInfo->Type));
	ZwClose(handle);
	return Status;
}

NTSTATUS MyQueryKey(HANDLE handle){
	NTSTATUS						Status;
	KEY_FULL_INFORMATION			*pKeyFullInfo;
	ULONG							ResultLength;

	Status = ZwQueryKey(
		handle,
		KeyFullInformation,
		0,
		0,
		&ResultLength
	);
	if (!NT_SUCCESS(Status)&&Status!=STATUS_BUFFER_TOO_SMALL){
		KdPrint(("querykey failed1. code:%X",Status));
		return Status;
	}
	pKeyFullInfo = ExAllocatePool(NonPagedPool,ResultLength);
	if (pKeyFullInfo==0){
		KdPrint(("exallocatepool failed."));
		return STATUS_UNSUCCESSFUL;
	}
	
	Status = ZwQueryKey(
		handle,
		KeyFullInformation,
		pKeyFullInfo,
		ResultLength,
		&ResultLength
	);
	if (!NT_SUCCESS(Status)){
		KdPrint(("querykey failed2. code:%X",Status));
		return Status;
	}

	KdPrint(("SubKeys:%d",pKeyFullInfo->SubKeys));
	ZwClose(handle);
	return Status;
}

VOID MyDriverUnload(PDRIVER_OBJECT pDriverObject){
	KdPrint(("unload success."));
}

VOID TestAllFunction(){
	NTSTATUS	Status;
	HANDLE		handle;
	wchar_t *regkey   = L"\\REGISTRY\\MACHINE\\SYSTEM\\ControlSet001\\services\\MyKey";
	wchar_t *regkey2   = L"\\REGISTRY\\MACHINE\\SYSTEM\\ControlSet001\\services\\napagent";
	wchar_t *regname   = L"evil";
	wchar_t *regname2   = L"Type";
	ULONG value = 10;
	wchar_t *filepath = L"\\??\\c:\\1.txt";
	
	Status = MyCreateKey(regkey);
	if (!NT_SUCCESS(Status)){
		KdPrint(("createkey failed."));
	}
	handle = MyOpenKey(regkey);
	if (!handle){
		KdPrint(("openkey failed."));
	}else{
		ZwClose((HANDLE)handle);
	}
	Status = MySetValueKey(regkey,regname,(PVOID)value);
	if (!NT_SUCCESS(Status)){
		KdPrint(("setkey failed."));
	}

	handle = MyOpenKey(regkey2);
	if (!handle){
		KdPrint(("openvaluekey failed."));
	}else{
		Status = MyQueryValueKey(handle,regname2);
		if (!NT_SUCCESS(Status)){
			ZwClose((HANDLE)handle);
		}
	}

	handle = MyOpenKey(regkey2);
	if (!handle){
		KdPrint(("openkey failed."));
	}else{
		Status = MyQueryKey(handle);
		if (!NT_SUCCESS(Status)){
			ZwClose((HANDLE)handle);
		}
	}

	Status = MyCreateFile(filepath);
	if (!NT_SUCCESS(Status)){
		KdPrint(("createfile failed."));
	}
}

NTSTATUS DriverEntry(PDRIVER_OBJECT pDriverObject,PUNICODE_STRING pRegistryPath){
	NTSTATUS	Status;
	TestAllFunction();

	pDriverObject->DriverUnload = MyDriverUnload;
	return STATUS_SUCCESS;
}
