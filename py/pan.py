from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException, WebDriverException
import time
import operator
import re
import os, sys
import base64
from docopt import docopt
import argparse
parser = argparse.ArgumentParser(description="your script description")
parser.add_argument('--cookie', '-c',  type = str)
parser.add_argument('--img', '-i',  type = str)
args = parser.parse_args()

dirName = r"F:\zhong\z\\"

imgPath = r'F:\temp3\imgDict\\'
imgname = 0
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 5)

cookiname =  ''
def getcookie():
    cookie_file = open(cookiname, "rb")
    cookie_str = cookie_file.read()
    cookie = eval(cookie_str.decode())
    cookie_file.close()
    browser.get('https://pan.baidu.com/')
    for item in cookie:
        temp = dict(item)
        cookie_add = {}
        browser.add_cookie(temp)
    browser.refresh()
    time.sleep(3)
    
def login():
    getcookie()
    time.sleep(2)
	
def is_visible(locator, type='', msg="", back=False, loop=False):
    #while True:
    try:
        item = wait.until(lambda x:x.find_element_by_xpath(locator))
        if operator.eq(type, "click"):
            item.click()
        elif operator.eq(type, "send"):
            item.send_keys(msg)
        elif operator.eq(type, "submit"):
            item.submit()
        elif operator.eq(type, "text"):
            return item.text
        else:
            return True
        
        #break     
    except TimeoutException:
        if back == True:
            return False
        print("%s Time out" % locator)
        #continue
    except ElementNotVisibleException:
        print("%s item is NoVisible" % locator)
        return True
           
def saveFileNameImg(byte_str, imgIndex):
    bytestr =  byte_str.replace('data:image/png;base64,', '').replace('"', '')
    img_byte = base64.b64decode(bytestr)
    f = open('%s%s.png' % (str(imgPath), str(imgIndex)), 'wb')
    f.write(img_byte)
    f.close()

def getFile(panurl, pwd):
    global imgname
    browser.get(url = panurl)
    print(panurl)
    is_visible('//*[@id="hvyVEbB"]', "send", pwd, loop=True)     #密码框
    is_visible('//*[@id="eci20zV"]/a/span', "click")         #密码进入    
    file_img_byte = browser.find_element_by_xpath('//*[@id="layoutMain"]/div[1]/div[1]/div/div[1]/h2/img').get_attribute('src')
    saveFileNameImg(file_img_byte, imgname)
    name = '%s.txt' % (str(imgname))
    imgname += 1
    #name = is_visible(('//*[@id="layoutMain"]/div[1]/div[1]/div/div[1]/h2','text')

    print('file name is ' + name)
    is_visible('//*[@id="layoutMain"]/div[1]/div[1]/div/div[2]/div/div/div[2]/a[1]/span', 'click')
    
    while not is_visible('//*[@id="fileTreeDialog"]'):
        print("dont get file free")
        is_visible('//*[@id="layoutMain"]/div[1]/div[1]/div/div[2]/div/div/div[2]/a[1]/span', 'click')
    
    #is_visible('//*[@id="fileTreeDialog"]/div[2]/div/ul/li/ul/li[21]/div', 'click', True)
    #time.sleep(0.3)
    
    is_visible('//*[@id="fileTreeDialog"]/div[3]/a[2]/span', 'click')
    time.sleep(0.1)
    is_visible('//*[@id="fileTreeDialog"]/div[4]/a[2]/span', 'click')
    is_visible('//*[@id="fileTreeDialog"]')
    time.sleep(0.3)
    return name
    
def openFile_get(filename):
    path = dirName + filename
    try:
        f = open(path,"r",encoding='utf-8')
        all = f.read()
    except UnicodeDecodeError:
        f = open(path,"r",encoding='gb18030')
        all = f.read()
    
    
    try:    
        url = re.search("http.*/[\w-]+", all).group()
        url_pwd = re.search(r"(?<=[密码][:：]).*?[\w]{4}", all).group()
    except AttributeError:
        print("search pwd error")
        return
    else:
        f.close()
        print('url is %s password is %s' %(url,url_pwd))
        newfianeme = getFile(url, url_pwd)
        if len(newfianeme) == 0:
            #os.remove(path)
            print("file is none")
        else:
            try:
                os.rename(path, dirName + newfianeme + '.txt')
            except FileExistsError:
                pass
            
    
def listdir():
    for file in os.listdir(dirName):
        try:
            print(file)
        except:
            pass
        openFile_get(file)
		
if __name__ == "__main__":	
    if args.cookie:
        print(args.cookie)
        cookiname =  r'F:\zhong\localcookie%s' % (args.cookie) 
     if args.img:
        imgname = int(args.img)
    login()
    time.sleep(2)
    listdir()