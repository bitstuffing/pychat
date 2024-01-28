from undetected_chromedriver import Chrome, ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

class SeleniumBrowser:

    USER_AGENT_EDGE = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/90.0.818.49"
        
    def __init__(self, mainUrl):

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

        # wait for the page to load
        time.sleep(4)

        # find the login input fields and fill them
        # username is an input with aria-label="Email / Username"
        driver.find_element_by_css_selector("input[aria-label=\"Email / Username\"]").send_keys("parekot353@bitofee.com")
        # password is an input with aria-label="Password"
        driver.find_element_by_css_selector("input[aria-label=\"Password\"]").send_keys("Passwd.11")

        # confirm that we have filled the fields
        print(driver.find_element_by_css_selector("input[aria-label=\"Email / Username\"]").get_attribute('value'))
        print(driver.find_element_by_css_selector("input[aria-label=\"Password\"]").get_attribute('value'))

        # find submit button and click it
        driver.find_element_by_css_selector("button[type=\"button\"]").click()

        # wait for the page to load
        time.sleep(10)

        # get the cookies
        driver_cookies = driver.get_cookies()
        cookies = {}
        for cookie in driver_cookies:
            cookies[cookie['name']] = cookie['value']
        
        print(cookies)

        # show screenshot
        driver.save_screenshot('screenshot.png')

if __name__ == '__main__':
    SeleniumBrowser("https://ch4.us.to/auth/signin")