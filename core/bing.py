from core.browser import Browser
import json
import uuid
import os
import re
import asyncio
import aiohttp
import string
import random
import requests
import urllib
import urllib.parse
from aiohttp import ClientSession
import datetime
from dateutil.tz import tzutc
import threading
import queue
import speech_recognition as sr
import traceback
from core.helpers.binghelper import BingResponse, BingMessageType, BingMessageType1, BingMessageType2, BingTextResponse

class AudioRecorder(threading.Thread):
    def __init__(self, sample_rate=22500):
        threading.Thread.__init__(self)
        self.queue = queue.Queue()
        self.exit = False
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone(sample_rate=sample_rate)

    def getQueue(self):
        return self.queue

    def getExit(self):
        return self.exit
    
    def setExit(self, exit):
        self.exit = exit

    def run(self):
        with self.mic as source:
            while not self.exit:
                audio = self.recognizer.record(source, duration=1)
                self.queue.put(audio.frame_data)

class Bing(Browser):
    VERSION = "1.1381.12"

    conversationId = ''
    clientId = ''
    conversationSignature = ''

    WS_BING_HEADERS = {
        "Pragma": "no-cache",
        "Origin": "https://www.bing.com",
        "Accept-Language": 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        "User-Agent": Browser.USER_AGENT,
        "Cache-Control": "no-cache",
        "Connection": "Upgrade",
    }
    
    DELIMITER = "\x1e"

    def __init__(self):
        super().__init__()
        self.url = "https://www.bing.com/search"
        self.form_url = 'https://www.bing.com/search?q=Bing+AI&showconv=1&FORM=hpcodx'
        self.turning_url = 'https://www.bing.com/turing/api/suggestions/v1/zeroinputstarter?lang=es&region=*&tone=Balanced&enablePersonalizedSuggestions=undefined&enableMarketplaceSuggestions=undefined'
        self.voice_service_url = 'wss://sr.bing.com/opaluqu/speech/recognition/dictation/cognitiveservices/v1'
        self.ws_url = 'wss://sydney.bing.com/sydney/ChatHub'
        self.invocation_id = 0
        self.headers = {
            'User-Agent': Browser.USER_AGENT, 
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
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
            'Origin': 'https://www.bing.com',
            'Host': 'sydney.bing.com',
            'Sec-WebSocket-Extensions': 'permessage-deflate',
            'Connection': 'keep-alive, Upgrade',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'websocket',
            'Sec-Fetch-Site': 'same-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade': 'websocket',
        }
        '''
        try:
            self.getCID()
        except Exception as e:
            print(e)
            print("Error getting IG and CID from bing.com, trying normal way...")
            self.session.get(self.url, headers=self.headers)
            pass
        '''
        # set MUID, _EDGE_S, _EDGE_V, SRCHD, SRCHUID, SRCHUSR, SRCHHPGUSR, _SS, _HPVN cookies
        response = self.session.get("https://www.bing.com/", headers=self.headers)
        for cookie in response.cookies:
            #print(cookie.name+"="+cookie.value)
            self.session.cookies.set(cookie.name, cookie.value)

        # set MUIDB cookie
        response = self.session.get("https://www.bing.com/geolocation/write?isDevLoc=false", headers=self.headers)
        for cookie in response.cookies:
            #print(cookie.name+"="+cookie.value)
            self.session.cookies.set(cookie.name, cookie.value)
        

    def getCID(self):
        response1 = self.session.get(self.form_url, headers=self.headers)

        html = response1.text
        self.ig = re.search(r'IG:"(.*?)"', html).group(1)
        print(f"IG: {self.ig}")

        self.cid = re.search(r'CID:"(.*?)"', html).group(1)
        print(f"cid: {self.cid}")

    def init_conversation(self, cmd="hello", queue = queue.Queue()):
        asyncio.run(self.init_conversation_async2(cmd, queue))

    async def init_conversation_async2(self, prompt, queue = queue.Queue()):
        try:
            prompt = prompt.encode('ascii', 'ignore').decode('ascii')
        except:
            pass
        cookies = ""
        cookies = self.extractFirefoxCookies()
        if True:
            #cookies = self.launch_captcha_solver()
            for cookie in cookies.split("; "):
                if "=" in cookie:
                    cookie = cookie.split("=")
                    #print("updating cookie: "+cookie[0]+"="+cookie[1])
                    self.session.cookies.set(cookie[0], cookie[1])

        for cookie in self.session.cookies:
            cookies += cookie.name+"="+cookie.value+"; "
        #print("PRE cookies: "+cookies)
        coroutine = self.run_init_conversation(prompt, cookies=cookies, queue=queue)
        #response = asyncio.run(coroutine)
        response = await coroutine
        if "CaptchaChallenge" in response.data:
            cookies = self.launch_captcha_solver()
            # updates self.session cookies using normal string cookies, parsing it and creating a cookie object for each one
            
            for cookie in cookies.split("; "):
                if "=" in cookie:
                    cookie = cookie.split("=")
                    #print("updating cookie: "+cookie[0]+"="+cookie[1])
                    self.session.cookies.set(cookie[0], cookie[1])

        self.run_init_conversation(prompt, cookies, queue)


    def launch_captcha_solver(self):
        # set valid cct cookie
        url = "https://www.bing.com/turing/captcha/challenge?q=&iframeid=local-gen-"+str(uuid.uuid4())
        cookie = self.extractCookiesFromRealFirefox(url)
        return cookie
    
    def cookiesToDict(self, cookies: str) -> dict:
        cookies = {
            key_value.strip().split("=")[0]: "=".join(key_value.split("=")[1:])
            for key_value in cookies.split(";")
        }
        cookies2 = {}
        for key in cookies:
            if cookies[key] == '':
                #del cookies[key]
                pass
            else:
                cookies2[key] = cookies[key].strip()
        return cookies2

    async def init_conversation_async(self):
        response = self.session.get(f"https://www.bing.com/turing/conversation/create?bundleVersion={Bing.VERSION}", headers=self.headers)
        data = response.json()
        conversationId = data.get('conversationId')
        clientId = data.get('clientId')
        conversationSignature = response.headers.get('X-Sydney-Encryptedconversationsignature')
        conversationSignature2 = response.headers.get('X-Sydney-Conversationsignature')
        #print(f"CONVERSATION-ID: {conversationId}")
        return conversationId, clientId , conversationSignature, conversationSignature2

    async def run_init_conversation(self, prompt="hello world!", cookies = '', queue = queue.Queue()):
        #print("init_conversation: cookies: "+cookies)
        if cookies != '':
            self.headers['Cookie'] = cookies
        if self.conversationId == '' or self.clientId == '' or self.conversationSignature == '' or self.conversationSignature2 == '':
                
            #tasks = [asyncio.create_task(self.init_conversation_async())]
            #await asyncio.gather(*tasks)
            #self.conversationId, self.clientId, self.conversationSignature, self.conversationSignature2 = tasks[0].result()
            self.conversationId, self.clientId, self.conversationSignature, self.conversationSignature2 = await self.init_conversation_async()

        async with ClientSession(headers=self.ws_headers, cookies=self.cookiesToDict(cookies), timeout=aiohttp.ClientTimeout(total=60)) as session:
            async with session.ws_connect(self.ws_url, autoping=False, params={'sec_access_token': self.conversationSignature}) as wss:
                #print("starting conversation...")
                await wss.send_str(self.format_message({'protocol': 'json', 'version': 1}))
                response = await wss.receive(timeout=10)
                #print("response: "+response.data)
                await wss.send_str(self.create_message(self.conversationId, self.clientId, self.conversationSignature, self.conversationSignature2, prompt))
                self.invocation_id += 1
                response2 = await wss.receive(timeout=10)
                #print("response2: "+response2.data)
                if "CaptchaChallenge" in response2.data:
                    return response2
                #else:
                #    print(response2.data)
                #print("done!")
                # get all responses until disconnected (TODO handler out of this function)
                while True:
                    response = await wss.receive(timeout=10)
                    if response.type == aiohttp.WSMsgType.CLOSED:
                        print("CLOSED!")
                        break
                    elif response.type == aiohttp.WSMsgType.ERROR:
                        print("ERROR!")
                        break
                    else:
                        json_response = response.data
                        if json_response != "":
                            
                            try:
                                #print(len(json_response))
                                #print(json_response)
                                if json_response[-1] == Bing.DELIMITER:
                                    json_response = json_response[:-1] # remove the 'custom' end delimiter
                                if "}\x1e" in json_response:
                                    discarted = json_response[json_response.find("}\x1e{")+2:]
                                    json_response = json_response[:json_response.find("}\x1e{")+1]
                                    discarted_json = json.loads(discarted)
                                    discartedType = BingMessageType(discarted_json.get('type'),discarted_json.get('invocationId'))

                                    print(f"Discarted: type: {discartedType.type}, invocationId: {discartedType.invocationId}")

                                data = json.loads(json_response)

                                # ChatData object
                                bingResponse = BingResponse(data)
                                # if bingResponse.chatmessage exists, it's a chat message
                                if hasattr(bingResponse, 'chatmessage'):
                                    if isinstance(bingResponse.chatmessage ,BingMessageType1):
                                        print(f"BingMessageType1, author: {bingResponse.chatmessage.arguments.messages[0].author}, message: {bingResponse.chatmessage.arguments.messages[0].text}")
                                    elif isinstance(bingResponse.chatmessage ,BingMessageType2):
                                        print(f"BingMessageType2, author: {bingResponse.chatmessage.item.messages[0].author}, message: {bingResponse.chatmessage.item.messages[0].text}")
                                    queue.put(bingResponse)
                                else:
                                    print("not a chat message:")
                                    print(json_response)

                            except Exception as e:
                                traceback_str = traceback.format_exc()
                                print(f"Error: {e}")
                                print(traceback_str)
                                print(f"json_response.encode('utf-8'): {json_response.encode('utf-8')}")
                                pass
                                
    
    def create_message(self, conversationId: str, clientId: str, conversationSignature: str, conversationSignature2: str, prompt: str):
        request_id = str(uuid.uuid4())
        struct = {
            "arguments": [
                {
                    "source": "cib",
                    "optionsSets": [
                        "nlu_direct_response_filter",
                        "deepleo",
                        "disable_emoji_spoken_text",
                        "responsible_ai_policy_235",
                        "enablemm",
                        "dv3sugg",
                        "iyxapbing",
                        "iycapbing",
                        "galileo",
                        "saharagenconv5"
                    ],
                    "allowedMessageTypes": [
                        "ActionRequest",
                        "Chat",
                        "ConfirmationCard",
                        "Context",
                        "InternalSearchQuery",
                        "InternalSearchResult",
                        "Disengaged",
                        "InternalLoaderMessage",
                        "InvokeAction",
                        "Progress",
                        "RenderCardRequest",
                        "RenderContentRequest",
                        "AdsQuery",
                        "SemanticSerp",
                        "GenerateContentQuery",
                        "SearchQuery"
                    ],
                    "sliceIds": [],
                    "verbosity": "verbose",
                    "scenario": "SERP",
                    "spokenTextMode": "None",
                    "traceId": ''.join(random.choice(string.hexdigits.upper()) for _ in range(32)),
                    "conversationHistoryOptionsSets": [
                        "autosave",
                        "savemem",
                        "uprofupd",
                        "uprofgen"
                    ],
                    "isStartOfSession": self.invocation_id == 0,
                    'requestId': request_id,
                    "message": {
                        #"userIpAddress": self.getInternetIpAddress(),
                        "timestamp": self.getTimeStamp(),
                        "author": "user",
                        "inputMethod": "Keyboard",
                        "text": prompt,
                        "messageType": "SearchQuery",
                        "requestId": request_id,
                        "messageId": request_id
                    },
                    "tone": "Precise", # Creative, Precise, Balanced
                    "spokenTextMode": "None",
                    "conversationSignature": conversationSignature2,
                    "conversationId": conversationId,
                    "participant": {
                        "id": clientId
                    }
                }
            ],
            "invocationId": str(self.invocation_id),
            "target": "chat",
            "type": 4
        }
        return self.format_message(struct)

    def format_message(self, msg: dict) -> str:
        return json.dumps(msg, ensure_ascii=False) + Bing.DELIMITER
    
    def build_speech_message(self, path, request_id = str(uuid.uuid4()),content = {}):
        timestamp = datetime.datetime.now(tz=tzutc()).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        content_type="application/json"

        message = f"Path: {path}\r\n"
        message += f"X-RequestId: {request_id}\r\n"
        message += f"X-Timestamp: {timestamp}\r\n"
        if content_type == "application/json":
            message += f"Content-Type: {content_type}\r\n\r\n"
            message += json.dumps(content, ensure_ascii=True)
        else:
            if content_type == "audio/x-wav":
                message += f"Content-Type: {content_type}\r\n\r\n"
            message += content
        #print(message)
        return message

    def speech_to_text(self):
        asyncio.run(self.speech_to_text_async())

    def build_audio_message_header(self, request_id = str(uuid.uuid4())):
        timestamp = datetime.datetime.now(tz=tzutc()).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

        content_type="audio/x-wav"
        message = bytes.fromhex('007e506174683a20617564696f') + b'\r\n' # ~Path: audio\n
        message += b'X-RequestId: '+request_id.encode('utf-8')+ b'\r\n' # X-RequestId: 534885F5FF347068C0CD34C5A66F6EFE\n
        message += b'X-Timestamp: '+timestamp.encode('utf-8')+ b'\r\n'
        message += b'Content-Type: '+content_type.encode('utf-8')+ b'\r\n\r\n'
        message += bytes.fromhex('524946460000000057415645666d74201000000001000100803e0000007d0000020010006461746100000000') # RIFF...WAVEfmt .............data....
        return message
    
    def build_audio_message_intro(self, request_id = str(uuid.uuid4())):
        timestamp = datetime.datetime.now(tz=tzutc()).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        message = bytes.fromhex('0063506174683a20617564696f') + b'\r\n' # Path: audio\n
        message += bytes.fromhex('582d5265717565737449643a20') + request_id.encode('utf-8') + b'\r\n' 
        message += bytes.fromhex('582d54696d657374616d703a20') + timestamp.encode('utf-8') + b'\r\n\r\n' 
        
        return message
    
    def build_audio_message_content(self, request_id = str(uuid.uuid4()), content = b''):
        timestamp = datetime.datetime.now(tz=tzutc()).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        print(f'timestamp: {timestamp}')
        message = bytes.fromhex('0063506174683a20617564696f') + b'\r\n' 
        message += bytes.fromhex('582d5265717565737449643a20') + request_id.encode('utf-8') + b'\r\n' 
        message += bytes.fromhex('582d54696d657374616d703a20') + timestamp.encode('utf-8') + b'\r\n\r\n' 
        message += content
        return message

    async def speech_to_text_async(self):
        
        '''
        if( self.cid == '' or self.ig == ''):
            self.session = requests.Session()
            self.getCID()
        '''

        response = self.session.get(url = self.turning_url, headers=self.headers)

        cookies = ""
        for cookie in response.cookies:
            cookies += cookie.name+"="+cookie.value+"; "

        for cookie in self.session.cookies:
            cookies += cookie.name+"="+cookie.value+"; "

        if cookies != '':
            self.headers['Cookie'] = cookies

        print("extracted cookies: "+cookies)

        request_id = str(uuid.uuid4())
        print(f'request_id: {request_id}')

        connection_key = ''.join(random.choice(string.hexdigits.upper()) for _ in range(32)) 
        print(f'connection_key: {connection_key}')
        #connection_key = str(uuid.uuid4())
        paramsDic = {
            'clientbuild': 'sydney',
            'referer': urllib.parse.quote_plus(self.form_url),
            'uqurequestid': request_id,
            'surface': 'desktop',
            'autodetect': 1,
            'uquclientversion': 0,
            'sroptions' : 'cdxrwss,cdxsydoroff,cdxwhisr,cdxwsnnc,lidprimary,cdxdlid,autotts',
            'language': 'xx-yy',
            'format': 'simple',
            'Ocp-Apim-Subscription-Key': 'key',
            'X-ConnectionId': connection_key
        }

        async with ClientSession(headers=self.headers, timeout=aiohttp.ClientTimeout(total=60)) as session:
            async with session.ws_connect(url = self.voice_service_url, autoping=False, params=paramsDic) as wss:
                request_id = ''.join(random.choice(string.hexdigits.upper()) for _ in range(32)) 
                message = {"context":{"system":{"name":"SpeechSDK","version":"1.15.0-alpha.0.1","build":"JavaScript","lang":"JavaScript"},"os":{"platform":"Browser/Linux x86_64","name":Browser.USER_AGENT,"version":"5.0 (X11)"},"audio":{"source":{"bitspersample":16,"channelcount":1,"connectivity":"Unknown","manufacturer":"Speech SDK","model":"HD Webcam C910","samplerate":16000,"type":"Microphones"}}},"recognition":"conversation"}
                content1 = self.build_speech_message(path='speech.config', request_id=request_id, content=message)
                #print(content1)
                await wss.send_str(content1)
                print("speech.config sent")
                await wss.send_str(self.build_speech_message(path='speech.context', request_id=request_id, content={}))
                print("speech.context sent")

                response = await wss.receive(timeout=10)
                if response.data != '':
                    print(response.data)

                response = await wss.receive(timeout=10)
                if response.data != '':
                    print(response.data)

                response = await wss.receive(timeout=10)
                if response.data != '':
                    print(response.data)
                    if "speech.startDetected" in response.data:
                        print("ok, lets go!")

                await wss.send_bytes(self.build_audio_message_header(request_id=request_id))

                await wss.send_bytes(self.build_audio_message_intro(request_id=request_id))

                print("audio header sent, reading response...")

                import time
                #sleep 100 ms
                time.sleep(0.101)
                
                
                chunk_size = 6400
                call = 0
                recorder = AudioRecorder()
                recorder.start()
                import time
                time.sleep(1)
                while not recorder.getExit():
                    if not recorder.getQueue().empty():
                        audio_data = recorder.getQueue().get()
                        # 6400 bytes per chunk
                        num_chunks = len(audio_data) // chunk_size
                        for i in range(num_chunks):
                            start_index = i * chunk_size
                            end_index = start_index + chunk_size
                            chunk_audio_data = audio_data[start_index:end_index]

                            if len(chunk_audio_data) == chunk_size:
                                await wss.send_bytes(self.build_audio_message_content(request_id=request_id, content=chunk_audio_data))
                                call += 1

                        if call % 12 == 0:
                            print('show partial text content')
                            response = await wss.receive(timeout=10)
                            if response.type == aiohttp.WSMsgType.CLOSED:
                                print("CLOSED!")
                            elif response.type == aiohttp.WSMsgType.ERROR:
                                print("ERROR!")
                            else:
                                json_response = response.data
                                if json_response != "":
                                    print(json_response)
                                    try:
                                        resp = json.loads(json_response[json_response.find("\r\n\r\n")+4:])
                                        text, offset, duration, recognitionStatus, displayText, primaryLanguage = None, None, None, None, None, None
                                        if hasattr(resp, 'Text'):
                                            text = resp.get('Text')
                                        if hasattr(resp, 'Offset'):
                                            offset = resp.get('Offset')
                                        if hasattr(resp, 'Duration'):
                                            duration = resp.get('Duration')
                                        if hasattr(resp, 'RecognitionStatus'):
                                            recognitionStatus = resp.get('RecognitionStatus')
                                        if hasattr(resp, 'DisplayText'):
                                            displayText = resp.get('DisplayText')
                                        if hasattr(resp, 'PrimaryLanguage'):
                                            primaryLanguage = resp.get('PrimaryLanguage')

                                        bingResponse = BingTextResponse(text = text, offset = offset, duration = duration, recognitionStatus = recognitionStatus, displayText = displayText, primaryLanguage = primaryLanguage)
                                        if '{"RecognitionStatus":"Success",' in json_response:
                                        # TODO review why this line is not working, it should be but... probably tomorrow will be a better day to check it
                                        #if recognitionStatus is not None and (recognitionStatus == "Success" or recognitionStatus == "EndOfDictation"):
                                            recorder.setExit(True)
                                    except Exception as e:
                                        traceback_str = traceback.format_exc()
                                        print(f"Error: {e}")
                                        print(traceback_str)
                                        print(f"json_response.encode('utf-8'): {json_response.encode('utf-8')}")
                                        pass

                

                #print("sent content, receiving LAST response...")

                
                response = await wss.receive(timeout=10)
                if response.type == aiohttp.WSMsgType.CLOSED:
                    print("CLOSED!")
                elif response.type == aiohttp.WSMsgType.ERROR:
                    print("ERROR!")
                else:
                    json_response = response.data
                    if json_response != "":
                        print(json_response) # {"Instrumentation": {}}

