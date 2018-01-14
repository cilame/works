import requests
from bs4 import BeautifulSoup
import re
import settings
from util import common


rule = ['https://jingyan.baidu.com',
        'baike.baidu.com',
        'https://zhidao.baidu.com',
        'https://baike.baidu.com/'
        ]


def crawl(search):
    if search is None:
        search = ''
    else:
        search = search.strip()
    base_url = 'https://www.baidu.com/s'
    queryString = settings.DEFAULT_QUERYSTRING
    queryString['wd'] = search
    headers = settings.DEFAULT_HEADERS
    response = requests.get(url=base_url, params=queryString, headers=headers)
    return load_html(response.text)


def load_html(content):
    html = BeautifulSoup(content, 'lxml')
    # print(html.prettify())
    # print(type(html))




    # 这里是获取百度左框中主要的显示内容，用于过滤网页框架其他部分的广告内容
    #################################
    # 这里之前代码没有考虑到 html.find('div', id='content_left') 找不到返回None的情况
    # 在输入一些无法找到的数据之后，程序直接报错弹出循环，已修改
    nodes = html.find('div', id='content_left')
    if not nodes:
        print('找不到该问题的相关答案.')
        return 
    nodes = nodes.find_all("div", class_='c-container')
    for node in nodes:





        # 数字计算
        #####################################################
        # 百度置顶显示的 calc 小程序置信度很高，优先考虑
        # 这里是直接使用百度搜索自带的数字计算框
        # 满足于搜索汉字罗马字符混合的输入  e.g.：“九十乘以4”
        calc_node = node.find(class_='op_new_cal_screen')
        if calc_node:
            calc_result = calc_node.find('p','op_new_val_screen_result').text.strip().replace(' ','')
            print(calc_result)
            return calc_result

        

        # 对 c-showurl 的节点进行收集
        ####################################################
        # 后续的处理全源于此
        target_url_node = node.find(class_="c-showurl")





        # 这里是对第一个节点进行特殊化对待处理
        #################################################
        # 如果第一个节点没有找到 c-showurl 且找到 c-span-last 则认为是岁数
        # 用了“除此之外”的逻辑，不是很好。
        if not target_url_node:
            if node.find('div', class_='c-span-last') is not None:
                abs_content_node = node.find('div', class_='c-span-last')
                print_content = common.process_c_span_last(abs_content_node)
                print(print_content) # 第一部分，搜索岁数时反馈内容
                return



        
        try:
            target_url = target_url_node.text
            # 对简要地址进行对比，看里面是否有置信度高的网址
            ################################################
            # 'baike', 'zhidao', 'baijia', 'jingyan','zhihu'
            # 对百度简要描述中的内容进行收集的过程
            # print(target_url_node['href'])      # 链接地址
            # print(target_url)       # 简要地址
            if common.check_url(target_url):
                if node.find('div', class_='c-abstract') is not None:
                    abs_content_node = node.find('div', class_='c-abstract')
                    print_content = common.process_c_abstract(abs_content_node)
                elif node.find('div', class_='c-span18') is not None:
                    abs_content_node = node.find('div', class_='c-span18')
                    print_content = common.process_c_span(abs_content_node)
                elif node.find('div', class_='c-border') is not None:
                    abs_content_node = node.find('div', class_='c-border')
                    print_content = common.process_c_border(abs_content_node)
                elif node.find('div', class_='c-span24')is not None:
                    abs_content_node = node.find('div', class_='c-span24')
                    print_content = common.process_c_span(abs_content_node)
                else:
                    print_content = ''



            # 第二部分，搜索天气时的反馈结果
            #################################################
            elif node.find_all('div', class_="xpath-log") is not None:
                print_content = common.process_c_xpath_log(node)
                temp = {}
                for i in range(5):
                    temp[print_content[0][i]] = print_content[1][i]
                print(temp)
                return

            # 搜索音乐的部分
            ###################################################
            # 这里查看是否节点中是否有 kuwo 音乐的地址，在再 common 中处理
            # 已在 setting 中多加一点 www.xiami.com, music.163.com, y.qq.com, www.kugou.com
            elif common.check_music_url(target_url):
                if node.find('div', class_='c-border') is not None:
                    abs_content_node = node.find('div', class_='c-border')
                    print_content = common.process_c_border(abs_content_node)



            

            # 不理解这段抽象的代码为何存在
            #######################################
            if nodes.__len__() == 1:
                if print_content:
                    # print(abs_content_node)   # 显示包括div
                    print(print_content.replace("[专业]", ''))      # 提取div里的text





            ##rule = ['https://jingyan.baidu.com',
            ##        'baike.baidu.com',
            ##        'https://zhidao.baidu.com',
            ##        'https://baike.baidu.com/'
            ##        ]
            else:
                # 这里出现逻辑问题
                #########################################
                # 因为有些搜索 target_url 的结果是 jingyan.baidu.com
                # 用源代码汇总下面的这样的判断非常非常的不靠谱
                # if target_url.split(".com")[0].__add__(".com") in rule:
                # 所以有如下修改
                if any(map(lambda i:target_url.split(".com")[0].__add__(".com")in i,rule)):
                    # 这里逻辑出现问题
                    ##########################################
                    # 源代码中出现了逻辑错误，在 node 之中没有抓到经验的 print_content 则返回 ""
                    # 那么即便是有经验，但是没有 print_content 也没有办法转到经验的页面，在 if print_content: 之后就已经消失了。
                    # 错误测试 e.g.“如何修电脑”，所以这里将删除 if print_content: 这个判断
                    # if print_content:

                    
                    # 百度经验的部分置信度很高，如果有就要单独进行处理
                    ###############################################################
                    # 这里的源代码判断方式不全，当 target_url.find("jingyan.baidu") == 0 时
                    # 需要 target_url_node.find_next_sibling() 来找到正确的 url 的内容
                    if target_url.find("jingyan.baidu") == 0:
                        ls = str(target_url_node.find_next_sibling())
                        rx = '(http://jingyan.baidu.com/article/[^\.]+\.html)'
                        _target = (re.findall(rx,ls)[0])
                    else:
                        _target = target_url_node['href']
                        
                    if target_url.find("jingyan.baidu") >= 0:
                        r = requests.get(_target, allow_redirects=False)
                        c_url = r.headers['Location']   # 获得重定向后的地址
                        response = requests.get(c_url)      # 百度经验次级页面...
                        htmls = BeautifulSoup(response.text, 'lxml')

                        # 输出步骤
                        ##############################################
                        # 这里对之前的步骤输入进行了一定的优化
                        node_list = htmls.find_all("div", class_='exp-content-block')
                        for nd in node_list[1:]:
                            nd_head = nd.find('h2',class_='exp-content-head')
                            if not nd_head or nd_head.text == '注意事项':
                                break
                            print('<-',nd_head.text,'->')
                            nd_list = nd.find_all('li', class_='exp-content-list')
                            for i, z in enumerate(nd_list, 1):
                                if nd_head.text == '工具/原料':
                                    pass
                                else:
                                    print("方法/步骤:", i)
                                if z.text.endswith('步骤阅读'):
                                    print(z.text.replace("百度经验:jingyan.baidu.com", '').replace('步骤阅读',''))
                                else:
                                    print(z.text.replace("百度经验:jingyan.baidu.com", '').replace('步骤阅读END',''))
                            print('--------')
                        return
                    else:
                        if print_content:
                            print(print_content.replace("[专业]", ''))
                            return

        except:
            target_url = ''
            pass

