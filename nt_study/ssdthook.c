#include "ntddk.h"

#pragma(1)
typedef struct ServiceDescriptorEntry{
    unsigned int *ServiceTableBase;
    unsigned int *ServiceCounterTableBase;
    unsigned int NumberOfServices;
    unsigned char *ParamTableBase;
} ServiceDescriptorTableEntry_t, *PServiceDescriptorTable;
#pragma()

__declspec(dllimport)ServiceDescriptorTableEntry_t KeServiceDescriptorTable;

typedef NTSTATUS (*NEWOPENPROCESS) (
    __out PHANDLE ProcessHandle,
    __in ACCESS_MASK DesiredAccess,
    __in POBJECT_ATTRIBUTES ObjectAttributes,
    __in_opt PCLIENT_ID ClientId
);

void PageProtectOff(){
    __asm{
        cli
        mov eax,cr0
        and eax,not 10000h
        mov cr0,eax
    }
}

void PageProtectOn(){
    __asm{
        mov eax,cr0
        or eax,10000h
        mov cr0,eax
        sti
    }
}

ULONG g_ntopenprocess;

NTSTATUS NewNtOpenProcess (
    __out PHANDLE ProcessHandle,
    __in ACCESS_MASK DesiredAccess,
    __in POBJECT_ATTRIBUTES ObjectAttributes,
    __in_opt PCLIENT_ID ClientId
){
    KdPrint(("NewNtOpenProcess!"));
    return ((NEWOPENPROCESS)g_ntopenprocess)(ProcessHandle,DesiredAccess,ObjectAttributes,ClientId);
}

NTSTATUS HookNtOpenProcess(){
    NTSTATUS status;
    status = STATUS_SUCCESS;
    g_ntopenprocess = KeServiceDescriptorTable.ServiceTableBase[190];
    PageProtectOff();
    KeServiceDescriptorTable.ServiceTableBase[190] = NewNtOpenProcess;
    PageProtectOn();
    return status;
}


VOID UnHookNtOpenProcess(){
    PageProtectOff();
    KeServiceDescriptorTable.ServiceTableBase[190] = g_ntopenprocess;
    PageProtectOn();
}

VOID MyDriverUnload(PDRIVER_OBJECT pDriverObject){
    UnHookNtOpenProcess();
}

NTSTATUS DriverEntry(PDRIVER_OBJECT pDriverObject,PUNICODE_STRING pReg_Path){
    HookNtOpenProcess();
    pDriverObject->DriverUnload = MyDriverUnload;
    return STATUS_SUCCESS;
}
