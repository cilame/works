import tkinter
import tkinter.messagebox as messagebox
from tkinter.scrolledtext import ScrolledText
import tkinter.ttk as ttk
import os, dnd, csv, time, math
import requests
import threading, difflib, functools
from collections import OrderedDict


WAVPATH = './wavfile'
# sigmoid_with_p 加权函数的附带参数P
P = 20


if not os.path.isdir(WAVPATH):
    os.mkdir(WAVPATH)

root = tkinter.Tk()
root.resizable(0,0)
root.title("语音识别分析工具(支持拖拽图标加载)")

frame1 = tkinter.Frame(root)
frame2 = tkinter.Frame(root)





# frame1
#=================================================
# 顶部一排的按钮
analyse_top = None
analyse_txt = None
# 分析方法
def analyse():
    # 分析方法就按照字典方式简单处理一下"key文件" 和"value文件"
    if not os.path.isfile(vs.get()) or not os.path.isfile(vs2.get()):
        messagebox.showwarning("提示","原始文件路径或翻译文件路径有误, 无法分析")
        return

    # 生成字典{url1:text1, url2:text2, ...}
    global key_values
    with open(vs.get()) as f:
        rd = csv.reader(f)
        key_values = OrderedDict(map(lambda i:(i[0].rsplit('/',1)[-1],i[1]),zip(*list(zip(*rd))[::-1])))

    global key_values2
    with open(vs2.get()) as f:
        rd = csv.reader(f)
        key_values2 = {i[0]:i[1:] for i in rd}

    inner_num = 0
    for i in key_values2:
        if i in key_values:
            inner_num += 1

    _analyse_model = "原始文件共 %2d 个翻译描述.\n"%len(key_values)+\
                     "翻译文件共 %2d 个翻译描述.\n"%len(key_values2)+\
                     "交集有 %2d 个."%inner_num

    global analyse_top, analyse_txt
    if analyse_top:
        analyse_top.destroy()
    analyse_top = tkinter.Toplevel(root)
    analyse_top.title("分析窗口.")
    analyse_top.resizable(0,0)
    analyse_txt = tkinter.Text(analyse_top, width=60, height=10)
    analyse_btn = ttk.Button(analyse_top,text="点击开始写入分析文件.", command=analyse_file)
    analyse_txt.insert(tkinter.END,_analyse_model+'\n')
    analyse_txt.pack()
    analyse_btn.pack()

def sigmoid_with_p(x,p):
    return 1./(1 + math.exp(- x/float(p)))

def analyse_file():
    global analyse_txt
    filename = vs2.get()
    if '/' in filename:
        filename = filename.rsplit('/',1)[1]
    filename = 'analyse_'+filename
    if os.path.isfile(filename):
        if not messagebox.askokcancel("提示","文件%s已存在，是否覆盖。"%filename):
            return
    analyse_txt.insert(tkinter.END,"正在写入...\n")
    analyse_txt.update()
    try:
        csvFile = open(filename,'w', newline='')
        writer = csv.writer(csvFile)
        ##writer.writerow(['key','原始数据',
        ##                 '阿里语音翻译','相似度（原数据与阿里语音翻译）',
        ##                 '百度语音翻译','相似度（原数据与百度语音翻译）',
        ##                 '腾讯语音翻译','相似度（原数据与腾讯语音翻译）',
        ##                 '讯飞语音翻译','相似度（原数据与讯飞语音翻译）'])
        writer.writerow(['key','原始数据',
                         '阿里语音翻译','百度语音翻译','腾讯语音翻译','讯飞语音翻译',
                         '相似度（原数据与阿里语音翻译）',
                         '相似度（原数据与百度语音翻译）',
                         '相似度（原数据与腾讯语音翻译）',
                         '相似度（原数据与讯飞语音翻译）',
                         'similar * sigmoid(len(str)/%d)（根据字符串长度进行加权的函数）'%P])
        for row in key_values:
            if row not in key_values2:
                continue
            translate_s = key_values2[row]
            similar_s   = list(map(lambda i:compare_diff(key_values[row],i)*sigmoid_with_p(len(key_values[row]),P),key_values2[row]))
            # 这里选了一个数字紧凑的表现方法
            translate_and_similar = translate_s + similar_s # list(functools.reduce(lambda i,j:i+j,zip(translate_s,similar_s)))
            _row = [row] + [key_values[row]] + translate_and_similar
            writer.writerow(_row)
        csvFile.close()
        analyse_txt.insert(tkinter.END,"分析已写入文件%s\n"%filename)
        analyse_txt.update()
    except:
        analyse_txt.insert(tkinter.END,"分析写入文件失败\n")
        analyse_txt.update()
        
    

