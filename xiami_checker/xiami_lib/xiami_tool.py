# -*- coding: utf-8 -*-

import re, xlrd, difflib, json
from itertools import groupby
from lxml import etree

#简单的字符串处理器，单独放以后方便扩展

def filter_space(string):
    s = re.findall('\s+',string)
    if s!=0:
        for i in set(s):
            string = string.replace(i,' ')
    return string

#打开xls读取

def xls_read(string,table_chr):
    data = xlrd.open_workbook(string)
    table = data.sheets()[0]
    func = lambda i:str(int(i)) if type(i)==float else i
    if type(table_chr)==int:
        return [map(func,table.col_values(i)) for i in range(table_chr)]
    elif type(table_chr)==list:
        table_chr_inner_all_need_be_int = lambda table_chr:map(lambda i:True if type(i)==int else False,table_chr).count(True)==len(table_chr)
        assert table_chr_inner_all_need_be_int(table_chr)
        return [map(func,table.col_values(i)) for i in table_chr]
    else:
        return None



#简单获取两个字符串的相似度
#第二个则为短字符串优先，遍历长字符串进行最大相似度输出

def compare_string(stringA,stringB):
    stringA,stringB = stringA.upper(),stringB.upper()
    return difflib.SequenceMatcher(None, stringA, stringB).ratio()
def compare_string_plus(stringA,stringB):
    if len(stringA) < len(stringB):
        b = len(stringA)
        k = len(stringB) - len(stringA)
        p = max([compare_string(stringA,stringB[i:i+b]) for i in range(1,k+1)])
        return p
    elif len(stringA) > len(stringB):
        b = len(stringB)
        k = len(stringA) - len(stringB)
        p = max([compare_string(stringB,stringA[i:i+b]) for i in range(1,k+1)])
        return p
    else:
        return compare_string(stringA,stringB)

#判断某个xpath是否存在
def is_exist_xpath(string,html):
    e = etree.HTML(html)
    if len(e.xpath(string))>0:
        return True
    else:
        return False

#判断两个字符串是否有特殊符号（括号等），如果有，则返回长度差与总长之比
#主要是用来对一些不带有附属说明的名字进行长度限制的
def has_brackets(stringA,stringB):
    if '(' not in stringA and '(' not in stringB and \
       ':' not in stringA and ':' not in stringB and \
       '-' not in stringA and '-' not in stringB and \
       '/' not in stringA and '/' not in stringB and \
       '.' not in stringA and '.' not in stringB and \
       '[' not in stringA and '[' not in stringB and \
       '\'' not in stringA and '\'' not in stringB and \
       'FEATUR' not in stringA and 'FEATUR' not in stringB and \
       'FROM' not in stringA and 'FROM' not in stringB and \
       '&AMP;' not in stringA and '&AMP;' not in stringB:
        cc = float(len(stringA)-len(stringB))
        zc = float(len(stringA)+len(stringB))
        return abs(cc)/zc
    else:
        return 0






#简单对歌手和专辑名字进行[A,B,A+' '+B]三段式组装

def create_keywords(AB_tuple):
    tuple_A,tuple_B = AB_tuple
    return tuple_A,tuple_B,[tuple_A,tuple_B,' '.join((tuple_A,tuple_B))]






#对信息进行简单的保存，防止出现各式各样的错误

def log(*string):
    string = map(lambda i:i.encode('utf-8') if type(i)==unicode else i,string)
    string = ''.join(map(str,string))
    print string
    with open('xiami.log','a') as f:
        f.write(string+'\n')

def log_find(album,singer_o,album_o):
    s = album
    t_func1 = lambda i:i.encode('utf-8') if 'UNICODE' in str(type(i)).upper() else i
    t_func2 = lambda i:map(t_func1,i)
    s = map(t_func2,s)
    with open('xiami_find.log','a') as f:
        for i in s:
            f.write(i[1]+'\t'+i[0]+'\t'+t_func1(singer_o)+'\t'+t_func1(album_o)+'\n')

