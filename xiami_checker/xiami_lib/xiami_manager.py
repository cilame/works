# -*- coding: utf-8 -*-


from itertools import *
import time, os, re

from xiami_checker import *
from xiami_filter import *
from xiami_id_find import *
from xiami_tool import *


def run_normal(singer_o,album_o,keyword):
    singer,album,keywords = create_keywords(keyword)
    log(singer,'--',album)#
    point_singer = easy_check_songpage(singer, keywords)
    point_singer = check_filter(singer, point_singer)
    log(point_singer)#
    point_album = easy_check_albumpage(album, point_singer)
    log(point_album)#
    if point_album != None and len(point_album) > 0:
        log_find(point_album,singer_o,album_o)#
    log('-----------------------')#

def run_del_slash(singer_o,album_o,AB_tuple,func,sleep_time):
    if '/' in AB_tuple[0]:
        t = AB_tuple[0].split('/')
        t = filter(lambda i:i.replace('"""','').strip()!='',t)
        for j in zip(t,[AB_tuple[1]]*len(t)):
            func(singer_o,album_o,j)
            time.sleep(sleep_time)
    else:
        func(singer_o,album_o,AB_tuple)
        time.sleep(sleep_time)

def run_album(s, start_page=1, start_singer_name=None, sleep_time=8):
    flag = False
    totel_num = 0
    for keyword,num in groupby(s):
        temp_num = len(list(num))
        totel_num += temp_num
        if (start_singer_name == None or start_singer_name in keyword[0]) and totel_num >= start_page-1:
            flag = True
        if flag:
            log('**** groupnum: %d, totelnum: %d' % (temp_num, totel_num))
            singer_o,album_o,keyword = del_map_string(keyword)
            run_del_slash(singer_o,album_o,keyword,run_normal,sleep_time)



def run_id(s1,s2,names,turl_albums,sleep_time=1,start_place=None,start_page=1):
    songs = arl_songs(s1,s2,names)
    songids = arl_songsid(s2,turl_albums)
    flag = False
    for index,i in enumerate(songids,1):
        if (start_place==None or start_place == i) and index >= start_page:
            flag = True
        if flag:
            log(str(index))
            id2songs = [get_songs_id(j[0]) for j in songids[i]]
            id2songs = reduce(lambda i,j:i+j, id2songs)
            inds,A,B = i,songs[i],id2songs
            log(inds[0],' <-singer album-> ',inds[1])
            ####################
            t = B[:]
            for songA,indx in A:
                for i in filter_similar(songA,t,brackets=False):
                    t.remove(i)
            Bp = B[:]
            for i in t:
                Bp.remove(i)
            Bc = Bp[:]
            for songA,indx in A:
                d = {}
                if len(Bp)==0:
                    log('---- had album and no song ---- song: ',songA)
                    continue
                for songB,idx,check,release in filter_similar(songA,Bp,brackets=False):
                    d[compare_string_plus(songA,songB) + compare_string(songA,songB)] = (indx,songA,songB,idx,check,release)
                if len(d)!= 0:
                    try:
                        Bp.remove(list(d[max(d)][2:]))
                    except:
                        log(':::: bad remove')
                    log_id(d[max(d)])
                else:
                    for songB,idx,check,release in filter_similar(songA,Bc,brackets=False):
                        d[compare_string_plus(songA,songB) + compare_string(songA,songB)] = (indx,songA,songB,idx,check,release)
                    if len(d)!=0:
                        log_id(d[max(d)])
            #####################以这部分的函数对于歌名重复的策略已经成立
            #####################在满足任务需求的情况下，暂时已不需要修改
            log('------------------------------------------------------')
            time.sleep(sleep_time)



def easy_run(find=None,\
             xls1=None,\
             xls2=None,\
             table1_chr=3,\
             table2_chr=4,\
             params1=None,\
             params2=None,\
             xls1_start_row=1,\
             xls2_start_row=1):
    if find==None:
        log('Error')
        log('None Find Mode, pls Define (find = "album") or (find = "id")or (find = "fin")')
        return
    if find=='album':
        if (xls1==None) or (not os.path.isfile(xls1)):
            log('Not Find File xls1')
            return
        names, singers, albums = xls_read(xls1,table_chr=table1_chr)
        names = names[xls1_start_row:]
        s1 = zip(singers, albums)[xls1_start_row:]
        if params1==None:
            run_album(s1,sleep_time=5)
        else:
            start_page1 = params1['start_page']
            run_album(s1,sleep_time=5,start_page=start_page1)
            
        #查找专辑，尽量将【歌名，歌手，专辑】按顺序排在前三列。
        #另外也可以从 table1_chr DIY这三列的顺序。可接受list,序号从零开始
    elif find=='id':
        if (xls1==None or xls2==None) or (not (os.path.isfile(xls1) and os.path.isfile(xls2))):
            log('Not Find File xls1/xls2')
            return
        names, singers, albums = xls_read(xls1,table_chr=table1_chr)
        names = names[xls1_start_row:]
        urls, talbums, album2, singer2 = xls_read(xls2,table_chr=table2_chr)
        turl_albums = zip(urls,talbums)[xls2_start_row:]
        s1 = rm_quote(zip(singers, albums)[xls1_start_row:])
        s2 = rm_quote(zip(singer2, album2)[xls2_start_row:])
        if params2==None:
            run_id(s1,s2,names,turl_albums)
        else:
            start_page2 = params2['start_page']
            run_id(s1,s2,names,turl_albums,start_page=start_page2)
            
        #查找id用，尽量将【url，真专辑名，表专辑名，表歌手名】按顺序排在前四列。
        #另外也可以从 table1_chr DIY这三列的顺序。
        #前提是查找的专辑信息存入xls2文件里面
    elif find=='fin':
        if (xls1==None or xls2==None) or (not (os.path.isfile(xls1) and os.path.isfile(xls2))):
            log('Not Find File xls1/xls2')
            return
        names, singers, albums = xls_read(xls1,table_chr=table1_chr)
        names = names[xls1_start_row:]
        urls, talbums, album2, singer2 = xls_read(xls2,table_chr=table2_chr)
        turl_albums = zip(urls,talbums)[xls2_start_row:]
        s1 = rm_quote(zip(singers, albums)[xls1_start_row:])
        s2 = rm_quote(zip(singer2, album2)[xls2_start_row:])
        had = get_had_num_list(s1,s2)
        with open('is_or_not_hadalbum.txt','w')as f:
            for i in range(len(names)):
                if i in had:
                    f.write('有\n')
                else:
                    f.write('无专辑\n')
        xls_name3 = u'./xiami_id.log'
        dic = {}
        with open(xls_name3,'r')as f:
            for i in f:
                a,b,c,d,e,f = i.split('\t')
                a = re.findall('\d+',a)[0]
                dic[int(a)] = [b,c,d,e,f]
        print len(dic)
        with open('reference.txt','w')as f:
            for i in range(len(names)):
                if dic.has_key(i):
                    f.write('\t'.join(dic[i]))
                else:
                    f.write('\n')
    else:
        log('Error')
        log('Not Effect Key Word')
