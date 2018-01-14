QA_URLS = ['baike', 'zhidao', 'baijia', 'jingyan','zhihu','dajie']
MUSIC_URLS = ['www.kuwo.cn','www.xiami.com','music.163.com','y.qq.com','www.kugou.com']

# c-abstract标签下需要清除内容的标签
C_ABSTRACT_CLEAR_TAGS = ['a', 'span', 'br', 'p']

STOP_WORDS_PATH = './STOP_WORDS.txt'
with open(STOP_WORDS_PATH, 'r', encoding="utf-8") as fp:
    STOP_WORDS_LIST = []
    for line in fp.readlines():
        STOP_WORDS_LIST.append(line.strip('\n'))


DEFAULT_QUERYSTRING = {
    # 'ie': 'utf-8',
    # 'newi': '1',
    # 'mod': '1',
    # 'isid': '178D2FB667E18526',
    #'wd': search,
    # 'rsv_spt': '1',
    # 'rsv_iqid': '0xedb5b94e000008a7',
    # 'issp': '1',
    # 'f': '3',
    # 'rsv_bp': '0',
    # 'rsv_idx': '2',
    # 'tn': 'baiduhome_pg',
    # 'rsv_enter': '0',
    # 'rsv_sug3': '15',
    # 'rsv_sug1': '15',
    # 'rsv_sug7': '100',
    # 'prefixsug': '%E8%8B%B9%E6%9E%9C',
    # 'rsp': '0',
    # 'inputT': '6031',
    # 'rsv_sug4': '6628',
    # 'rsv_sid': '25421_1423_21125_18559_17001_25441_25435_25177_20719',
    # '_ss': '1',
    # 'clist': '',
    # 'hsug': '',
    # 'f4s': '1',
    # 'csor': '2',
    # '_cr1': '28795',
}

DEFAULT_HEADERS={
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': 'BAIDUID=178D2FB617D61759E9DB1B34307B667E:FG=1; BIDUPSID=1C3C3290019ABB1797B00EA3803C80D3; PSTM=1495552015; __cfduid=d89e64de365c942008106bc62863f0abe1508820292; BDSFRCVID=IftsJeC62RyOlYRA5LrbwN6wig3NWqOTH6aooEeFbQ08JZnQlcp3EG0PJU8g0KubVI2-ogKK0eOTHkbP; H_BDCLCKID_SF=tJ4f_KDytCv5j5ru5DTHh4I0MU_X5-RLfbRp_POF5l8-hCTyXpr2XU_uMlr9-MCqbK5MabjttfjxOKQphp6b-xKXjaJW5xP82gb20hcN3KJmqfK9bT3v5DumLtAH2-biWbR-2Mbd2bombCDxDj0ajjvLepb3ejLOHD7yWCkh2fJ5OR5Jj65Cb-IT5J5CQ4TGLTvw_t3V5hvHHCoh3MA--t4Hypuf0Jbr2jb-2ln23t3bsq0x0bQYe-bQyp_L5h395KOMahkM5l7xObvP05CaejjLeauDJjne2Poa3RRHbPK_Hn7zeT515btpbt-qJj38am7P3qjl2JoJfpuC5PrF0pDQjabnBT5Ka268bhLX2R3roRO5yPREX5KkQN3T0PKO5bRiLRoH2pn4Dn3oyT3qXp0nMU5Tqj_8tJCOVCD-f-OsKRoph-oM5DCShUFs5q5A-2Q-5KL-JJ3nqh5OLqQ8Xq4WXGjfa4b-2HvybxbdJJjofhF9y-Ot3ptZefo7XxngK2TxoUJhQCnJhhvG-4osyhKebPRiJPQ9QgbW3ftLJKtKMDKRj5Rb5nbHKf4etjLXKKOLVMPK3tOkeq8CD4uVKb_s04QIafuJb2_qLbTjWhcabK52y5jHhPj0jf8DKpJjW5-tXDDyL-bpsIJMb4DWbT8U5eFt3M4taKviaKJHBMb1jnoMe6LbejbQjGL8q-JQ2C7WsJjs24ThD6rnhPF3ytAvKP6-35KH0KOmBPTF0xnTshR6X6jbMJKUXqJDBq37JD6y_t3k-h3NexL4WtJjb-_U2-oxJpOR5JbMopvaKfQzh66vbURvD-Lg3-7W5q8EtRk8_KtKtCI3HnRY-P4_-tAt2qoXetJyaR3A0tbbWJ5TMCo-2fnSWqDFjtvH5JbwJjv00KOkQ-jcShPC-tnoQtLz-RLjqUTzaH6Q3-tb3l02Vhcae-t2ynLV34uHe4RMW20j0l7mWnvDVKcnK4-XDjQ0jNJP; BD_UPN=123253; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; MCITY=-289%3A; H_PS_PSSID=25421_1423_21125_18559_17001_25441_25435_25177_20719; BD_CK_SAM=1; PSINO=5; BD_HOME=1; sug=3; sugstore=0; ORIGIN=2; bdime=0; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; H_PS_645EC=999a%2Fl%2F64f4Dwb0s8ePlRuayAWEQbTAPcapmg179rIAXWsRYp1F2%2F%2FwkfvwwxJ5ekVp8; WWW_ST=1513839211837',
    'Host': 'www.baidu.com',
    'is_referer': 'https://www.baidu.com/',
    # 'is_xhr': '1',
    # 'Referer': 'https://www.baidu.com/s?wd=%E8%8B%B9%E6%9E%9C&rsv_spt=1&rsv_iqid=0xedb5b94e000008a7&issp=1&f=3&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=0&rsv_sug3=15&rsv_sug1=15&rsv_sug7=100&prefixsug=%25E8%258B%25B9%25E6%259E%259C&rsp=0&inputT=6031&rsv_sug4=6628',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',

}