def log_id(string):
    indx,songA,songB,idx,check,release = string
    string = map(lambda i:i.encode('utf-8') if type(i)==unicode else i,string)
    string = '\t'.join(map(str,string))
    log('table name:',songA)
    log('find  name:',songB)
    log('find   id :',idx)
    log('is checked:',check)
    log('is release:',release)
    with open('xiami_id.log','a') as f:
        f.write(string+'\n')




#针对不同类型的导入文件进行简单的字符串处理

def del_string(string):
    return string.replace('"""','').replace('&amp;','and')

def del_map_string(AB_tuple):
    tuple_A,tuple_B = AB_tuple
    if type(AB_tuple[0]) != str and type(AB_tuple[0]) != unicode:
        if type(AB_tuple[0]) == float:
            tuple_A = str(int(AB_tuple[0]))
        else:
            tuple_A = str(AB_tuple[0])
    if type(AB_tuple[1]) != str and type(AB_tuple[1]) != unicode:
        if type(AB_tuple[1]) == float:
            tuple_B = str(int(AB_tuple[1]))
        else:
            tuple_B = str(AB_tuple[1])
    return tuple_A,tuple_B,(tuple_A,tuple_B)







#因为一些字符串转换的原因不得不除掉引号，
#这样才能使“原有表格”信息形成的【歌手，专辑】的tuple，
#与“处理后表格”的tuple进行hash对比
#即，将tuple作为字典的索引进行进一步的处理

def rm_quote(s):
    for index,i in enumerate(s):
        if type(i[0])==float:
            a = i[0]
        else:
            a = i[0].replace('"','')
        if type(i[1])==float:
            b = i[1]
        else:
            b = i[1].replace('"','')
        s[index] = (a,b)
    return s




#简单获取已经从txt中复制到的xls里的数据
#并进行专辑有无的下标对比，获得发现专辑的下标

def filter_by_string(s):
    t = {}
    start = 0
    for i,j in groupby(s):
        lens = len(list(j))
        if t.has_key(i):
            t[i] += range(start,start+lens)
        else:
            t[i] = range(start,start+lens)
        start += lens
    return t

def get_had_num_list(s1,s2):
    v = filter_by_string(s1)
    had = []
    for i in set(s2):
        if i in v:
            had += v[i]
    return had




#通过“有专辑”的tuple表将歌曲表进行处理，留下来的
#即为以“有专辑”的tuple作为字典标签收纳歌曲群
#返回这样的结构{（歌手1，专辑1）：【歌曲1，歌曲2……】，……}

def arl_songs(s1,s2,names):
    t = {}
    start = 0
    for i,j in groupby(s1):
        lens = len(list(j))
        if i in s2:
            if t.has_key(i):
                t[i] += zip(names[start:start+lens],range(start,start+lens))
            else:
                t[i] = zip(names[start:start+lens],range(start,start+lens))
        start += lens
    return t

#同上，不过下面这里是要准备获取专辑群的字典

def arl_songsid(s,dic):
    t = {}
    start = 0
    for i,j in groupby(s):
        lens = len(list(j))
        if i in s:
            if t.has_key(i):
                t[i] += dic[start:start+lens]
            else:
                t[i] = dic[start:start+lens]
        start += lens
    return t






#通过三部处理以后的文件找到相应的表示方式
#并写入 final_info 文件当中

def final_info(xls,ifo_list):
    s = xls_read(xls,ifo_list)
    with open('final_info.txt','w') as f:
        for i in zip(*s):
            del_string = lambda p:[str(int(key)) if type(key)==float else key for key in p]
            a,b,c,d = del_string(i)
            if b.strip() == '':
                if c == u'无专辑':
                    f.write('未收录'+'\n')
                else:
                    if d == u'下架':
                        f.write('下架'+'\n')
                    else:
                        if a.strip()=='':
                            f.write('未收录'+'\n')
                        else:
                            f.write('\n')
            else:
                f.write('问题'+'\n')






