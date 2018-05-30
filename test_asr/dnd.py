def hook_dropfiles(hwnd,func=lambda i:print(i)):
    """
    *args:
        hwnd
    **kw:
        func = lambda i:print(i)
        # this func to deal each full_path_file_name.
        # default func just print each one.
    if you use tkinter, you can hook like this:
    =================================================
    > from dnd import hook_dropfiles as dndhook
    >
    > import tkinter
    > tk = tkinter.Tk()
    > hwnd = tk.winfo_id()
    >
    > dndhook(hwnd)
    >
    > tk.mainloop()
    test: work on win7 32bit & 64bit.
    """
    import platform
    import ctypes
    from ctypes.wintypes import DWORD
    prototype = ctypes.WINFUNCTYPE(DWORD,DWORD,DWORD,DWORD,DWORD)
    WM_DROPFILES = 0x233
    GWL_WNDPROC = -4

    def py_drop_func(hwnd,msg,wp,lp):
        if msg == WM_DROPFILES:
            count = ctypes.windll.shell32.DragQueryFile(wp,-1,None,None)
            szFile = ctypes.c_buffer(260)
            for i in range(count):
                ctypes.windll.shell32.DragQueryFile(wp,i,szFile,ctypes.sizeof(szFile))
                dropname = szFile.value
                func(dropname)
            ctypes.windll.shell32.DragFinish(wp)
        return ctypes.windll.user32.CallWindowProcW(org_wndproc,hwnd,msg,wp,lp)

    global org_wndproc,new_wndproc
    org_wndproc = None
    new_wndproc = prototype(py_drop_func)

    if platform.architecture()[0] == "32bit":
        GetWindowLong = ctypes.windll.user32.GetWindowLongW
        SetWindowLong = ctypes.windll.user32.SetWindowLongW
    elif platform.architecture()[0] == "64bit":
        GetWindowLong = ctypes.windll.user32.GetWindowLongPtrW
        SetWindowLong = ctypes.windll.user32.SetWindowLongPtrW

    ctypes.windll.shell32.DragAcceptFiles(hwnd,True)
    org_wndproc = GetWindowLong(hwnd,GWL_WNDPROC)
    SetWindowLong(hwnd,GWL_WNDPROC,new_wndproc)
