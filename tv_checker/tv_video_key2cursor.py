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
s.get('http://tvadmin.yunos-inc.com/#?dataid=100048399')
s.maximize_window()
time.sleep(15)
s.switch_to_frame(s.find_element_by_id("100048399"))

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
    time.sleep(1)
    try:
        f = s.find_element_by_xpath('//*[@id="datalist"]/table/tbody/tr/td[6]/a')
        f.click()
        time.sleep(3)
        leftclick()
        time.sleep(2)
        s.get_screenshot_as_file('pic/'+str(index)+'.png')
        rightclick()
        time.sleep(1)
    except:
        s.get_screenshot_as_file('pic/'+str(index)+'.png')
        time.sleep(1)

def main(startpage):
    keys = map(lambda i:i.strip(), open('t.txt').readlines())
    toggle = False
    for i,j in enumerate(keys,1):
        if i == startpage:
            toggle = True
        if toggle:
            print i
            run(i,j)

def temp(lists):
    keys = map(lambda i:i.strip(), open('t.txt').readlines())
    for i,j in enumerate(keys,1):
        if i in lists:
            print i
            run(i,j)
    
if __name__ == '__main__':
    print "start"
    main(start_num)

    
