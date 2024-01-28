import requests
import datetime

import asyncio
import json
from pathlib import Path

import subprocess
import time
import sqlite3

import re
import os
from os.path import expanduser

from core.seleniumbrowser import SeleniumBrowser

class Browser():

    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/122.0'
    USER_AGENT_EDGE = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/122.0.0.0"
    STEAM_BUFFER_SIZE = 512

    CAPTCHA_TIMEOUT = 5

    headers = {
        'User-Agent': USER_AGENT
    }

    def __init__(self):
        self.session = requests.Session()

    def getInternetIpAddress(self):
        return requests.get('https://api.ipify.org').text
    
    def getTimeStamp(self):
        # format current time in "2023-12-02T23:27:26+01:00" format
        return datetime.datetime.now().astimezone().isoformat()
            
    def launch_firefox(self, url, timeout = 10):
        process = subprocess.Popen(['/usr/bin/firefox', '-url', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if timeout:
            time.sleep(timeout)
        process.kill()

    
    def get_cookies_from_internal_storage(self, ff_cookies):
        con = sqlite3.connect(ff_cookies)
        cur = con.cursor()
        cur.execute("SELECT host, path, isSecure, expiry, name, value FROM moz_cookies where host like '%.bing.com%'")
        cookie_string = ""
        for item in cur.fetchall():
            #c = http.cookiejar.Cookie(0, item[4], item[5], None, False, item[0], item[0].startswith('.'), item[0].startswith('.'), item[1], False, item[2], item[3], item[3] == "", None, None, {})
            # get the cookie string to put in requests.get sentence 
            cookie_string += f"{item[4]}={item[5]}; "
            
        return cookie_string

    def extractCookiesFromRealFirefox(self, url):
        
        self.launch_firefox(url, Browser.CAPTCHA_TIMEOUT)

        return self.extractFirefoxCookies()

    def extractFirefoxCookies(self):
        firefox_cookies = "/tmp/cookies.sqlite"

        # get the system content of the file ~/.mozilla/firefox/profiles.ini
        response = os.popen("cat ~/.mozilla/firefox/profiles.ini").read()
        #print(response)
        # extract with regex all lines starting with Path= and without the "Path=" string
        regex = "(?<=Path=)(.*)"
        firefox_cookies_file = re.findall(regex, response)
        #print("checking for firefox cookies in:")
        cookies = ""
        # copy the firefox_cookies_files to /tmp if isset in system
        for file in firefox_cookies_file:
            next_file = expanduser(f"~/.mozilla/firefox/{file}/cookies.sqlite")
            if(os.path.isfile(next_file)):
                os.system(f"cp {next_file} /tmp")
                cookies = self.get_cookies_from_internal_storage(firefox_cookies)
                #print(f"Firefox cookies from {next_file} copied to {firefox_cookies}")
                # remove temp file
                os.system(f"rm {firefox_cookies}")
            else:
                print(f"File {next_file} not found.")
        return cookies
