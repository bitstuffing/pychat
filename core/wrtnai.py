from core.browser import Browser
import requests
import aiohttp
from aiohttp import ClientSession
import asyncio
import random
import string
import time
import queue
import json

class WRTNAI(Browser):

    def __init__(self, builder=True):
        self.session = requests.Session()
        self.main_url = 'https://wrtn.ai' 
        self.ws_url = 'wss://william.wow.wrtn.ai/socket.io/?EIO=4&transport=websocket'
        self.headers = {
            'User-Agent': Browser.USER_AGENT,
            'Accept': '*/*',
            'Accept-Language': 'es-es,es',
            'Referer': self.main_url,
            'Origin': self.main_url,
            'Connection': 'keep-alive'
        }
        if builder:
            self.builder()

        # get models
        # curl 'https://william.wow.wrtn.ai/models?platform=web' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Site: cross-site' -H 'Priority: u=0, i' -H 'TE: trailers'
        models_url = 'https://william.wow.wrtn.ai/models?platform=web'
        headers_models = {
            'User-Agent': Browser.USER_AGENT,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Priority': 'u=0, i',
            'TE': 'trailers'
        }
        response = self.session.get(models_url, headers=headers_models)
        jsonResponse = response.json()
        self.models = jsonResponse['data']
        for model in self.models:
            print(model['name'] + " - " + model['_id'])
        
    def builder(self):

        response = self.session.get(self.main_url, headers=self.headers)

        cookies = response.headers.get('set-cookie')
        cookie = cookies[:cookies.find(';')] #AWSALB=...
        
        self.cookie = cookie

    def create_conversation(self, selectedModel=0):
        self.selectedModel = selectedModel
        # curl 'https://william.wow.wrtn.ai/guest-chat' -X POST -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0' -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br, zstd' -H 'Referer: https://wrtn.ai/' -H 'Content-Type: application/json' -H 'Platform: web' -H 'x-wrtn-id: W2.2.4e4c9dfd.0bea.463a.ae5d.e384fbdc64b3' -H 'wrtn-locale: en-US' -H 'Mixpanel-Distinct-Id: $device:194839caf90c0e-0c472626e607888-45390429-1fa400-194839caf91c0a' -H 'Origin: https://wrtn.ai' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-site' -H 'TE: trailers' --data-raw '{"unitId":"65d592f0b18cdb6b8aa92373","type":"model"}'
        url = 'https://william.wow.wrtn.ai/guest-chat'
        #self.xwrtnid = 'W2.2.' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=24))
        self.xwrtnid = self.cookie.split('__w_id=')[1]
        self.mixpanelid = (
            '$device:'
            + ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
            + '-'
            + ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
            + '-'
            + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            + '-'
            + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            + '-'
            + ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        )
        print(self.cookie)
        headers = {
            'User-Agent': Browser.USER_AGENT,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Referer': self.main_url,
            'Content-Type': 'application/json',
            'Platform': 'web',
            'x-wrtn-id': self.xwrtnid,
            'Mixpanel-Distinct-Id': self.mixpanelid,
            'wrtn-locale': 'en-US',
            'Origin': self.main_url,
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'TE': 'trailers'
        }
        # with no login we can only use the 0,4 models
        data = {
            'unitId': self.models[self.selectedModel]['_id'],
            'type': 'model'
        }
        response = self.session.post(url, headers=headers, json=data)
        jsonResponse = response.json()
        self.conversationId = jsonResponse['data']['_id']

    def sendMessage(self, message, queue=queue.Queue()):
        # call to send_message async function
        asyncio.run(self.send_message(message, queue))

    async def send_message(self, message, queue = queue.Queue()):
        # -H 'DNT: 1' -H 'Connection: keep-alive, Upgrade' -H 'Cookie: __w_id=W2.2.4@@@@; Mixpanel-Distinct-Id=%24device%3Axxxx; cf_clearance=ppppp-1.2.1.1-qqqqq.eeee.rrrr.kkkk' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: websocket' -H 'Sec-Fetch-Site: same-site' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade: websocket'
        self.ws_headers = {
            'User-Agent': Browser.USER_AGENT,
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Sec-WebSocket-Version': '13',
            'Origin': self.main_url,
            'Sec-WebSocket-Extensions': 'permessage-deflate',
            #'Sec-WebSocket-Key': 'Lu/++++==',
            'DNT': '1',
            'Connection': 'keep-alive, Upgrade',
            #'Cookie': self.cookie + '; Mixpanel-Distinct-Id=' + self.mixpanelid,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'websocket',
            'Sec-Fetch-Site': 'same-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade': 'websocket'
        }
        cookie = self.cookie + '; Mixpanel-Distinct-Id=' + self.mixpanelid
        async with ClientSession(headers=self.ws_headers, cookies=self.cookiesToDict(cookie), timeout=aiohttp.ClientTimeout(total=60)) as session:
            async with session.ws_connect(self.ws_url, autoping=False) as wss:
                print("starting conversation...")
                await wss.send_str("40/v1/guest-chat,{}")
                response = await wss.receive()
                print("response 0: "+response.data)
                response = await wss.receive()
                print("response 40: "+response.data)
                print("sending message...")
                # 42/v1/guest-chat,["enterChat",{"chatId":"CHAT_ID","clientHeaders":{"x-wrtn-id":"W2.2.XYZT","wrtn-locale":"ja-JP"}}]
                await wss.send_str("42/v1/guest-chat,[\"enterChat\",{\"chatId\":\""+self.conversationId+"\",\"clientHeaders\":{\"x-wrtn-id\":\""+self.xwrtnid+"\",\"wrtn-locale\":\"es-ES\"}}]")
                print("message sent 42")
                response = await wss.receive()
                print("response: "+str(response.data))
                print("sending message...")
                # 42/v1/guest-chat,["startChat",{"message":"TEXT","model":"fast_ai_search","mode":"chat","reroll":false,"commandChipType":"","isChocoChip":false,"images":[],"referenceIds":[],"assignmentId":"","adContext":{"adCreativeId":null,"packageAdCreativeId":null,"inventoryCodes":["CHAT_BRAND","CHAT_REFERENCE","CHAT_WRTN_PICK"]},"content":"hola","chatId":"CHAT_ID","email":"","platform":"web","williamRequestId":"XYZT","clientHeaders":{"x-wrtn-id":"W2.2.XXXX","wrtn-locale":"ko-KR","x-test-id":"","wrtn-test-ab-model":{"fast_ai_search":"B","fast_internal":"disabled"}}}]
                requestId = ''.join(random.choices(string.ascii_lowercase + string.digits, k=24)) 
                await wss.send_str("42/v1/guest-chat,[\"startChat\",{\"message\":\""+message+"\",\"model\":\""+self.models[self.selectedModel]['_id']+"\",\"mode\":\"chat\",\"reroll\":false,\"commandChipType\":\"\",\"isChocoChip\":false,\"images\":[],\"referenceIds\":[],\"assignmentId\":\"\",\"adContext\":{\"adCreativeId\":null,\"packageAdCreativeId\":null,\"inventoryCodes\":[\"CHAT_BRAND\",\"CHAT_REFERENCE\",\"CHAT_WRTN_PICK\"]},\"content\":\""+message+"\",\"chatId\":\""+self.conversationId+"\",\"email\":\"\",\"platform\":\"web\",\"williamRequestId\":\""+requestId+"\",\"clientHeaders\":{\"x-wrtn-id\":\""+self.xwrtnid+"\",\"wrtn-locale\":\"ko-KR\",\"x-test-id\":\"\",\"wrtn-test-ab-model\":{\"fast_ai_search\":\"B\",\"fast_internal\":\"disabled\"}}}]")
                print("message sent")
                response = await wss.receive(timeout=20)
                print("response: "+response.data)
                # startChat response in loop until we get a "2" response
                while '42/v1/guest-chat,["end",' not in response.data and '42/v1/guest-chat,["error",' not in response.data:
                    response = await wss.receive(timeout=10)
                    print("response: "+response.data)
                    chunk = response.data
                    if '42/v1/guest-chat,["data",{"chunk":"' in chunk:
                        chunk = chunk[chunk.find(':"')+2:chunk.rfind('"}]')]
                        queue.put(chunk)
                        print(chunk)
                #close connection
                await wss.close()
                

        