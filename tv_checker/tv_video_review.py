# -*- coding: utf-8 -*-
import win32api
import win32con

from selenium import webdriver
import time,os

start_num = raw_input('pls input start_num(default 1):')
start_num = 1 if start_num=="" else int(start_num)

if not os.path.isdir('pic'):
    os.mkdir('pic')

driver = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
op = webdriver.ChromeOptions()
op.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
op.binary_location=driver
s = webdriver.Chrome(chrome_options=op)
s.get('http://tvadmin.yunos-inc.com/#?dataid=100051408')
s.maximize_window()
time.sleep(15)
s.switch_to_frame(s.find_element_by_id("100051408"))

def leftclick():
    win32api.SetCursorPos([459,713])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
def rightclick():
    win32api.SetCursorPos([1329,251])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)

def run(index,key):
    v = s.find_element_by_id("extVideoStrId")
    v.clear()
    v.send_keys(key)
    c = s.find_element_by_id("search_btn")
    c.click()
    time.sleep(2)

    # 判断时间是否超过五分钟，超过则不用审核
    f = s.find_element_by_xpath('//*[@id="datalist"]/table/tbody/tr[1]/td[10]')
    try:
        k = int(f.text.split(':')[0])
    except:
        k = 1000
    if int(f.text.split(':')[0]) >=5:
        a = s.find_element_by_xpath('//*[@id="datalist"]/table/tbody/tr/td[9]/div/dd[1]/span')
        b = s.find_element_by_xpath('//*[@id="datalist"]/table/tbody/tr/td[9]/div/dd[2]/span')
        print a.text,b.text,'timeout'
        return

    # 处理一系列弹出框的问题，是用以简单审核

    f = s.find_element_by_xpath('//*[@id="datalist"]/table/tbody/tr/td[2]/div/a[3]/nobr')
    f.click()
    time.sleep(2)
    s.switch_to.default_content()
    s.switch_to_frame(s.find_element_by_id('modalFrame'))
    f = s.find_element_by_xpath('//*[@id="form3"]/table/tbody/tr[3]/td/div/label[1]')
    f.click()
    f = s.find_element_by_xpath('//*[@id="form3"]/table/tbody/tr[3]/td/div/label[2]')
    f.click()
    time.sleep(.5)
    f = s.find_element_by_xpath('//*[@id="form3"]/div/div/button[2]')
    f.click()
    alert = s.switch_to_alert()
    time.sleep(1)
    alert.accept()
    alert = s.switch_to_alert()
    time.sleep(1)
    alert.accept()

    time.sleep(1)
    f = s.find_element_by_xpath('//*[@id="form3"]/div/div/button[1]')
    f.click()
    
    time.sleep(3)
    s.switch_to.default_content()
    s.switch_to_frame(s.find_element_by_id("100051408"))
    time.sleep(3)
    ###############################################

    a = s.find_element_by_xpath('//*[@id="datalist"]/table/tbody/tr/td[9]/div/dd[1]/span')
    b = s.find_element_by_xpath('//*[@id="datalist"]/table/tbody/tr/td[9]/div/dd[2]/span')
    print a.text,b.text,'checked'

def main(startpage):
    keys = map(lambda i:i.strip(), open('ts.txt').readlines())
    needkeys = map(lambda i:i.strip(), open('tss.txt').readlines())
    toggle = False
    for i,j in enumerate(keys,1):
        if i == startpage:
            toggle = True
        if toggle:
            print i,
            if j not in needkeys:
                print
                continue
            run(i,j)

def temp(lists):
    keys = map(lambda i:i.strip(), open('ts.txt').readlines())
    for i,j in enumerate(keys,1):
        if i in lists:
            print i
            run(i,j)
    
if __name__ == '__main__':
    print "start"
    main(start_num)

    
