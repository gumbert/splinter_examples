# -*- coding: utf-8 -*-
from splinter import Browser
from random import randint
import names
import password_generator
import StringIO, urllib
import base64
import time, datetime

def main():
        
    #how many accounts we need  
    ntimes = 1
        
    for i in range(1,ntimes+1):     
        try:
            f = open('antigate.txt','r')
            gatecode = f.read()
            if (gatecode == 'antigate_user_key'):
                print "replace antigate_user_key in file antigate.txt"
                break
            else:
                print "antigate code ok", gatecode
            f.close()
            
        except:
            print "error open antigate.txt file"
     
        #print i
        firstname = names.get_first_name()
        print "firstname", firstname
        lastname = names.get_last_name()
        print "lastname", lastname
        login = firstname+lastname+str(randint(10,1000))
        print "login", login
        password = password_generator.generate()
        print "password", password
        
        browser = Browser() #Browser(user_agent="Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en)")
        
        
        browser.visit('https://passport.yandex.com/registration/mail')
        
        browser.find_by_id('firstname').fill(firstname)
        browser.find_by_id('lastname').fill(lastname)
        
        browser.find_by_id('login').fill(login)
        browser.find_by_id('password').fill(password)
        browser.find_by_id('password_confirm').fill(password)
         
        #click on select   
        browser.find_by_name("hint_question_id").click()
        
        #wait 
        browser.is_element_not_present_by_css("li[role=\"presentation\"]", wait_time=2)
        
        #check first question
        browser.find_by_css("li[role=\"presentation\"]")[1].click()
        
        browser.find_by_id("hint_answer").fill(firstname)
        
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
            break
        print "sending captcha, wait..."
        gateimgcode = antigateGet(captcha_id, gatecode)
        if (gateimgcode == 'ERROR_WRONG_USER_KEY'):
            print 'something wrong with antigate user key', captcha_id
            browser.quit()
            break
        print "get captca", gateimgcode
        
        browser.find_by_id('answer').fill(gateimgcode)
        
        browser.find_by_css("button[type=\"submit\"]").click()
        browser.is_element_not_present_by_tag("html", wait_time=2)
        
        today = datetime.date.today()
        filename = 'yandex'+str(today)+'.txt'
        file = open(filename,'a')
        file.write(login+'@yandex.com'+':'+login+':'+password+'\n')
        file.close()
        
        print str(i)+" accounts saved to"+filename
            
        browser.quit()

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