# -*- coding: utf-8 -*-
import requests, time
from xiami_tool import *

#这里内容是用在通过key进行搜索页面的HTML获取
#还有通过URL进行搜索页面的HTML获取

def get_html_by_word(keyword):
    headers = {'User-Agent': 'Chrome/46.0.2490.86'}
    url = 'http://www.xiami.com/search'
    try:
        s = requests.get(url=url, params={'key':keyword}, headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        log(':::: error requests. pls wait 20 sec.')
        time.sleep(20)
        return get_html_by_word(keyword)
    return s.content

def get_html_by_url(url):
    headers = {'User-Agent': 'Chrome/46.0.2490.86'}
    try:
        s = requests.get(url=url, headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        log(':::: error requests. pls wait 20 sec.')
        time.sleep(20)
        return get_html_by_url(url)
    return s.content
