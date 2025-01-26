from core.browser import Browser
import requests
import urllib.parse
import random

class Hix(Browser):

    def __init__(self):
        self.session = requests.Session()
        self.main_url = 'https://chat.hix.ai'
        auth_url = 'https://chat.hix.ai/api/auth/session'
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
        resp = self.session.get(auth_url, headers=self.headers)
        resp.raise_for_status()
        print("Hix cookies: ", resp.cookies)

    
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
        hex_chars = '0123456789abcdef'
        self.deviceId = ''.join(random.choice(hex_chars) for _ in range(32))
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
        deviceNumber = ''.join(random.choice(hex_chars) for _ in range(64))
        callbackUrl = urllib.parse.quote_plus('https://chat.hix.ai/chatgpt/openai-o1-mini')
        data = f'deviceId={deviceId}&redirect=false&deviceNumber={deviceNumber}&version=v1&csrfToken={csrfToken}&callbackUrl={callbackUrl}&json=true'
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