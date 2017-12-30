# -*- coding: utf-8 -*-
from xiami_tool import *

from xiami_connect import *
from xiami_search import *
from xiami_filter import *

#这里就是专门用于统一 get_html 和 filter 两部分的功能
#主要是实现通过字符串即可获取搜索页面的HTML
#获取HTML之后用filter进行处理然后对结果进行判断

def check_song_by_singer_init(keyword):
    html = get_html_by_word(keyword)
    isrc = init_xpath_tree(html)
    if u'歌曲' not in isrc:
        if not is_exist_xpath('//div[@class="search_result_box"]/p[@class="seek_counts ok"]/strong',html):
            log(':::: maybe ip connect error. pls stop running.')
        log(':: None songs, keyword:',keyword)
        return None
    log(':: *Had songs, keyword:',keyword)
    return isrc[u'歌曲']

def check_filter(string,string_urls,brackets=True):
    filter_data1 = filter_equal(string,string_urls)
    filter_data2 = filter_similar(string,string_urls,brackets=brackets)
    filter_data = filter_data1 + filter_data2
    filter_data = map(tuple,filter_data)
    return list(set(filter_data))


#这里是主要描述如何通过关键字获取歌手地址并进行过滤的方法

def check_by_keyword(singer,keyword):
    xtree = check_song_by_singer_init(keyword)
    if xtree == None:
        return None
    songsers_urls = get_songs_and_url_by_xpath(xtree)
    return list(set(songsers_urls))

def easy_check_songpage(singer,keywords):
    if type(keywords) == str:
        return check_by_keyword(singer,keywords)
    elif type(keywords) == list:
        all_singer = [check_by_keyword(singer,keyword) for keyword in keywords]
        if all_singer.count(None) == 3:
            return []
        all_singer = [i for i in all_singer if i != None]
        all_singer = reduce(lambda i,j:i+j, all_singer)
        return all_singer


#这里是主要描述如何通过歌手地址获取id进而获取所有专辑名字进行过滤的方法

def check_by_idurl(album, urls):
    all_albums = get_singer_all_albums_by_string(urls)
    chk_albums = check_filter(album, all_albums, brackets=False)
    return chk_albums

def easy_check_albumpage(album, point_singer):
    if point_singer == []:
        return None
    singers,urls = zip(*point_singer)
    return check_by_idurl(album, urls)





