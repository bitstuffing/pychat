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

class You(Browser):

    def __init__(self, query='hello!'):
        
        self.url = f"https://you.com/search?q={query}&fromSearchBar=true&tbm=youchat"
        self.session = requests.Session()
        self.headers = {
            'User-Agent': Browser.USER_AGENT,
            'Accept': 'text/event-stream',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            #'Accept-Encoding': 'gzip, deflate, br',
            'Referer' : "https://you.com",
            'Origin' : "https://you.com",
            'X-SDK-Parent-Host': 'https://you.com',
        }

        self.email = "invalidemail@gmail.com"
        self.password="invalidPasswordJ#d€7€"

        self.cfbm = ""
        self.sessionToken = ""
        self.jwt = ""

        self.conversation = []

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

    def send_message(self,query = "aclarame, por favor, ¿eres chatgpt3 o chatgpt4?", stream=True, q=queue.Queue()):
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
        
        ws_url = f'https://you.com/api/streamingSearch?q={query}%3F&page=1&count=10&safeSearch={safeSearch}&mkt={responseLanguage}&responseFilter={filters}&domain=youchat&use_personalization_extraction=true&queryTraceId={traceId}&chatId={chatId}&conversationTurnId={turnId}&pastChatLength=0&selectedChatMode={chatModel}&chat={chat}'
        extractedText = ""
        if stream:
            response = self.session.get(ws_url, headers=self.headers, stream=True)
            event = ""
            for line in response.iter_lines():
                line = line.decode('utf-8')
                if line:
                    #print(line, end='\n')
                    # make a switch case to handle the different types of lines, if line startsWith "event: " then it's a new event, if line startsWith "data: " 
                    if line.startswith('data: '):
                        if event == 'youChatToken':
                            # extract youChatToken content from b'data: {"youChatToken": "targetDataToBeExtracted"}' response
                            #print("original line: ",line)
                            extractedData = line[line.find(': "')+len(': "'):]
                            extractedData = extractedData[:extractedData.rfind('"}')]
                            q.put(extractedData)
                            extractedText+=extractedData                         
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
        
        nodePetition = {"question":query}
        nodeResponse = {"answer":extractedText}

        self.conversation.append(nodePetition)
        self.conversation.append(nodeResponse)

        return extractedText
            
