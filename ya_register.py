# -*- coding: utf-8 -*-
from splinter import Browser
from random import randint
import names, password_generator 
import StringIO, urllib
import base64
import time, datetime
import sys

def main():
        
    #how many accounts we need  
    ntimes = 1
        
    for i in range(1,ntimes+1):     
     
        print "starting browser"
        firstname = names.get_first_name()
        #print "firstname", firstname
        lastname = names.get_last_name()
        #print "lastname", lastname
                
        browser = Browser() #Browser(user_agent="Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en)")
        
        
        browser.visit('https://passport.yandex.com/registration/mail')
        
        browser.find_by_id('firstname').fill(firstname)
        browser.find_by_id('lastname').fill(lastname)
        
        testlogin = False
        count = 0
        while (testlogin == False):
            count = count + 1
            login = firstname+lastname+str(randint(10,1000))
            print "login:", login
            browser.find_by_id('login').fill(login)
            browser.is_element_not_present_by_css("div.control__error__login_notavailable", wait_time=2)
            if browser.is_text_present("username available"):
                testlogin = True
            else:
                print "login is not available, generate new"
            if (count>3):
                #print "logins in this script is unavailable now, please make new login generator"
                browser.quit()
                sys.exit("logins in this script is unavailable now, please make new login generator")
                
        password = password_generator.generate()
        print "password:", password

        browser.find_by_id('password').fill(password)
        browser.find_by_id('password_confirm').fill(password)
         
        #click on select   
        browser.find_by_name("hint_question_id").click()
        
        #wait 
        browser.is_element_not_present_by_css("li[role=\"presentation\"]", wait_time=3)
        
        #check first question
        browser.find_by_css("li[role=\"presentation\"]")[1].click()
        
        browser.find_by_id("hint_answer").fill(firstname)
        
        gateimgcode = "sgasafgdffff" #captcha(browser)
        browser.find_by_id('answer').fill(gateimgcode)
        
        browser.find_by_css("button[type=\"submit\"]").click()
        
        testcaptcha = False
        count = 0
        while (testcaptcha == False):
            count = count + 1
            browser.is_element_not_present_by_css("div.control__error__captcha_incorrect", wait_time=2)          
            if browser.is_text_present("characters were entered incorrectly"):
                print "captcha code is bad, try again"
                password = password_generator.generate()
                print "password:", password

                browser.find_by_id('password').fill(password)
                browser.find_by_id('password_confirm').fill(password)
                gateimgcode = captcha(browser)
                browser.find_by_id('answer').fill(gateimgcode)
                browser.find_by_css("button[type=\"submit\"]").click()
            else:
                testcaptcha = True
            if (count>3):
                #print "something wrong with captcha"
                browser.quit()
                sys.exit("something wrong with captcha")
                
        browser.is_element_not_present_by_tag("html", wait_time=2)
        
        if browser.is_text_present("Personal information"):        
            today = datetime.date.today()
            filename = 'yandex'+str(today)+'.txt'
            file = open(filename,'a')
            file.write(login+'@yandex.com'+':'+login+':'+password+'\n')
            file.close()
            print str(i)+" accounts saved to "+filename
            browser.quit()
        else:
            #print "something wrong, please start script again"
            browser.quit()
            sys.exit("something wrong, please start script again")
        
def captcha(browser):
    try:
        f = open('antigate.txt','r')
        gatecode = f.read()
        if (gatecode == 'antigate_user_key'):
            print "replace antigate_user_key in file antigate.txt"
            browser.quit()
        else:
            print "antigate code:", gatecode
        f.close()        
    except:
        print "error open antigate.txt file"
    #get url captcha
    url = browser.find_by_tag('img').last['src']
    #print url
    
    #put captcha in memory and open like file   
    file_like = StringIO.StringIO(urllib.urlopen(url).read())
    img = file_like.read()
    
    #send captcha to antigate.com
    captcha_id = antigateSend(img, gatecode)
    if (captcha_id == 'ERROR_NO_SLOT_AVAILABLE'):
        print 'captcha error', captcha_id
        browser.quit()
    print "sending captcha, wait..."
    gateimgcode = antigateGet(captcha_id, gatecode)
    if (gateimgcode == 'ERROR_WRONG_USER_KEY'):
        print 'something wrong with antigate user key', captcha_id
        browser.quit()
    print "get captca", gateimgcode
    
    return gateimgcode


def antigateSend(captcha, api_key, phrase=0, regsense=0, numeric=0, calc=0, min_len=0, max_len=0, is_russian=0):
    params = urllib.urlencode({
    'method': 'base64',
    'key': str( api_key),
    'body': base64.b64encode(captcha),
    'phrase': str( phrase),
    'regsense': str( regsense),
    'numeric': str( numeric),
    'calc': str( calc),
    'min_len': str( min_len),
    'max_len': str( max_len),
    'is_russian': str( is_russian)
    })
    answer = urllib.urlopen('http://antigate.com/in.php', params).read()
    if (answer[:2] == 'OK'): return answer[3:]
    else: return answer

def antigateGet(captcha_id, api_key):
    params = urllib.urlencode({'key': api_key, 'action': 'get', 'id': captcha_id})
    answer = urllib.urlopen("http://antigate.com/res.php?%s" % params).read()
    while(answer == 'CAPCHA_NOT_READY'):
        time.sleep(1)
        answer = urllib.urlopen("http://antigate.com/res.php?%s" % params).read()
    if (answer[:2] == 'OK'): return answer[3:]
    else: return answer

main()