from core.browser import Browser
import requests
import queue
import json
import asyncio
import aiohttp
import time

class Duck(Browser):

    def __init__(self):
        self.messages = []
        self.session = requests.Session()
        self.main_url = 'https://duckduckgo.com/?q=DuckDuckGo%20AI%20Chat&ia=chat&duckai=1'
        self.headers = {
            "User-Agent": Browser.USER_AGENT,
            "Accept": "text/event-stream",
            "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Referer": "https://duckduckgo.com/",
            "Content-Type": "application/json",
            "Origin": "https://duckduckgo.com",
            "Connection": "keep-alive",
            "Cookie": "dcm=8; dcs=1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Priority": "u=4",
            "TE": "trailers",
            #"x-vqd-4": f"4-2072830025737040208510812508995428{''.join(random.choices('0123456789', k=4))}",
            'Cookie' : 'dcm=8; dcs=1'
        }

        asyncio.run(self.obtain())

    async def obtain(self):
        status_headers = {
            "accept": "text/event-stream",
            "content-type": "application/json", 
            "x-vqd-accept": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0"
        }
        status_url = "https://duckduckgo.com/duckchat/v1/status"
        for attempt in range(20):
            async with aiohttp.ClientSession() as self.session:
                async with self.session.get(status_url, headers=status_headers) as response:
                    vqd = response.headers.get("x-vqd-4", "")
                    if vqd:
                        print(vqd)
                        self.headers["x-vqd-4"] = vqd
                        self.vqd = vqd
                        break
                    else:
                        time.sleep(0.2)

    def chat(self, text='who are you?', model='o3-mini', queue=queue.Queue()):
        messages = self.messages.copy()
        text.replace("'", "'\"'\"'")
        messages.append({"content": text, "role": "user"})
        payload = {
            "model": model,
            "messages": messages
        }
        retries = 20
        url = "https://duckduckgo.com/duckchat/v1/chat"
        chat_headers = {
            'User-Agent' : Browser.USER_AGENT,
            'Accept': 'text/event-stream',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            #'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Referer' : 'https://duckduckgo.com/',
            'Content-Type': 'application/json',
            'x-vqd-4': self.vqd,
            'Origin': 'https://duckduckgo.com',
            'Connection': 'keep-alive',
            'Cookie': 'dcm=8; dcs=1',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Priority': 'u=4',
            'TE': 'trailers'
        }
        for retry in range(retries):
            try:
                payload = json.dumps(payload)
                print(payload)
                with requests.post(url, data=payload, headers=chat_headers, stream=True) as response:
                    response.raise_for_status() 
                    # success, store the user message in self.messages
                    message = ""
                    for line in response.iter_lines(decode_unicode=True):
                        if 'data: ' in line and 'message' in line:
                            line = line[line.find('data: ')+len('data: '):]
                            messageJson = json.loads(line)
                            message += messageJson['message']
                            queue.put(message)
                            #print(line)
                        if "[DONE]" in line:
                            #print("breaking...")
                            break
                    # read the response headers, seaking for the x-vqd-4 header
                    vqd = response.headers.get("x-vqd-4", "")
                    if vqd:
                        self.headers["x-vqd-4"] = vqd
                        self.vqd = vqd
                    #print("new: ",vqd)
                    #close the connection
                    #print("closing connection...")
                    response.close()
                #store in the history messages
                self.messages.append({"content": text, "role": "user"})
                self.messages.append({"content": message.replace("'", "'\"'\"'"), "role": "assistant"})
                # dont try again
                break
            except Exception as ex:
                print("ex: ", ex)
                time.sleep(2)
        return queue.queue[-1]