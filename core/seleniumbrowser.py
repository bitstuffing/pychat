from undetected_chromedriver import Chrome, ChromeOptions

class SeleniumBrowser:

    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/122.0'
    driver = None
    
    def __init__(self):
        self.cookies = ""
        #self.loadDriver()

    def loadDriver(self):
        options = ChromeOptions()
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-client-side-phishing-detection")
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--disable-oopr-debug-crash-dump")
        options.add_argument("--no-crash-upload")
        options.add_argument("--disable-extensions")
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        self.driver = Chrome(use_subprocess=False, options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": self.USER_AGENT})
        print(self.driver.execute_script("return navigator.userAgent;"))
