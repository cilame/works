import settings
import re


def check_url(url):
    # re_urls=['baike', 'zhidao', 'baijia', 'jingyan','zhihu']
    re_urls = settings.QA_URLS
    for re_url in re_urls:
        if re.search(re_url, url):
            return True
    return False


def check_music_url(url):
    music_urls = settings.MUSIC_URLS
    for music_url in music_urls:
        if music_url == url.strip():
            return True
    return False


# 获得天气信息
def process_c_xpath_log(abs_content_node):
    local = abs_content_node.find('h3').find_all('a')[0].text[0:6] # 取得位置
    tems = abs_content_node.find('div', class_='op_weather4_twoicon').find_all('a')
    tem_date = []
    tem_temp = []
    for i in range(5):
        # 取时间
        if tems[i].find('p',class_='op_weather4_twoicon_date_day'):
            date = tems[i].find('p',class_='op_weather4_twoicon_date_day').text
        else:
            date = tems[i].find('p', class_='op_weather4_twoicon_date').text
        # 取温度
        temp = tems[i].find('p',class_='op_weather4_twoicon_temp').text
        tem_date.append(date.strip()[0:6])
        tem_temp.append(temp)
    return tem_date,tem_temp

    
def process_c_abstract(c_abstract_node):
    for each_text_nodes in c_abstract_node.contents:
        tag_name = each_text_nodes.name
        try:
            tag_class = each_text_nodes.get('class', None)
        except:
            tag_class = None
        if tag_name:
            if tag_name not in settings.C_ABSTRACT_CLEAR_TAGS:
                each_text_nodes.clear()
    content = process_content(c_abstract_node.text)
    return content


def process_c_border(abs_content_node):
    if abs_content_node.find('div', class_='op-misuc-lrc-text-c') is not None:
        text_nodes = abs_content_node.find('div', class_='op-misuc-lrc-text-c')
        text_list = []
        for each_node in text_nodes.contents:
            tag_name = each_node.name
            try:
                tag_class = each_node.get('class', None)
            except:
                tag_class = None
            if  tag_name and tag_name == 'p' and tag_class and 'wa-musicsong-lyric-line' in tag_class:
                text_list.append(each_node.text.strip())
        return '/'.join(text_list)
    else:
        for each_text_nodes in abs_content_node.contents:
            # tag_name = each_text_nodes.name
            try:
                tag_class = each_text_nodes.get('class', None)
            except:
                tag_class = None

            # if tag_class is not None and 'c-row' in tag_class:
            #     contents_list = each_text_nodes.find_all('p',class_='c-gap-top-small')
            #     final_content = ''
            #     for each_tag in contents_list:
            #         content = each_tag.text
            #         content = process_content(content)
            #         if content != '':
            #             final_content += content
            #   return final_content


def process_c_span_last(abs_content_node):
    text_list = []
    for each_a_node in abs_content_node.find_all('a'):
        each_a_node.clear()
    for each_text_node in abs_content_node.contents:
        tag_name = each_text_node.name
        try:
            tag_class = each_text_node.get('class', None)
        except:
            tag_class = None
        if tag_class and ('f13' in tag_class or 'op-bk-polysemy-move'in tag_class):
            each_text_node.clear()
            continue

        if tag_name:
            if tag_name == 'p':
                each_string = each_text_node.text
                text_list.append(process_content(each_string))
            elif tag_name == 'div':
                if tag_class:
                    if 'op_exactqa_s_answer' in tag_class:
                        each_string = each_text_node.text
                        text_list.append(process_content(each_string.strip()))
    return ' '.join(text_list)

    try:
        abs_content = abs_content_node.text
    except:
        abs_content = ''
    content = process_content(abs_content.strip())
    # content = proecss_content_tags(abs_content_node)
    # print(content)
    return content


def process_c_span(abs_content_node):
    for each_text_nodes in abs_content_node.contents:
        tag_name = each_text_nodes.name
        try:
            tag_class = each_text_nodes.get('class', None)
        except:
            tag_class = None
        if tag_class is not None and ('f13' in tag_class or 'op-bk-polysemy-move'in tag_class):
            each_text_nodes.clear()
            continue

        if tag_name != None :
            if tag_name == 'p':
                for cont in each_text_nodes.contents:
                    each_tag_name = cont.name
                    if each_tag_name and each_tag_name != 'em' :
                        cont.clear()

                tt = each_text_nodes.string
                optimize_c_span_node(each_text_nodes)
                    # else:
                    #     cont.text = refine_content(cont.text)
                    # exec('each_text_nodes.{}.clear()'.format(tag_name))
            # elif tag_name == 'a':
            #     for cont in each_text_nodes.contents:

    try:
        abs_content = abs_content_node.text
    except:
        abs_content = ''
    content = process_content(abs_content.strip())
    # content = proecss_content_tags(abs_content_node)
    # print(content)
    return content


def process_content_tags(abs_content_node):

    final_content = ''
    c_list = []
    for each_text_nodes in abs_content_node.contents:

        try:
            text = each_text_nodes.text
        except:
            text = ''
        c_list.append(process_content(text))
    final_content = ' '.join(c_list)
    return final_content


def process_content(content):

    if content == '':
        return ''
    else:
        content = content.replace('\n','').strip('-').strip()
        if content.endswith('...'):
            ends_tag_list = ['。', '！', '？', '!', '?', ';']
            for index in range(len(content)-1,-1,-1):
                if content[index] in ends_tag_list:
                    re_content = content[:index+1].replace('...','').strip()
                    re_content = refine_content(re_content)
                    return re_content
            return ''
        else:
            re_content = refine_content(content.strip())
            return re_content
            return content.strip()

    return content.strip()


def refine_content(content, stop_words_list=settings.STOP_WORDS_LIST):
    for stop_word in stop_words_list:
        stop_word_re = re.compile(stop_word)
        content = stop_word_re.sub('', content)
    return content.strip()


def optimize_c_span_node(node):
    text = node.text
    for each in text:
        if each in [':', "："]:
            tmp_string = text[text.index(each) + 1:].strip()
            if len(tmp_string) > 0 and tmp_string[-1] not in [',', '.', '，', '。']:
                tmp_string += '。'
            node.string = process_content(tmp_string)
            break
    # return node.text
