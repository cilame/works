# -*- coding: utf-8 -*-
import difflib
from xiami_tool import *

#这里是主要的过滤器，对 [(singer,singer_url), ...] 这样格式的内容进行过滤。

def filter_equal(string,songsers_urls):
    stringB = string.upper().replace('"""','')
    filter_data = []
    for i in songsers_urls:
        stringA = i[0].upper().replace('"""','')
        if has_brackets(stringA,stringB) < .23:
            if (stringB in stringA or stringA in stringB) and len(stringA) > 0:
                filter_data.append(i)
    return filter_data
    
def filter_similar(string,songsers_urls,brackets=True):
    stringB = string.upper().replace('"""','')
    filter_data = []
    for i in songsers_urls:
        stringA = i[0].upper().replace('"""','')
        if brackets:
            if has_brackets(stringA,stringB) < .23:
                if compare_string_plus(stringA,stringB) > .70 and len(stringA) > 0:
                    filter_data.append(i)
        else:
            if compare_string_plus(stringA,stringB) > .70 and len(stringA) > 0:
                filter_data.append(i)
    return filter_data





