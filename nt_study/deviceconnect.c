#include "ntddk.h"
#include "wdmsec.h"

#define 	KS_DEVICE_NAME		L"\\Device\\FirstDevice"
#define 	KS_SYB_LIC_NAME		L"\\??\\FirstDevice"
#define		IOCTL_ON			CTL_CODE(FILE_DEVICE_UNKNOWN,0x900,METHOD_BUFFERED,FILE_ANY_ACCESS)
#define		IOCTL_OFF			CTL_CODE(FILE_DEVICE_UNKNOWN,0x901,METHOD_BUFFERED,FILE_ANY_ACCESS)

VOID MyDriverUnload(PDRIVER_OBJECT pDriverObject){
	UNICODE_STRING usSymDevice;
	RtlInitUnicodeString(&usSymDevice,KS_SYB_LIC_NAME);
	if(pDriverObject->DeviceObject!=NULL){
		IoDeleteSymbolicLink(&usSymDevice);
		IoDeleteDevice(pDriverObject->DeviceObject);
		KdPrint(("delete device success!"));
	}
}

NTSTATUS CreateDeviceSecure(PDRIVER_OBJECT pDriverObject){
	NTSTATUS Status;
	PDEVICE_OBJECT pDevObj;
	UNICODE_STRING usDevName;
	UNICODE_STRING usSysName;
	UNICODE_STRING DefaultSDDLString;
	const GUID KS_GUID_CLASS = {0x0d583db6,0x510b,0x11e8,{0x9e,0x1b,0x00,0x50,0x56,0xc0,0x00,0x08}};

	RtlInitUnicodeString(&usDevName,KS_DEVICE_NAME);
	RtlInitUnicodeString(&DefaultSDDLString,L"D:P(A;;GA;;;WD)");

//  this function can be find in wdmsec.h
//	NTSTATUS IoCreateDeviceSecure(
//	  _In_     PDRIVER_OBJECT   DriverObject,
//	  _In_     ULONG            DeviceExtensionSize,
//	  _In_opt_ PUNICODE_STRING  DeviceName,
//	  _In_     DEVICE_TYPE      DeviceType,
//	  _In_     ULONG            DeviceCharacteristics,
//	  _In_     BOOLEAN          Exclusive,
//	  _In_     PCUNICODE_STRING DefaultSDDLString,
//	  _In_opt_ LPCGUID          DeviceClassGuid,
//	  _Out_    PDEVICE_OBJECT   *DeviceObject
//	);
	
	Status = IoCreateDeviceSecure(
			pDriverObject,
			0,
			&usDevName,
			FILE_DEVICE_UNKNOWN,
			FILE_DEVICE_SECURE_OPEN,
			TRUE,
			&DefaultSDDLString,
			(LPCGUID)&KS_GUID_CLASS,
			&pDevObj);
	if(!NT_SUCCESS(Status)){
		return Status;
	}
	pDevObj->Flags |= DO_BUFFERED_IO;

	RtlInitUnicodeString(&usSysName,KS_SYB_LIC_NAME);
	Status = IoCreateSymbolicLink(&usSysName,&usDevName);
	if(!NT_SUCCESS(Status)){
		IoDeleteDevice(pDevObj);
		return Status;
	}
	return STATUS_SUCCESS;
}

NTSTATUS DisPathRoutine(PDEVICE_OBJECT pDeviceObject,PIRP pIrp){
	NTSTATUS Status = STATUS_SUCCESS;
	PIO_STACK_LOCATION pStack = IoGetCurrentIrpStackLocation(pIrp);
	ULONG ulcode = (ULONG) pStack->Parameters.DeviceIoControl.IoControlCode;
	
	PVOID lpInputBuffer = pIrp->AssociatedIrp.SystemBuffer;
	ULONG ulReadLength = pStack->Parameters.DeviceIoControl.InputBufferLength;

	switch(ulcode){
    case IOCTL_ON:
        KdPrint(("recive hook message.\r\n"));
        break;
    case IOCTL_OFF:
        KdPrint(("recive resest hook message.\r\n"));
        break;
    }

    pIrp->IoStatus.Status = Status;
    pIrp->IoStatus.Information = ulReadLength; //return in func DeviceIoControl's params-->lpBytesReturned?
    IoCompleteRequest(pIrp,IO_NO_INCREMENT);
	return Status;
}

NTSTATUS CreateCompleteRoutine(PDEVICE_OBJECT pDeviceObject,PIRP pIrp){
	//为了在 r3 层 createfile 创建设备链接时候能获得句柄，这里需要返回成功。 
	return STATUS_SUCCESS;
}

VOID DebugPrint(NTSTATUS Status){
	if(!NT_SUCCESS(Status)){
		KdPrint(("create device failed! code:%X",Status));
	}else{
		KdPrint(("create device success!"));
	}
}

NTSTATUS DriverEntry(PDRIVER_OBJECT pDriverObject,PUNICODE_STRING pRegistryPath){
	NTSTATUS Status;

	Status = CreateDeviceSecure(pDriverObject);
	DebugPrint(Status);

	pDriverObject->MajorFunction[IRP_MJ_CREATE] = CreateCompleteRoutine;
	pDriverObject->MajorFunction[IRP_MJ_DEVICE_CONTROL] = DisPathRoutine;

	pDriverObject->DriverUnload = MyDriverUnload;
	return STATUS_SUCCESS;
}
