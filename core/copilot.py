from core.browser import Browser
import requests
import queue
import aiohttp
import asyncio
from aiohttp import ClientSession

'''
Similar model to Bing, but it's the current published model to the people.
'''
class Copilot(Browser):

    def __init__(self):
        self.url = "https://copilot.microsoft.com/"
        self.session = requests.Session()
        self.cookies = ''

        self.headers = {
            'User-Agent': Browser.USER_AGENT, 
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1'
        }
        self.ws_headers = {
            'User-Agent': Browser.USER_AGENT,
            'Accept': '*/*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Sec-WebSocket-Version': '13',
            'Sec-GPC':'1',
            'Origin': 'https://copilot.microsoft.com',
            'Host': 'copilot.microsoft.com',
            'Sec-WebSocket-Extensions': 'permessage-deflate',
            'Connection': 'keep-alive, Upgrade',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'websocket',
            'Sec-Fetch-Site': 'same-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade': 'websocket',
            'Set-WebSocket-Key' : 'XGfeihRVyxaMctc1hR8hww=='
        }

        resp1 = self.session.get(self.url, headers=self.headers)
        resp1.raise_for_status()

        self.headers['Referer'] = self.url
        self.headers['DNT'] = '1'
        self.headers['Sec-GPC'] = '1'
        self.headers['TE'] = 'trailers'

        resp2 = self.session.post('https://copilot.microsoft.com/c/api/start', headers=self.headers, json={"timeZone":"Europe/Madrid","teenSupportEnabled":True})
        resp2.raise_for_status()

    def create_conversation(self):
        resp3 = self.session.post('https://copilot.microsoft.com/c/api/conversations', headers=self.headers)
        print(resp3.text)
        self.conversationId = resp3.json()['id']


        
    def init_conversation(self, message="hello", queue = queue.Queue()):
        cookies = self.extractFirefoxCookies(domain="copilot.microsoft.com")
        print(cookies)
        self.cookies = cookies
        self.ws_url = "wss://copilot.microsoft.com/c/api/chat"
        self.ws_headers['Cookie'] = cookies
        asyncio.run(self.run_init_conversation(message, cookies, queue))
    

    async def run_init_conversation(self, prompt="hello world!", cookies = '', queue = queue.Queue()):
        #print("init_conversation: cookies: "+cookies)
        if cookies != '':
            self.headers['Cookie'] = cookies

        if "conversationId" not in self.__dict__:
            self.create_conversation()
        
        async with ClientSession(headers=self.ws_headers, timeout=aiohttp.ClientTimeout(total=60)) as session:
            async with session.ws_connect(self.ws_url, autoping=False, params={'api-version': '2'}) as wss:
                print("starting conversation...")
                await wss.send_str('{"event":"setOptions","supportedCards":["image","video"],"ads":null}')
                # escape special characters data = f'{"event":"send","conversationId":"{self.conversationId}","content":[{"type":"text","text":"hi world!"}],"mode":"chat"}'
                data = {
                    "event": "send",
                    "conversationId": self.conversationId,
                    "content": [{"type": "text", "text": prompt}],
                    "mode": "chat"#"reasoning" # DEV. NOTE: this doesn't work if your cookie is not a Microsoft Logged account, if you want to use 'new' reasoning model
                }
                await wss.send_json(data)
                response = await wss.receive(timeout=10)
                print("response: "+response.data)
                response2 = await wss.receive(timeout=10)
                print("response2: "+response2.data)
                if "CaptchaChallenge" in response2.data:
                    return response2
                else:
                    print(response2.data)
                # get all responses until disconnected (TODO handler out of this function)
                print('processing conversation...')
                while True:
                    try:
                        response = await wss.receive(timeout=3)
                        print("resp... ", response.data)
                    except Exception as e:
                        break
                    if response.type == aiohttp.WSMsgType.CLOSED:
                        print("CLOSED!")
                        break
                    elif response.type == aiohttp.WSMsgType.ERROR:
                        print("ERROR!")
                        break
                    
                await wss.close()
                await session.close()