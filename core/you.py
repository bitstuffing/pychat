import base64
import time
import uuid
import requests
from core.browser import Browser
import string
import random
import datetime
import queue
import urllib
import json


# Activa el debug globalmente para todas las solicitudes
#requests.urllib3.disable_warnings() # Inhibit InsecureRequestWarning
#requests.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL' # Adjusting the settings to improve the workers
import logging

# Configurar el nivel de log para ver debug de urllib3
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

class You(Browser):

    def __init__(self, message='hello!'):
        
        self.session = requests.Session()
        #self.session.cert = "/home/bit/file.ca"
        self.session.verify = False
        
        #verify = "/home/bit/file.ca"
        self.url = f"https://you.com/search?q={message}&fromSearchBar=true&tbm=youchat"
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Dnt': '1',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Sec-Gpc': '1',
            'Te': 'trailers',
        }

        proxy = {
            'http': 'http://127.0.0.1:8080'
        }
        
        self.conversation = []

        response = self.session.get('https://you.com/',headers=self.headers, proxies=proxy)
        print(response.cookies)

        for cookie in response.cookies:
            print(cookie.name, cookie.value)

        newCookies = response.cookies.get_dict()
        newCookies['youpro_subscription'] = 'false'
        newCookies['youchat_smart_learn'] = 'true'
        newCookies['youchat_personalization'] = 'true'
        newCookies['you_subscription'] = 'free'
        #newCookies['uuid_guest'] = str(uuid.uuid4())
        #newCookies['uuid_guest_backup'] = newCookies['uuid_guest']
        newCookies['total_query_count'] = "0"
        newCookies['safesearch_guest'] = 'Moderate'
        newCookies['daily_query_count'] = "0"
        newCookies['daily_query_date'] = datetime.datetime.now().strftime("%a %b %d %Y")
        newCookies['ai_model'] = 'gpt_4o'
        defaultUUID = str(uuid.uuid4())
        key = 'ab.storage.deviceId.'+defaultUUID
        key2 = 'ab.storage.sessionId.'+defaultUUID

        #g%3A4821c822-0124-bc23-aac4-5f2b99d90b84%7Ce%3Aundefined%7Cc%3A1720534394566%7Cl%3A1720598297294
        newCookies[key] = 'g%3A'+str(uuid.uuid4())+'%7Ce%3Aundefined%7Cc%3A1720534394566%7Cl%3A1720598297294'
        #g%3Ab3e5e4cc-9e7f-0d55-43bd-067f71d00da9%7Ce%3A1720600139045%7Cc%3A1720598297294%7Cl%3A1720598339045
        newCookies[key2] = 'g%3A'+str(uuid.uuid4())+'%7Ce%3A1720600139045%7Cc%3A1720598297294%7Cl%3A1720598339045'
        
        self.headers2 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Host' : 'you.com',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer' : "https://you.com/",
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Sec-GPC' : '1',
            'Upgrade-Insecure-Requests': '1'
        }
        print(newCookies)

        response2 = self.session.get('https://you.com/api/get_nullstate_suggestions?chat_mode=default',headers=self.headers2, cookies=newCookies)
        print(response2.cookies)

    def login(self, newRegister=False):
        
        # login / register part
        register = 'https://web.stytch.com/sdk/v1/passwords'
        auth = 'https://web.stytch.com/sdk/v1/passwords/authenticate'

        randomUUID = str(uuid.uuid4()) 

        stringEncoded = base64.b64encode('public-token-live-507a52ad-7e69-496b-aee0-1c9863c7c819:public-token-live-507a52ad-7e69-496b-aee0-1c9863c7c819'.encode('ascii'))
        currentTime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        eventData = '{"event_id":"event-id-'+randomUUID+'","app_session_id":"app-session-id-'+randomUUID+'","persistent_id":"persistent-id-'+randomUUID+'","client_sent_at":"'+currentTime+'","timezone":"Europe/Madrid","app":{"identifier":"you.com"},"sdk":{"identifier":"Stytch.js Javascript SDK","version":"3.3.0"}}'
        encodedEventData = base64.b64encode(eventData.encode('ascii'))
        url = auth
        if newRegister:
            url = register
            #generate a random email with random domain
            self.email = ''.join(random.choice(string.ascii_lowercase) for i in range(12))
            self.email += '@'
            self.email += ''.join(random.choice(string.ascii_lowercase) for i in range(7))
            self.email += '.com'
            #generate a random password with 18 alphanumeric characters with lowercase and uppercase mixed and some special characters
            self.password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(18))

        data = {"email":self.email,"password":self.password,"session_duration_minutes":129600}
        self.headers['Authorization'] = f'Basic {stringEncoded.decode("ascii")}'
        self.headers['Content-Type'] = 'application/json'
        self.headers['X-SDK-Client'] = encodedEventData.decode('ascii')
        response = self.session.get('https://you.com',headers=self.headers)
        #print(response.cookies)
        for cookie in response.cookies:
            #print(cookie.name, cookie.value)
            if cookie.name == '__cf_bm':
                self.cfbm = cookie.value
                break

        time.sleep(3)
        #print(self.headers)
        response = self.session.post(url=url, headers=self.headers, json=data)
        #print(response.text)
        jsonResponse=response.json()
        self.sessionToken = jsonResponse['data']['session_token']
        self.jwt = jsonResponse['data']['session_jwt']

    def send_message(self,message = "aclarame, por favor, ¿eres chatgpt3 o chatgpt4?", stream=True, queue=queue.Queue()):
        # search part

        uuidGuest = uuid.uuid4()
        cookie = ""
        cookies = {
            'uuid_guest': uuidGuest,
            'uuid_guest_backup': uuidGuest,
            'safesearch_guest': 'Moderate',
            '__cf_bm' : self.cfbm,
            'chat_mode': 'gpt-4',
            'youchat_personalization': 'true',
            'youchat_smart_learn': 'true',
            'youpro_subscription': 'false',
            'you_subscription': 'freemium',
            'stytch_session': self.sessionToken,
            'stytch_session_jwt': self.jwt,
            'ydc_stytch_session': self.sessionToken,
            'ydc_stytch_session_jwt': self.jwt,
            'region':'es-ES' 
        }
        for key, value in cookies.items():
            cookie += f'{key}={value}; '


        self.headers['Cookie']=cookie

        chatId = uuid.uuid4()
        filters = 'WebPages,Translations,TimeZone,Computation,RelatedSearches'
        safeSearch = 'Moderate'
        traceId = chatId
        turnId = uuid.uuid4() 
        chatModel = 'gpt-4' #'default'
        responseLanguage = 'es-ES'
        # crearte chat var with url encoded conversation
        chat = ""
        if len(self.conversation) == 0:
            chat = urllib.parse.urlencode(self.conversation)
        else:
            chat = urllib.parse.quote(str(self.conversation))
            print(chat)
        
        ws_url = f'https://you.com/api/streamingSearch?q={message}%3F&page=1&showNoAppsInYouChat=true&count=10&safeSearch={safeSearch}&mkt={responseLanguage}&responseFilter={filters}&domain=youchat&use_personalization_extraction=true&queryTraceId={traceId}&chatId={chatId}&conversationTurnId={turnId}&pastChatLength=0&selectedChatMode={chatModel}&chat={chat}'
        extractedText = ""
        if stream:
            response = self.session.get(ws_url, headers=self.headers, stream=True)
            event = ""
            for line in response.iter_lines():
                line = line.decode('unicode_escape')
                line = str(line)
                if line:
                    #print(line, end='\n')
                    # make a switch case to handle the different types of lines, if line startsWith "event: " then it's a new event, if line startsWith "data: " 
                    if line.startswith('data: '):
                        if event == 'youChatToken':
                            # extract youChatToken content from b'data: {"youChatToken": "targetDataToBeExtracted"}' response
                            #print("original line: ",line)
                            extractedData = line[line.find(': "')+len(': "'):]
                            extractedData = extractedData[:extractedData.rfind('"}')]
                            queue.put(str(extractedData))
                            extractedText+=str(extractedData)                         
                            #print("extracted value: ",extractedData, end='\n')
                        #elif event == 'youChatModeLimits': # limits information
                        #    print(line)
                        #else: # more metadata answer information 
                        #    print("unhandled line: ",line, event)
                    elif line.startswith('event: '):
                        # extract new event from "b'event: youChatToken'" response
                        event = line[line.find('event: ')+7:]
                    
        else:
            response = self.session.get(ws_url, headers=self.headers)
            data = response.text
            # extract information line by line
            for line in data.splitlines():
                if line.startswith('data: '):
                    if event == 'youChatToken':
                        extractedData = line[line.find(': "')+len(': "'):]
                        extractedData = extractedData[:extractedData.rfind('"}')]
                        extractedText+=extractedData                         
                        
                elif line.startswith('event: '):
                    # extract new event from "b'event: youChatToken'" response
                    event = line[line.find('event: ')+7:]
        
        nodePetition = {"question":message}
        nodeResponse = {"answer":extractedText}

        self.conversation.append(nodePetition)
        self.conversation.append(nodeResponse)

        return extractedText
            
