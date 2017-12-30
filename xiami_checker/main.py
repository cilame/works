# -*- coding: utf-8 -*-
from xiami_lib.xiami_manager import *

if __name__ == '__main__':

    xls1 = u'new.xlsx'
    xls2 = u'new2.xlsx'
    #easy_run(find="album", xls1=xls1, params1={'start_page':0})
    #这一步要保证 xls1 文件的存在
    #经过上步产生的txt文件手动全部复制写入新建xls文件并命名xls2
    #[歌名，艺人名，专辑名]

        
    easy_run(find="id", xls1=xls1, xls2=xls2, table1_chr=[0,2,1], params2={'start_page':107})
    #这一步要保证 xls1 和 xls2 文件的存在

    
    easy_run(find="fin", xls1=xls1, xls2=xls2)
    #这一步要保证 xls1, xls2 和 xiami_id.log 文件存在
