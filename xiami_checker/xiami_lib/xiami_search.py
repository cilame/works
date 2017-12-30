# -*- coding: utf-8 -*-
import re
from lxml import etree
from xiami_tool import *

#这里面的内容主要是用在通过搜索后的页面将搜索页的HTML
#抽出来获取【歌曲】，【歌手】，【专辑】部分的内容进行处理

#init-------------------
def init_xpath_tree(html):
    e = etree.HTML(html)
    v = e.xpath('//*[@id="wrapper"]/div[2]/div[1]/div/div[2]/div')
    i = map(lambda i:i.xpath('string(./h5)'),v)
    return dict(zip(i,v))

#songs-------------------
def get_songs_info(xtree):
    song   = xtree.xpath('string(.)').strip()
    singer = xtree.xpath('string(./../td[@class="song_artist"])').strip()
    album  = xtree.xpath('string(./../td[@class="song_album"])').strip()
    return map(filter_space,[song,singer,album])
def get_songs_by_xpath(xtree):
    s = xtree.xpath('.//td[@class="song_name"]')
    return map(get_songs_info,s)

#songs & url--------------
def get_songs_and_url_info(xtree):
    singer = xtree.xpath('./../td[@class="song_artist"]/a/@title')
    for i in range(1,len(singer)):
        singer[i] = xtree.xpath('string(./../td[@class="song_artist"]/a[%d])'%(i+1)).strip()
    urls   = xtree.xpath('./../td[@class="song_artist"]/a/@href')
    return singer,urls
def get_songs_and_url_by_xpath(xtree):
    s = xtree.xpath('.//td[@class="song_name"]')
    s = map(get_songs_and_url_info,s)
    s = map(lambda z:reduce(lambda i,j:i+j,z),zip(*s))
    return zip(s[0],s[1])

#ablums-------------------
def get_albums_info(xtree):
    album   = xtree.xpath('./a[@class="song"]/@title')[0].strip()
    singer  = xtree.xpath('string(./a[@class="singer"])').strip()
    return map(filter_space,[album,singer])
def get_albums_by_xpath(xtree):
    s = xtree.xpath('.//p[@class="name"]')
    return map(get_albums_info,s)

#singers-------------------
def get_singers_info(xtree):
    singer = xtree.xpath('./a/@title')[0].strip()
    return filter_space(singer)
def get_singers_by_xpath(xtree):
    s = xtree.xpath('.//p[@class="buddy"]')
    return map(get_singers_info,s)



from math import ceil
from xiami_connect import *

#这里就是通过歌手页面获取其歌手id
#然后通过歌手id进行专辑名字和地址的收集

def get_all_albums_num_by_url(url):
    html = get_html_by_url(url)
    xtree = etree.HTML(html)
    stree = xtree.xpath('string(//*[@id="artist_albums"]/div[1]/p)')
    albums_num = int(re.findall('\d+',stree)[0])
    if albums_num == 0:
        page_num = 0
    else:
        page_num = int(ceil(float(albums_num)/12))
    return albums_num,page_num

def get_all_albums_name_by_url(url):
    s = get_html_by_url(url)
    e = etree.HTML(s)
    albums = e.xpath('//*[@id="artist_albums"]/div[@class="albumThread_list"]/ul/li')
    albums = map(lambda i:[i.xpath('.//p[@class="name"]/a/@title')[0],\
                           i.xpath('.//p[@class="name"]/a/@href')[0]],\
                         albums)
    return albums
    
def get_singer_all_albums_by_string(urls):
    s = 'http://www.xiami.com/artist/album-'
    filter_id = ['bMgK23ea4','WeU99a9d','ueF379d0','bgrSabed9','bAlN19c4c']
    urls_id   = filter(lambda k:k not in filter_id,[i[28:] for i in urls])
    urls = map(lambda i:s+i,urls_id)
    albums_and_ids = []
    for url in urls:
        num,page = get_all_albums_num_by_url(url)
        log(':: url:',url)
        log(':: num:',num)
        log(':: page:',page)
        if page > 20:page = 20
        if page > 1000:
            log(':::: special url!!')
        for i in range(1,page+1):
            iurl = url+'?page='+str(i)
            for album_name,album_id in get_all_albums_name_by_url(iurl):
                albums_and_ids.append([album_name,album_id])
    return albums_and_ids


