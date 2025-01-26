from core.seleniumbrowser import SeleniumBrowser
from core.helpers.tempemail import TempEmail
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# experimental selenium browser client cch137.link
class Ch4usto(SeleniumBrowser):

    DOMAIN = "cch137.link"

    def __init__(self):
        super().__init__()
        self.mainUrl = f"https://{self.DOMAIN}/"
        self.loginUrl = f"https://{self.DOMAIN}/auth/signin"
        self.registerUrl = f"https://{self.DOMAIN}/auth/signup"
        self.chatUrl = f"https://{self.DOMAIN}/apps/ai-chat/"
        self.email = ""
        self.password = "Passwd.11" 
        self.xtoken = "" 
        self.cookie = None

    def register(self):
        tempEmail = TempEmail()
        self.email = tempEmail.getEmail()
        if self.driver is None:
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
                    if "verification code:\n\n" in email["body_text"]:
                        # extract from ' Here is your CH4 verification code: 966540 Do not share this information with anyone. The verificat' the code 966540
                        verification_code = email["body_text"].split("code:\n\n")[1].split("\n\n")[0]
                        print("verification code is: " + verification_code)
                        break


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
            print("pass_text")
            # set password
            pass_text.send_keys(self.password)

            # Verification Code
            code_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label=\"Verification Code\"]"))
            )
            print("code_text")
            # set verification code
            code_text.send_keys(verification_code)

            # find submit button and click it
            button_submit = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[type=\"button\"]"))
            )
            print("button_submit")
            button_submit.click()
            #self.driver.save_screenshot('submit_register.png')

            time.sleep(5)
            #self.driver.save_screenshot('submit_wait.png')
            # search cookie, in the new version registered users are logged in automatically
            self.cookie = self.driver.get_cookie('x-token')
            print(str(self.cookie))
            self.xtoken = self.cookie["value"]
            #self.driver.save_screenshot('ok_register.png')
            print("self.xtoken: " + self.xtoken)

        except:
            screenshot = self.driver.get_screenshot_as_png()
            with open('screenshot_fail.png', 'wb') as f:
                f.write(screenshot)
            self.driver.quit()
            self.driver = None
            print("element not found :'(")

    def login(self):
        if self.driver is None:
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
            

            # javascript should redirect us to the main page, so we wait for it to load    

        except:
            screenshot = self.driver.get_screenshot_as_png()
            with open('screenshot_fail.png', 'wb') as f:
                f.write(screenshot)
            self.driver.quit()
            print("element not found :'(")
        
        self.cookie = None # first time clean old cookies
        # get the sign in cookies
        while self.cookie == None or self.xtoken == "":
            print("try...")
            try:
                self.cookie = self.driver.get_cookie('x-token')
                print(str(cookie))
                #self.driver.save_screenshot('ok_login.png')
            except:
                print("cookie not found")
                self.driver.save_screenshot('fail_login.png')
                time.sleep(1)
                pass
        
        print("continue...")

        self.xtoken = ""
        while self.xtoken == "":
            driver_cookies = self.driver.get_cookies()
            cookies = {}
            for cookie in driver_cookies:
                cookies[cookie['name']] = cookie['value']
                self.cookies += cookie['name'] + "=" + cookie['value'] + "; "
                if cookie['name'] == "x-token":
                    self.xtoken = cookie['value']
                    self.cookie = cookie
            time.sleep(1)
        
        print(cookies)

        # show screenshot
        #self.driver.save_screenshot('screenshot.png')
    
        #self.driver.quit()

        return cookies # self.cookies
    
    def send_message(self, cmd="hello, who are you?", conversationUrl = ""):
        if conversationUrl == "":
            conversationUrl = self.chatUrl
        #self.loadDriver()
        #cookie = self.driver.get_cookie('x-token')
        #print(str(self.cookie))
        # TODO (here is the magic)
        if self.cookie == None:
            if self.email == "":
                self.register()
            self.login()
        else:
            print("elseeee")
            if self.driver is None:
                self.loadDriver()
                # now updates self.driver with the cookies
                #self.driver.get("https://"+self.DOMAIN+"/")
                print("else222")
            self.driver.delete_all_cookies()
            time.sleep(1)
            #self.driver.add_cookie(self.cookie)
            #self.driver.get(self.chatUrl)
            #if self.cookie == None:
            self.cookie = {'domain': self.DOMAIN, 'httpOnly': True, 'name': 'x-token', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': str(self.xtoken)}
            cookie2 = {'domain': "."+self.DOMAIN, 'httpOnly': True, 'name': 'x-token', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': str(self.xtoken)}
            print(str(cookie2))
            self.driver.add_cookie(self.cookie)
            print("one is added")
            self.driver.add_cookie(cookie2)

        print("opening chat...")
        print(str(self.driver.get_cookies()))
        self.driver.get(self.chatUrl)
        time.sleep(1)

        # print all the page (debug)
        #self.driver.save_screenshot('screenshot.png')
        #print("screenshot saved")

        # search for $("button[id^='react-aria']") and click it
        button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[id^='react-aria']"))
        )

        button.click()
        model = ""
        while "GPT-4" not in model:
            time.sleep(0.5)
            # now click on li element with value="gpt-4"
            li_model = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[value='gpt-4']"))
            )
            li_model[len(li_model)-1].click()

            # take 0.5 second to load the model
            time.sleep(0.5)
            print("searching for model...")

            # ensure that the button value is "gpt-4", so we have to seek for a children node "span" with "data-slot" attribute = "value" and tag content "gpt-4"
            span_model = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-slot='value']"))
            )
            model = span_model.text
            print("model is: " + model)
        if("GPT-4" in model):
            print("using model selected, span text is: " + model) 
            try:
                # search for the textarea with data-slot="input"
                textarea = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[data-slot='input']"))
                )
                # set the message
                textarea.send_keys(cmd)
                # now simulate the enter key in textarea to send the message
                textarea.send_keys(u'\ue007')

                # wait for the response, read the p element inside the last div with class "aichat-message"
                response = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.aichat-message p"))
                )

                # there is a response, so there is a conversatsion, now capture the button with css
                button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[id^='aichat-conv-']")) #cc_aLbej
                )

                # get the id attribute value to continue conversation
                self.conversationId = button.get_attribute('id').split("aichat-conv-")[1]
                

                # check size of response and print it
                print(len(response))

                # the javascript will write the response in the p element, so we need to refresh the element to get the text each second
                last_response = ""
                next_try = 0
                while next_try < 10:
                    try:
                        current_response = response[len(response)-1].text
                        time.sleep(0.5)
                        print("temp response is: " + current_response)
                        if last_response == current_response and last_response != "": 
                            print("same response, next try...")
                            next_try += 1
                        elif len(current_response)>0:
                            print("updating response...")
                            last_response = current_response
                        else:
                            print("empty response, waiting...")
                    except:
                        time.sleep(0.5)
                        print("exception, waiting...")
                        if last_response != "":
                            next_try += 1
                        pass
                    
                print("response is: " + last_response)
                #self.driver.save_screenshot('screenshot2.png')
            except Exception as ex:
                #self.driver.save_screenshot('exception.png')
                print("exception: " + str(ex))

        else:
            print("target model not selected")


        self.driver.close()
        self.driver = None # flag to reload the driver