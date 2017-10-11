from selenium import webdriver
import time
import operator

browser = webdriver.Chrome()
usr = 'weilsheng@163.com'
pwd = '6991491'

def login():
    browser.get(url='http://study.163.com/member/login.htm')
    # 
    browser.switch_to.window(browser.window_handles[0])
    time.sleep(3)
    browser.find_element_by_xpath('//*[@id="form_parent"]/div[2]/div[1]/div[1]/div[2]').click()
    t = browser.find_element_by_xpath('//*[@id="form_parent"]/div[2]/div[1]/div[1]/div[1]').text
    print("get text is %s" % t)
    iframe = browser.find_element_by_xpath('//*[@class="wrap f-fl ursContainer f-pr"]/iframe')
    browser.switch_to.frame(iframe)
    browser.find_element_by_xpath('//*[@class="j-inputtext dlemail"]').send_keys(usr)
    browser.find_element_by_xpath('//*[@class="j-inputtext dlpwd"]').send_keys(pwd)
    browser.find_element_by_xpath('//*[@id="dologin"]').click()
    time.sleep(1)
    cookie = browser.get_cookies()
    cookie_file = open(r"D:\project\packet\py\localcookie", "wb+")
    cookie_file.write(str(cookie).encode('utf8'))
    cookie_file.close()

if __name__ == "__main__":
    login()