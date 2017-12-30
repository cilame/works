# -*- coding: utf-8 -*-
from xiami_connect import *
from lxml import etree

def get_songs_id(url):
    if not url.startswith('http://'):
        url = 'http://www.xiami.com'+url
    s = get_html_by_url(url)
    e = etree.HTML(s)
    x = len(e.xpath('//*[@id="album_cover"]/span'))
    m = [[''.join(i.xpath('string(.)')), \
          i.xpath('./../../td[@class="chkbox"]/input/@value')[0],\
          '' if len(i.xpath('./../../td[@class="chkbox"]/input/@checked'))>0 else u'下架',\
          '' if not x else u'未发布']
        for i in e.xpath('//*[@class="song_name"]/a[1]')]
    return m

