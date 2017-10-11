from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException
import time,threading
import http.server
import socketserver
import operator

browser = webdriver.Chrome()
my_url = "http://study.163.com/message/msgList.htm"
 
'''
browser = webdriver.PhantomJS(executable_path=r'D:\phantomjs\bin\phantomjs.exe')
pagescript = "var page = this;page.onResourceReceived = function(res){page.browserLog.push({'url': res.url});}"
browser.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')
browser.execute('executePhantomScript', {'script': pagescript, 'args': []})
'''

class myhandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print("do get")
        actionLock.acquire()
        #deal all url
        actionLock.release()
        

def receiveUrl():
    hand = myhandler
    httpd = socketserver.TCPServer(("127.0.0.1", 12346), hand);
    httpd.serve_forever()
    
wait = WebDriverWait(browser, 5)
def getcookie():
    cookie_file = open(r"D:\project\packet\py\localcookie", "rb")
    cookie_str = cookie_file.read()
    cookie = eval(cookie_str.decode().replace("\"", ""))
    cookie_file.close()
    browser.get(my_url)
    for item in cookie:
        temp = dict(item)
        cookie_add = {}
        '''for key, value in temp.items():
            cookie_add[key] = value
        browser.add_cookie(cookie_add)'''
        browser.add_cookie(temp)
    browser.refresh()
    time.sleep(3)

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
    
    
def getvedio():
    ml_url = 'http://mooc.study.163.com/learn/deeplearning_ai-2001281002?tid=2001392029#/learn/content?type=detail&id=2001702003'
    browser.get(url=ml_url)
    time.sleep(5)
    
    
    weeks = browser.find_elements_by_xpath('//*[@id="courseLearn-inner-box"]/div/div/div[1]/div[1]/div/div[1]/div/div[2]/div')
    week_len = len(weeks)
    print('get weeks is %s' % week_len)
    urlfile = open(r'D:\project\packet\phan\urlfile', 'wb+')
    
    for j in range(week_len):
        #weeks group
        is_visible('//*[@id="courseLearn-inner-box"]/div/div/div[1]/div[1]/div/div[1]/div/div[@class="up j-up f-thide"]', 'click')
        #week item
        is_visible('//*[@id="courseLearn-inner-box"]/div/div/div[1]/div[1]/div/div[1]/div/div[2]/div', 'click')
        time.sleep(1)
        
        days = browser.find_elements_by_xpath('//*[@id="courseLearn-inner-box"]/div/div/div[1]/div[1]/div/div[2]/div/div[2]/div')
        print('get days is %s' % len(days))
        day_len = len(days)
        for i in range(day_len):
            is_visible('//*[@id="courseLearn-inner-box"]/div/div/div[1]/div[1]/div/div[2]/div/div[@class="up j-up f-thide"]','click')
            time.sleep(1)
            is_visible('//*[@id="courseLearn-inner-box"]/div/div/div[1]/div[1]/div/div[2]/div/div[2]/div[%d]' % i, 'click')
            #time.sleep(8)
            actionLock.release()
            actionLock.acquire()
            '''
            print("get url is %s\n" % str(browser.get_log('browser')))
            urlfile.write(str(browser.get_log('browser')).encode('utf8'))
            urlfile.flush()
            print("one day")
            '''
            
    urlfile.close()    
            
if __name__ == "__main__":
    t = threading.Thread(target=receiveUrl)
    t.start()
    getcookie()
    getvedio()
    