def compare_diff(a,b):
    return difflib.SequenceMatcher(a=a,b=b).ratio()


def check_download():
    v = filter(lambda i:i.strip(),text.get(0.,tkinter.END).splitlines())
    w = False # 是否在加载路径中出现错误，F没有
    files = []
    for i in v:
        try:
            assert i.startswith("http")
            files += [[i.rsplit('/',1)[1], i]]
        except:
            messagebox.showwarning("警告","错误的文件格式")
            w = True
            break
    if not w:
        have,unhave = 0,0
        foo = lambda i:os.path.isfile(os.path.join(WAVPATH,i[0]))
        for i in files:
            if foo(i): have += 1
            else: unhave += 1
        if unhave and\
                 messagebox.askokcancel("提示",
                                        "%d已下载,有%d未下载,是否下载?"%\
                                        (have,unhave)):
            if download_wav(files):
                messagebox.showinfo("提示","下载完毕")
        else:
            messagebox.showinfo("提示","检查完毕%d已经下载"%have)

def download_wav(files):
    text.delete(0.,tkinter.END)
    for i,url in files:
        filename = WAVPATH+'/'+i
        if not os.path.isfile(filename):
            text.insert(tkinter.END,'下载...'+i+"\n")
            s = requests.get(url)
            with open(filename,'wb') as f:
                f.write(s.content)
            text.see(tkinter.END)
            text.update()
    return True

def open_path():
    os.startfile(os.path.join(os.getcwd(),WAVPATH))

vs = tkinter.StringVar(value = "加载的csv文件地址.")
vs2 = tkinter.StringVar(value = "翻译的csv文件地址.")
entry1 = ttk.Entry(frame1,textvariable=vs)
entry2 = ttk.Entry(frame1,textvariable=vs2)
vi = tkinter.IntVar(value=5)
label1 = ttk.Label(frame1,text="翻译线程数:")
combobox = ttk.Combobox(frame1,width=3,textvariable=vi,state='readonly')
ttk.Radiobutton(frame1,text="")
combobox["values"] = (1,2,3,4,5,6,7,8,9,10)
button1_1 = ttk.Button(frame1,text='分析内容',command=analyse)
button1_2 = ttk.Button(frame1,text='检查下载',command=check_download)
button1_3 = ttk.Button(frame1,text='wav文件路径:%s'%WAVPATH,command=open_path)

entry1.pack(side=tkinter.LEFT,fill=tkinter.X)
entry2.pack(side=tkinter.LEFT,fill=tkinter.X)
button1_1.pack(side=tkinter.RIGHT,fill=tkinter.X)
button1_2.pack(side=tkinter.RIGHT,fill=tkinter.X)
button1_3.pack(side=tkinter.RIGHT,fill=tkinter.X)
combobox.pack(side=tkinter.RIGHT,fill=tkinter.X)
label1.pack(side=tkinter.RIGHT,fill=tkinter.X)









info = """\
+---------------------------------------+
|csv 格式读取，将csv文件拖入文本框即可  |
|格式+----------------------+           |
|    | file_text | file_url |           |
|    | file_text | file_url |           |
|    | file_text | file_url |           |
|    | file_text | file_url |           |
|    |     .     |     .    |           |
|    |     .     |     .    |           |
|    |     .     |     .    |           |
|    +----------------------+           |
|csv 第一列为 wav 语音文字              |
|csv 第二列为 wav 文件地址              |
|  （下载时，默认地址尾作为文件名字存储 |
+---------------------------------------+
|wav 格式读取，将wav文件批量拖入文本框  |
|会对应每一个wav进行识别                |
|并以日期输出到当前目录的一个csv文件里面|
+---------------------------------------+\
"""




