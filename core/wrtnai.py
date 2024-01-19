from core.browser import Browser
import requests
import aiohttp
from aiohttp import ClientSession
import random
import string
import time
import queue
import json

class WRTNAI(Browser):

    def __init__(self, builder=False):
        self.session = requests.Session()
        self.main_url = 'https://wrtn.ai' 
        self.url = 'https://api.channel.io/front/v6/users/me'
        self.ws_url = 'wss://front-ws.channel.io/socket.io/'
        self.js_url = 'https://services.wow.wrtn.ai/app/chat/remoteEntry.js'
        self.version = 'W1.2.250118664121020100101121051080192032' 
        self.headers = {
            'User-Agent': Browser.USER_AGENT,
            'Accept': '*/*',
            'Accept-Language': 'es-es,es;q=0.8,en-us;q=0.5,en;q=0.3',
            'Access-Control-Request-Method': 'PATCH',
            'Access-Control-Request-Headers': 'content-type,x-session',
            'Referer': self.main_url,
            'Origin': self.main_url,
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site'
        }
        if builder:
            self.builder()
        
    def builder(self):

        response = self.session.options(self.url, headers=self.headers)

        cookies = response.headers.get('set-cookie')
        cookie = cookies[:cookies.find(';')] #AWSALB=...
        cookie2= cookies[cookies.find('AWSALBCORS='):] 
        cookie2 = cookie2[:cookie2.find(';')]
        self.cookie = cookie + '; ' + cookie2

        # now we have to get the x-veil-id
        self.xveilid, self.xsession = self.obtain_xveilid_and_xsession()
        

    def obtain_xveilid_and_xsession(self):
        response = self.session.get(self.js_url, headers=self.headers)
        self.pluginId = response.text[response.text.find('REACT_APP_CHANNEL_ID_PLUGIN_KEY:"')+len('REACT_APP_CHANNEL_ID_PLUGIN_KEY:"'):]
        self.pluginId = self.pluginId[:self.pluginId.find('"')]
        self.bootUrl = f'https://api.channel.io/front/v6/elastic/plugins/{self.pluginId}/boot'
        response = self.session.post(self.bootUrl, headers=self.headers, data={"url":"https://wrtn.ai/"})
        xveilid = response.json()['veilId']
        xsession = response.json()['sessionJWT']
        return xveilid, xsession
    

    def prompt(self, cmd="who are you?", queue=queue.Queue(), stream=True):
        # generates a random new identifier
        x_wrt_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=21))
        self.xwrtnid = f"{self.version}.{x_wrt_id}.{int(time.time() * 1000)}"
        
        # creates an assistant
        url1 = 'https://william.wow.wrtn.ai/chat/anonymous/start?platform=web&mode=chat&model=gpt4'
        headers = {
            'User-Agent': Browser.USER_AGENT,
            'Accept': 'application/json',
            'Accept-Language': 'es-es,es;q=0.8,en-us;q=0.5,en;q=0.3',
            'Platform': 'web',
            'Origin': self.main_url,
            'Connection': 'keep-alive',
            'Referer': self.main_url,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'TE': 'trailers',
            'x-wrtn-id': self.xwrtnid,
        }
        self.session.options(url1, headers=headers)
        response = self.session.post(url1, headers=headers, data={"message" : cmd})
        assistant_id = response.json()['data']

        url2 = f'https://william.wow.wrtn.ai/chat/anonymous/{assistant_id}?model=gpt4&platform=web&user=nobody@wrtn.io'
        if stream:
            response = self.session.get(url2, headers=headers, stream=True)
            if response.status_code == 200:
                stringResponse = ""
                for line in response.iter_content(Browser.STEAM_BUFFER_SIZE):
                    if line:
                        try:
                            resp = (line.decode('utf-8'))
                        except UnicodeDecodeError:
                            for encoding in ['ISO-8859-1', 'latin1', 'cp1252', 'cp437', 'big5', 'gb2312', 'euc-kr', 'windows-1252']:
                                try:
                                    resp = (line.decode(encoding))
                                    break
                                except UnicodeDecodeError:
                                    continue
                            
                            else:
                                raise UnicodeDecodeError("Not possible to decode it :'(")
                        stringResponse += resp
                        # refresh stringResponse with the data not processed
                        stringResponse = self.processQueue(queue, stringResponse)
            else:
                print(f"Error obtaining information: {response.status_code}")
            # serialize queue (Queue) and assing it to stringResponse without consuming queue
            stringResponse = ""
            for item in queue.queue:
                stringResponse += item
            
            print(stringResponse)
        else:
            self.session.get(url2, headers=headers)
            url3 = f'https://william.wow.wrtn.ai/chat/anonymous/{assistant_id}/result'
            response = self.session.get(url3, headers=headers)
            print(response.json()["data"]["content"])

    def processQueue(self, queue, stringResponse):
        import re
        # stringResponse is a stream, find all strings between '":"' and "}, and remove all chars after "} from stringResponse, next put all texts found in the queue
        matches = re.findall(r'":"(.*?)"}', stringResponse)
        for match in matches:
            if match != "[DONE]":
                queue.put(match)
                #print(match, end='')
        #print("")
        return stringResponse[stringResponse.rfind('"}')+2:]
        