#include "ntddk.h"

#pragma(1)
typedef struct ServiceDescriptorEntry{
    unsigned int *ServiceTableBase;
    unsigned int *ServiceCounterTableBase;
    unsigned int NumberOfServices;
    unsigned char *ParamTableBase;
} ServiceDescriptorTableEntry_t, *PServiceDescriptorTableEntry;
#pragma()

__declspec(dllimport)ServiceDescriptorTableEntry_t KeServiceDescriptorTable;

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

typedef NTSTATUS (*NewNtCreateFile) (
    __out PHANDLE FileHandle,
    __in ACCESS_MASK DesiredAccess,
    __in POBJECT_ATTRIBUTES ObjectAttributes,
    __out PIO_STATUS_BLOCK IoStatusBlock,
    __in_opt PLARGE_INTEGER AllocationSize,
    __in ULONG FileAttributes,
    __in ULONG ShareAccess,
    __in ULONG CreateDisposition,
    __in ULONG CreateOptions,
    __in_bcount_opt(EaLength) PVOID EaBuffer,
    __in ULONG EaLength
    );

//global
ULONG g_ntcreatefile;
ULONG g_fastcallpointer;
ULONG g_goto_orig;

VOID FilterKiFastCallEntry(ULONG ServiceTableBase,ULONG FuncIndex){
	if(ServiceTableBase==(ULONG)KeServiceDescriptorTable.ServiceTableBase){
		if(FuncIndex==190){
			KdPrint(("CurrentProcess:%s FuncIndex:%d",(char*)PsGetCurrentProcess()+0x16c,FuncIndex));
			
		}
	}
}

__declspec(naked)
void NewKiFastCallEntry(){
    __asm{
        pushad
        pushfd

        //这时候的eax为此时所调用ssdt标志位 
        //这时候的edi为ServiceTableBase地址 
		//这时候的edx就是ssdt中所调用的内核函数地址 
		push eax
		push edi 
        call FilterKiFastCallEntry

        popfd
        popad
        
        sub esp,ecx;
        shr ecx,2
        jmp g_goto_orig
    }
}

void HookKiFastCallEntry(ULONG HookPointer){
    ULONG u_temp;
    UCHAR jmp_code[5];

    u_temp = (ULONG)NewKiFastCallEntry - HookPointer - 5;
    jmp_code[0] = 0xE9;
    *(ULONG*)&jmp_code[1] = u_temp;

    PageProtectOff();
    RtlCopyMemory((PVOID)HookPointer,jmp_code,5);
    PageProtectOn();
}

ULONG SearchHookPointer(ULONG startAddress){
	ULONG uIndex;
	UCHAR *p = (UCHAR*)startAddress;
	for(uIndex = 0;uIndex<200;uIndex++){
		if( *p==0x2B &&
			*(p+1)==0xE1 &&
			*(p+2)==0xC1 &&
			*(p+3)==0xE9 &&
			*(p+4)==0x02){
			return (ULONG)p;
		}
		p--;
	}
	return 0;
}

NTSTATUS MyNtCreateFile (
    __out PHANDLE FileHandle,
    __in ACCESS_MASK DesiredAccess,
    __in POBJECT_ATTRIBUTES ObjectAttributes,
    __out PIO_STATUS_BLOCK IoStatusBlock,
    __in_opt PLARGE_INTEGER AllocationSize,
    __in ULONG FileAttributes,
    __in ULONG ShareAccess,
    __in ULONG CreateDisposition,
    __in ULONG CreateOptions,
    __in_bcount_opt(EaLength) PVOID EaBuffer,
    __in ULONG EaLength
    ){
    	ULONG u_call_retaddr;
    	__asm{
    		pushad	
    		mov		eax,[ebp+4]
    		mov		u_call_retaddr,eax
    		popad
		}
		g_fastcallpointer = SearchHookPointer(u_call_retaddr);
		if (g_fastcallpointer==0){
			KdPrint(("SearchHookPointer failed."));
		}else{
			g_goto_orig = g_fastcallpointer + 5;
			HookKiFastCallEntry(g_fastcallpointer);
		}
		
		PageProtectOff();
		KeServiceDescriptorTable.ServiceTableBase[66] = (unsigned int)g_ntcreatefile;
		PageProtectOn(); 
		return ((NewNtCreateFile)g_ntcreatefile)(
			FileHandle,
			DesiredAccess,
			ObjectAttributes,
			IoStatusBlock,
			AllocationSize,
			FileAttributes,
			ShareAccess,
			CreateDisposition,
			CreateOptions,
			EaBuffer,
			EaLength
		);
	}

void TryHookKiFastCallEntry(){
	g_ntcreatefile = KeServiceDescriptorTable.ServiceTableBase[66]; //win7 的 ntcreatefile 系统 ssdt 表中的数值为66；
	PageProtectOff();
	KeServiceDescriptorTable.ServiceTableBase[66] = (unsigned int)MyNtCreateFile;
	PageProtectOn(); 
}

void UnHookKiFastCallEntry(){
	UCHAR orig_jmpcode[5] = {0x2B, 0xE1, 0xC1, 0xE9, 0x02};
	if (g_fastcallpointer==0){
		return;
	}
    PageProtectOff();
    RtlCopyMemory((PVOID)g_fastcallpointer,orig_jmpcode,5);
    PageProtectOn();
}

VOID MyDriverUnload(PDRIVER_OBJECT pDriverObject){
    UnHookKiFastCallEntry();
}

NTSTATUS DriverEntry(PDRIVER_OBJECT pDriverObject,PUNICODE_STRING pRegistryPath){
    TryHookKiFastCallEntry();
    pDriverObject->DriverUnload = MyDriverUnload;
    return STATUS_SUCCESS;
}