# frame2
#=================================================
# 下面的文本框，附加拖拽功能
def menu_clear():
    text.delete(0.,tkinter.END)

def menu_post(event):
    menu.post(event.x_root,event.y_root)

# 这里引入识别接口
#=================================================
import sys
sys.path.append('asr_interface')
import asr_interface.test_xunfei as xunfei
import asr_interface.test_baidu as baidu
import asr_interface.test_aliyun as aliyun
import asr_interface.test_tengxun as tengxun

def drag_icon(filepath):
    filename = filepath.decode("gbk")
    # 这里处理拖拽上来的 csv 文件
    if filename.endswith('.csv') and messagebox.askokcancel("提示",
                                     "请问要加载 csv 文件 %s 吗？"% filename):
        vs.set(filename)
        with open(filename) as f:
            v = list(csv.reader(f))
            csv_list   = []
            csv_list_h = []
            csv_list  += [i[1] for i in v if i[0].strip()]
            csv_list   = list(set(csv_list))
        if csv_list:
            text.delete(0.,tkinter.END)
            for i in csv_list:
                if i in csv_list_h:
                    continue
                text.insert(tkinter.END,i+'\n')
            csv_list_h += csv_list
        csv_list     = []
        csv_list_h   = []
    # 这里处理拖拽上来的 wav 文件, 直接翻译
    if filename.endswith('.wav'):
        text.insert(tkinter.END,filename+'\n')



# 为了多线程
import queue
queue_aliyun  = queue.Queue()
queue_baidu   = queue.Queue()
queue_tengxun = queue.Queue()
queue_xunfei  = queue.Queue()

lock = threading.Lock()


# 为了显示翻译进度
asr_top_window = None
temp_vi1 = tkinter.IntVar()
temp_vi2 = tkinter.IntVar()
temp_vi3 = tkinter.IntVar()
temp_vi4 = tkinter.IntVar()
def asr_top():
    # 翻译进度框
    global asr_top_window
    if asr_top_window:
        asr_top_window.destroy()
    asr_top_window = tkinter.Toplevel(frame2)
    asr_top_window.title("翻译进度")
    asr_top_window.resizable(0,0)
    ttk.Label(asr_top_window,text="阿里-当前翻译数:",width=15,anchor="center").grid(row=0,column=0)
    ttk.Label(asr_top_window,text="百度-当前翻译数:",width=15,anchor="center").grid(row=1,column=0)
    ttk.Label(asr_top_window,text="腾讯-当前翻译数:",width=15,anchor="center").grid(row=2,column=0)
    ttk.Label(asr_top_window,text="讯飞-当前翻译数:",width=15,anchor="center").grid(row=3,column=0)
    ttk.Label(asr_top_window,textvariable=temp_vi1,width=10).grid(row=0,column=1)
    ttk.Label(asr_top_window,textvariable=temp_vi2,width=10).grid(row=1,column=1)
    ttk.Label(asr_top_window,textvariable=temp_vi3,width=10).grid(row=2,column=1)
    ttk.Label(asr_top_window,textvariable=temp_vi4,width=10).grid(row=3,column=1)


