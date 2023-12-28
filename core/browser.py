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

class Browser():

    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0'
    USER_AGENT_EDGE = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    STEAM_BUFFER_SIZE = 512

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
    
    def solveCaptchaChrome(self, captchaUrl):
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import json

        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")

        driver = webdriver.Chrome(options=options)
        driver.get(captchaUrl) 
    
        # Espera hasta que el elemento con el ID 'success-text' sea visible
        try:
            success_text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "success-text"))
            )
            cookies = driver.get_cookie_string()
            driver.quit()
            cookies = json.loads(cookies) if cookies else {}
            print("Elemento encontrado y cookies obtenidas.")
            return cookies
        except:
            driver.quit()
            print("Elemento no encontrado después de 10 segundos.")
            return {}
        
    def solveCaptchaFirefox(self, captchaUrl, other):
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import json, time

        options = webdriver.FirefoxOptions()

        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        options.set_preference("window-size", "1920,1080")

        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("dom.webnotifications.enabled", False)

        profile = webdriver.FirefoxProfile()
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference("dom.webnotifications.enabled", False)

        service = webdriver.FirefoxService(firefox_profile = profile)

        driver = webdriver.Firefox(
            service= service,
            options = options
        )
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        #options.add_argument("--headless")
               
        time.sleep(2)
        driver.get(captchaUrl) 

        # wait for 'success-text'
        try:
            success_text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "success-text"))
            )
            cookies = driver.get_cookie_string()
            driver.quit()
            cookies = json.loads(cookies) if cookies else {}
            print("found element, coockes obtained.")
            return cookies
        except:
            screenshot = driver.get_screenshot_as_png()
            with open('screenshot.png', 'wb') as f:
                f.write(screenshot)
            driver.quit()
            print("element not found :'(")
            return {}
        
    def solveCaptcha2(self, captchaUrl, mainUrl):
        # call to solveCaptchaAsync
        #return asyncio.run(self.solveCaptchaAsync(captchaUrl, mainUrl))
        self.solveCaptchaSelenium(captchaUrl, mainUrl)
        
    def solveCaptchaSelenium(self, captchaUrl, mainUrl):
        from undetected_chromedriver import Chrome, ChromeOptions
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import json
        import time

        options = ChromeOptions()
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--headless=new")
        #options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        #options.add_argument("--disable-renderer-backgrounding")
        #options.add_argument("--disable-background-timer-throttling")
        #options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-client-side-phishing-detection")
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--disable-oopr-debug-crash-dump")
        options.add_argument("--no-crash-upload")
        #options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        #options.add_argument("--disable-low-res-tiling")
        #options.add_argument("--log-level=3")
        #options.add_argument("--silent")
        
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        #options.add_argument("user-agent="+self.USER_AGENT_EDGE)
        driver = Chrome(use_subprocess=False, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": self.USER_AGENT_EDGE})
        print(driver.execute_script("return navigator.userAgent;"))
        
        time.sleep(4)
        driver.get(mainUrl) 
        # wait 4 seconds
        time.sleep(4)

        # Open captchaUrl in a new tab
        driver.execute_script("window.location.href = '{}';".format(captchaUrl))
        
        try:
            ## error is caused by:
            ## https://challenges.cloudflare.com/cdn-cgi/challenge-platform/h/b/flow/ov1/39531545:1701774410:PuGLG-Yh-DxTHbLa2ykrQt6-LUcl6TTFFDl_iPlFLiM/830c05699a752fab/bfb90721bb496c6 400 code
            success_text = WebDriverWait(driver, 40).until(
                EC.presence_of_element_located((By.ID, "success-text"))
            )
            cookies = driver.get_cookie_string()
            driver.quit()
            cookies = json.loads(cookies) if cookies else {}
            print("found element, coockes obtained.")
            return cookies
        except:

            driver.execute_script("window.location.href = '{}';".format(captchaUrl))

            try:
                success_text = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "success-text"))
                )
                cookies = driver.get_cookie_string()
                driver.quit()
                cookies = json.loads(cookies) if cookies else {}
                print("element found, coockes obtained.")
                return cookies
            except:
                # store screenshot
                screenshot = driver.get_screenshot_as_png()
                with open('screenshot.png', 'wb') as f:
                    f.write(screenshot)
                driver.quit()
                print("Element not found after 10 seconds.")
                return {}
            
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
        firefox_cookies = "/tmp/cookies.sqlite"
        self.launch_firefox(url, 10)

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
