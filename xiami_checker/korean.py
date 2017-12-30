# -*- coding: utf-8 -*-
import time
from xiami_lib.xiami_manager import *

def get_album_url_by_xpath(xtree):
    c = xtree.xpath('//*[@class="song_album"]/a')
    m = [zip([i.xpath('string(.)')[1:-1]],i.xpath('./@href')) for i in c]
    return reduce(lambda i,j:i+j,m)

def check_by_keyword(keyword):
    xtree = check_song_by_singer_init(keyword)
    if xtree == None:
        return None
    albums_urls = get_album_url_by_xpath(xtree)
    return set(albums_urls)

if __name__=='__main__':
    xls1=u'./new.xlsx'
    s = xls_read(xls1,[1,2])
    s = zip(*s)[1:]
    s = groupby(s)
    an = 0
    num=-1
    toggle = False
    for i,j in s:
        if an>num:
            toggle=True
        if toggle:
            a,b = i
            print a
            t = check_by_keyword(a)
            if t==None:
                continue
            t = filter_similar(a,t,brackets=False)
            log_find(t,a,b)
            time.sleep(1)
            print an,'-------------'
        an+=len(list(j))
        
    
    