# 判断线程停止参数
asr_threads_num = tkinter.IntVar(0)
asr_limits_num = tkinter.IntVar(0)
asr_lists = None
def run_asr():
    # 验证是否都是wav格式
    # 验证是否都是能够访问得到的文件
    global asr_threads_num, asr_limits_num, asr_lists
    asr_threads_num.set(0)
    asr_limits_num.set(vi.get()*4)
    temp_vi1.set(0)
    temp_vi2.set(0)
    temp_vi3.set(0)
    temp_vi4.set(0)
    v = list(filter(lambda i:i.strip(),text.get(0.,tkinter.END).splitlines()))
    asr_lists = [['' for i in range(5)] for i in range(len(v))]
    w = False
    for idx,filename in enumerate(v):
        try:
            assert filename.endswith("wav")
            if filename.startswith('http'):
                filename = os.path.join(WAVPATH,filename.rsplit('/',1)[1])
            assert os.path.isfile(filename)
            # 因为网络问题不会保证输出顺序，所以就直接在put\
            # queue的过程中将序号带进去处理（csv输出需要顺序）
            queue_aliyun.put((idx,filename))
            queue_baidu.put((idx,filename))
            queue_tengxun.put((idx,filename))
            queue_xunfei.put((idx,filename))
        except:
            messagebox.showwarning("警告","错误的文件格式（输入内容不正确）或部分需翻译音频文件不存在（请检查下载）")
            queue_aliyun.queue.clear()
            queue_baidu.queue.clear()
            queue_tengxun.queue.clear()
            queue_xunfei.queue.clear()
            temp_vi1.set(0)
            temp_vi2.set(0)
            temp_vi3.set(0)
            temp_vi4.set(0)
            w = True
            break
    if not w and not queue_aliyun.empty():
        asr_top()
        thread_it(pack_asr,vi.get(),temp_vi1,0,queue_aliyun,  aliyun.asr,8000)
        thread_it(pack_asr,vi.get(),temp_vi2,1,queue_baidu,   baidu.asr,8000)
        thread_it(pack_asr,vi.get(),temp_vi3,2,queue_tengxun, tengxun.asr,8000)
        thread_it(pack_asr,vi.get(),temp_vi4,3,queue_xunfei,  xunfei.asr,8000)

def pack_asr(intvar,asr_list_index,que,asr_func,rate):
    # 在没有进行保存前，所有翻译的字符串都放在全局变量 asr_lists 里面
    # asr_list_index 是最终要保存的数据的第二维下标
    global asr_threads_num, asr_limits_num, asr_lists
    while 1:
        try:
            idx,filename = que.get(timeout=2)
            status,ret = asr_func(filename,8000)
            
            lock.acquire()
            # 进度框的数字处理
            intvar.set(intvar.get() + 1)
            # 翻译文件写入二维列表 asr_lists 中
            asr_lists[idx][asr_list_index+1] = ret.replace('\n','')
            if not asr_lists[idx][0]:
                asr_lists[idx][0] = filename.rsplit('\\',1)[-1]
            lock.release()

        except queue.Empty as e:
            lock.acquire()
            print("thread %s end."%threading.current_thread().getName())
            asr_threads_num.set(asr_threads_num.get()+1)
            if asr_threads_num.get() == asr_limits_num.get():
                # 触发保存提示
                if asr_lists and messagebox.askokcancel("提示","全部翻译完成,是否保存."):
                    save_to_csv()
            lock.release()
            break

def thread_it(func,num,*args,**kw):
    thread_number = num
    for i in range(thread_number):
        t = threading.Thread(target=func, args=args, kwargs=kw)
        t.setDaemon(True)
        t.start()

def save_to_csv():
    global asr_lists, asr_threads_num, asr_limits_num
    if not asr_lists:
        return
    save_csv_name = "./%04d%02d%02d_%02d%02d%02d.csv"%time.localtime()[:6]
    csvFile = open(save_csv_name,'w', newline='')
    writer = csv.writer(csvFile)
    for row in asr_lists:
        writer.writerow(row)
    csvFile.close()
    asr_lists = None
    asr_threads_num.set(0)
    asr_limits_num.set(0)
    vs2.set(save_csv_name)
    print("写入完成")

def test():
    asr_top()


menu = tkinter.Menu(frame2,tearoff=0)
menu.add_command(label="清除文本",command=menu_clear)
menu.add_command(label="翻译文件",command=run_asr)
menu.add_command(label="翻译进度",command=test)
menu.add_command(label="保存文件",command=save_to_csv)

text = ScrolledText(frame2,width=100)
text.bind('<3>',menu_post)
text.pack(side=tkinter.RIGHT,fill=tkinter.X)
for i in info.splitlines(): text.insert(tkinter.END,i+"\n")
dnd.hook_dropfiles(text.winfo_id(),drag_icon)# 拖拽支持











# frames pack
frame1.pack(side=tkinter.TOP,fill=tkinter.X)
frame2.pack(side=tkinter.TOP,fill=tkinter.X)



root.mainloop()
