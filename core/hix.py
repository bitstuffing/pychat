import uuid
import time
import json
import os
from core.browser import Browser
import requests
import urllib.parse
#import hashlib

class Hix(Browser):

    def __init__(self):
        self.session = requests.Session()
        self.main_url = 'https://chat.hix.ai'
        self.auth_url = 'https://chat.hix.ai/api/auth/session'
        self.headers = {
            'User-Agent': Browser.USER_AGENT,
            'Accept': '*/*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Referer': self.main_url,
            'Content-Type': 'application/json',
            'baggage': 'undefined',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua': '"Edge";v="114", "Chromium";v="114", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'Priority': 'u=4',
            'TE': 'trailers'
        }
        resp = self.session.get(self.auth_url, headers=self.headers)
        resp.raise_for_status()

        # curl 'https://chat.hix.ai/sign-in' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3' -H 'Accept-Encoding: gzip, deflate, br, zstd' -H 'Alt-Used: chat.hix.ai' -H 'Connection: keep-alive' -H 'Referer: https://chat.hix.ai/chatgpt/openai-o1-mini' -H 'Cookie: user_group=125; first-visit-url=https%3A%2F%2Fchat.hix.ai%2Fchatgpt%2Fopenai-o1-mini; __Host-next-auth.csrf-token=a14222ceed8a1b2c2cc4c8bc5db1f58752d7c8babb77e11cf6ccb78fd09a6282%7Cef77c1dae97227a220b6bed5025495b410b8594e17ea2078a00cd6070fb09b1b; __Secure-next-auth.callback-url=https%3A%2F%2Fchat.hix.ai; device-id=c0e05003773a2627ff6ac881e67924cb' -H 'Upgrade-Insecure-Requests: 1' -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Site: same-origin' -H 'Sec-Fetch-User: ?1' -H 'Priority: u=0, i' -H 'TE: trailers'

        url = 'https://chat.hix.ai/sign-in'
        headers = {
            'User-Agent': Browser.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            #'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            'Referer': 'https://chat.hix.ai/chatgpt/openai-o1-mini',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Priority': 'u=0, i',
            'TE': 'trailers'
        }

    
    def send_message(self, message):
        

        url = 'https://chat.hix.ai/api/auth/providers'
        headers = {
            'User-Agent': Browser.USER_AGENT,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Referer': 'https://chat.hix.ai/chatgpt/openai-o1-mini',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua': '"Edge";v="114", "Chromium";v="114", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0'
        }
        response = self.session.get(url, headers=headers)
        print(response.json())


        from urllib.parse import quote
        random_bytes = os.urandom(16)
        device_id = ''.join(f'{b:02x}' for b in random_bytes)
        distinct_id = device_id  # UUID v4
        timestamp = int(time.time() * 1000)
        session_id = str(uuid.uuid4())  # UUID for session value

        data = {
            "distinct_id": distinct_id,
            "$sesid": [timestamp, session_id, timestamp]
        }

        json_str = json.dumps(data, separators=(",", ":"))
        encoded_value = quote(json_str)

        # build token
        project_token = "phc_9LvbXawaTFdrUSVPTOjwbVv7bZWE1iOQDhF8U7dPa0E"
        cookieKey = f"ph_{project_token}_posthog"
        cookieValue = f"{encoded_value}"

        cookie = f"{cookieKey}={cookieValue}" 

        print("generated cookie: ", cookie)

        self.session.cookies[cookieKey] = cookieValue

        resp = self.session.get(self.auth_url, headers=self.headers)
        resp.raise_for_status()
        print(resp.json())
        


        url = 'https://chat.hix.ai/api/auth/csrf'
        headers = {
            'User-Agent': Browser.USER_AGENT,
            'Accept': '*/*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': 'https://chat.hix.ai/chatgpt/openai-o1-mini',
            'Content-Type': 'application/json',
            'baggage': 'undefined',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua': '"Edge";v="114", "Chromium";v="114", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'Priority': 'u=4',
            'TE': 'trailers'
        }
        self.deviceId = device_id
        # append deviceId to cookies
        self.cookies = self.session.cookies
        self.cookies['deviceId'] = self.deviceId
        self.session.cookies = self.cookies

        response = self.session.get(url, headers=headers)
        csrfToken = response.json()["csrfToken"]
        print(csrfToken)


        url = 'https://chat.hix.ai/api/auth/signin/anonymous-user'
        headers = {
            'User-Agent': Browser.USER_AGENT,
            'Accept': '*/*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': 'https://chat.hix.ai/chatgpt/openai-o1-mini',
            'Content-Type': 'application/x-www-form-urlencoded',
            'baggage': 'undefined',
            'Origin': 'https://chat.hix.ai',
            'Connection': 'keep-alive'
        }
        deviceId = self.deviceId
        print("deviceId: "+deviceId)

    
        #sha256_hash = hashlib.sha256(deviceId.encode()).hexdigest()
        deviceNumber = '' # TODO
        callbackUrl = urllib.parse.quote_plus('https://chat.hix.ai/chatgpt/openai-o1-mini')
        data = f'deviceId={device_id}&redirect=false&deviceNumber={deviceNumber}&version=v1&csrfToken={csrfToken}&callbackUrl={callbackUrl}&json=true'
        response = self.session.post(url, data=data, headers=headers)
        print("-->"+response.text)
        print(response.cookies)
        url = 'https://chat.hix.ai/api/auth/signin?csrf=true'
        response = self.session.post(url, data=data, headers=headers)
        print("**>"+response.text)
        print(response.cookies)

        url = 'https://chat.hix.ai/api/trpc/hixChat.getUsedBotList,subUsage.getSubUsage,grammar.getCopyScapeUsage?batch=1&input='
        data = '{"0":{"json":{"limit":1000}},"1":{"json":{"appName":"HIXChat"}},"2":{"json":null,"meta":{"values":["undefined"]}}}'

        headers = {
            'User-Agent': Browser.USER_AGENT,
            'Accept': '*/*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Referer': self.main_url,
            'Content-Type': 'application/json',
            'baggage': 'undefined',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua': '"Edge";v="114", "Chromium";v="114", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'Priority': 'u=4',
            'TE': 'trailers'
        }
        data = urllib.parse.quote_plus(data)
        response = self.session.get(url+data, headers=self.headers)
        print(response.json())

        url = 'https://chat.hix.ai/api/trpc/hixChat.createChat?batch=1'
        data = '{"0":{"json":{"title":"'+message+'","botId":1182}}}'
        response = self.session.post(url, data=data, headers=self.headers)
        print(response.json())