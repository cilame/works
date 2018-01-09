# -*- coding: utf-8 -*-
import os, re, json, string, tarfile

class DataLoader(object):
    """
    **kw:
        extract: 是否在创建对象时候解压（默认解压，True）
        logging: 是否打印加载时候的信息（默认打印，True）

    e.g:
        >>> s = DataLoader('./data.tar.gz',log=False)
        >>> datas = s.load_datas()

        在 s.load_datas() 函数内会延迟创建一个 self.datas 的 list 数据。
        这个函数本质上就是返回这个。这个 list 是清洗后的所有数据。
        控制台使用时注意至少加个接收的名字。
    """
    def __init__(self, filename, extract=True, logging=True):
        
        self._filename = filename
        self._extract_path = self._filename+'_data'
        self._all_id = set()
        self._log = logging
        if extract:
            self.extract()

    # 解压缩，根据测试文件，目前只支持 tgz 解压
    def extract(self):
        if not os.path.isdir(self._extract_path):
            tarobj = tarfile.open(self._filename, "r:gz")
            tarobj.extractall(self._extract_path)
            tarobj.close()
        else:
            self._print("[ ATTENTION ] file dir '%s' exist."%self._extract_path)

    # 读取文件
    def load_datas(self):
        if not hasattr(self, 'datas'):
            # 延迟创建 datas
            self.datas = []
        files = os.listdir(self._extract_path)
        self._print('txt file numbers: %d' % len(files))
        for txt_name in files:
            txt_path = os.path.join(self._extract_path,txt_name)
            self._print('[ LOADING ] %s, all_load_num: %d' % (txt_path,len(self.datas)))
            self._load_onetxt(txt_path)
        self._print('final. %ds info loads.'%len(self.datas))
        return self.datas

    # 读取单个 txt 文件数据
    def _load_onetxt(self, pathname):
        s = open(pathname).readlines()
        for indx,i in enumerate(s):
            _n = json.loads(i)
            _id    = _n.get('id','')
            _age   = _n.get('age','')
            _name  = _n.get('name','')
            _email = _n.get('email','')
            a = self._check_id(_id)
            b = self._check_age(_age)
            c = self._check_name(_name)# 题目不要求，恒等于 True
            d = self._check_email(_email)
            if a and b and c and d:
                self._all_id.add(_id)
                self.datas.append(i)
            else:
                self._print('*[ WARNING ] load fail: {} {} {} {}'.format(_id,_age,_name,_email))



    # 检查id
    # 类型判断(int)和查重
    def _check_id(self, _id):
        tp = isinstance(_id,int)
        return tp and _id not in self._all_id

    # 检查年龄
    # 类型判断(int)和判断是否大于0
    def _check_age(self, _age):
        tp = isinstance(_age,int)
        return tp and _age > 0

    # 检查名字(题目中似乎并不需求这个，注释掉之前写的逻辑部分直接返回 True 了)
    # 类型判断(basestring)和是否等于纯空格和空字符串
    # 另外名字的判断还要检查名字的字符串里面没有这些奇怪符号
    # string.punctuation 就是这些符号 '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    def _check_name(self, _name):
##        tp = isinstance(_name,basestring)
##        return tp and _name.strip() != '' and all(map(lambda i:i not in _name,string.punctuation))
        return True

    # 检查email
    # 类型判断(basestring)以及判断是否能够用 email 正则找到
    def _check_email(self, _email):
        tp = isinstance(_email,basestring)
        rx = '(^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$)'
        return tp and len(re.findall(rx,_email)) == 1

    # 方便用参数 logging 控制是否输出加载信息
    def _print(self,args):
        if self._log:
            print(args)

if __name__ == '__main__':
    s = DataLoader('./data.tar.gz')
    #s = DataLoader('./data.tar.gz', logging=False)
    datas = s.load_datas()

