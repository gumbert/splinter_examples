# -*- coding: utf-8 -*-
from splinter import Browser
import csv, ast
import sys, os

#profile = {'network.proxy.http': 'IPADDRESSS',
#'network.proxy.http_port': 21301,
#'network.proxy.type': 1}
# 0 (default): Direct connection to the Internet (no proxy used)
# 1: Manual proxy configuration (use values in network.proxy.*)
# 2: Autoconfiguration by URL (use value in network.proxy.autoconfig_url)
# 3: Same as 0 for compatibility reasons (see bug 115720) and will be reset to 0
# 4: Auto-detect proxy settings for this network

def main():
    fname = "proxy.txt"
    
    try:
        f = open(fname, 'r')
        if os.stat(fname).st_size==0:
            print "has no proxy, use your ip"
            dosmth(False)       
        else:
            print "find "+str(enumerate(f,1))+" proxys"
            dosmth(True, fname) 
    except IOError:
        print "can't read or open proxy file: "+fname
        print "has no proxy, use your ip"
        dosmth(False)
        #sys.exit("can't read or open proxy file: "+fname)
        
def dosmth(*arg):
    #First argument True or False. When True use proxy in file 'fname', else use machine ip.
    print arg
    if not arg[0]:
        browser = Browser()
        browser.visit("http://www.ip-ping.ru/")
        print browser.find_by_css("div.hc2").text
        browser.quit()
    else:
        fname = arg[1]
        with open(fname, 'r') as f:
            reader = csv.reader(f, delimiter=":")
            profiles = []
            for ip, port in reader:
                #print type(ip), port
                profiles.append("{'network.proxy.http':'"+ip+"','network.proxy.http_port':"+port+",'network.proxy.type': 1}")
                
            for profile in profiles:
                print profile
                profile = ast.literal_eval(profile)
                browser = Browser(profile_preferences = profile)
                 
                browser.visit("http://www.ip-ping.ru/")
                print browser.find_by_css("div.hc2").text
                browser.quit()
            
main()
