from core.seleniumbrowser import SeleniumBrowser
from core.helpers.tempemail import TempEmail
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# experimental selenium browser client for ch4.us.to (same domain/database than ch4t.us)
class Ch4usto(SeleniumBrowser):

    def __init__(self):
        super().__init__()
        self.loginUrl = "https://ch4.us.to/auth/signin"
        self.registerUrl = "https://ch4.us.to/auth/signup"
        self.password = "Passwd.11" 

    def register(self):
        tempEmail = TempEmail()
        self.email = tempEmail.getEmail()
        self.loadDriver()

        self.driver.get(self.registerUrl) 

        try:
            email_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label=\"Email\"]"))
            )
            # set email
            email_text.send_keys(self.email)
            # now search for "Send Verification Code" button
            button_send = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[type=\"button\"]"))
            )
            # click it
            button_send.click()

            # now read emails and get the verification code
            verification_code = ""
            while verification_code == "":
                emails = tempEmail.getEmails()
                for email in emails:                    
                    if "verification code: " in email["bodyPreview"]:
                        # extract from ' Here is your CH4 verification code: 966540 Do not share this information with anyone. The verificat' the code 966540
                        verification_code = email["bodyPreview"].split("code: ")[1].split(" ")[0]


            username = self.email.split("@")[0]
            username_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label=\"Username\"]"))
            )
            # set username
            username_text.send_keys(username)
            # Password
            pass_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label=\"Password\"]"))
            )
            # set password
            pass_text.send_keys(self.password)

            # Verification Code
            code_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label=\"Verification Code\"]"))
            )
            # set verification code
            code_text.send_keys(verification_code)

            # find submit button and click it
            button_submit = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[type=\"button\"]"))
            )
            button_submit.click()

        except:
            screenshot = self.driver.get_screenshot_as_png()
            with open('screenshot.png', 'wb') as f:
                f.write(screenshot)
            self.driver.quit()
            print("element not found :'(")



    def login(self):
        self.loadDriver()

        print("logging in...")

        # open the main page
        self.driver.get(self.loginUrl) 

        print("finding page elements...")
        try:
            # wait for the page to load target elements one by one
            username_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label=\"Email / Username\"]"))
            )
            #change username
            username_text.send_keys(self.email)
            pass_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label=\"Password\"]"))
            )
            # change password
            pass_text.send_keys(self.password)

            # confirm that we have filled the fields
            print(username_text.get_attribute('value'))
            print(pass_text.get_attribute('value'))

            # find submit button and click it
            button_submit = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[type=\"button\"]"))
            )
            button_submit.click()
            time.sleep(4)

            # javascript should redirect us to the main page, so we wait for it to load    

        except:
            screenshot = self.driver.get_screenshot_as_png()
            with open('screenshot.png', 'wb') as f:
                f.write(screenshot)
            self.driver.quit()
            print("element not found :'(")
                
        # get the sign in cookies
        driver_cookies = self.driver.get_cookies()
        cookies = {}
        for cookie in driver_cookies:
            cookies[cookie['name']] = cookie['value']
            self.cookies += cookie['name'] + "=" + cookie['value'] + "; "
        
        print(cookies)

        # show screenshot
        self.driver.save_screenshot('screenshot.png')
    
        self.driver.quit()

        return cookies # self.cookies
    
    def send_message(self, cmd="hello, who are you?"):
        self.loadDriver()

        # TODO (here is the magic)

        self.driver.close()