from core.browser import Browser
import requests
import string
import random
import time
import queue

class Gpt4free(Browser):

    def __init__(self):

        self.session = requests.Session()
        self.main_url = 'https://gpt4free.io'
        self.url = 'https://gpt4free.io/chat/'

        self.headers = {
            'User-Agent': Browser.USER_AGENT,
            'Accept': 'text/event-stream',
            'Accept-Language': 'es-ES,es;q=0.8;q=0.3',
            'Referer': self.url,
            'Origin': self.main_url
        }

        response = self.session.get(self.url)

        cookie = response.text.split('sessionId&#34;:&#34;N\/A&#34;,&#34;restNonce&#34;:&#34;')[1].split('&#34;,&#34;')[0]

        self.headers['Connection'] = 'keep-alive'
        self.headers['Sec-Fetch-Dest'] = 'empty'
        self.headers['Sec-Fetch-Mode'] = 'no-cors'
        self.headers['Sec-Fetch-Site'] = 'same-origin'
        self.headers['Content-Type'] = 'application/json'
        self.headers['X-WP-Nonce'] = cookie
        self.headers['Pragma'] = 'no-cache'
        self.headers['Cache-Control'] = 'no-cache'
        
        self.reset()

    def prompt(self, cmd="who are you?", stream=True, queue=queue.Queue()):
        timestamp = int(round(time.time() * 1000)) 
        data = self.buildData(self.randomId, cmd)
        stringResponse = self.launchQuery(data,stream,queue=queue)
        self.messages.append(self.buildMessage(self.randomId, "user", cmd, timestamp))
        timestamp = int(round(time.time() * 1000))
        self.messages.append(self.buildMessage(self.randomId, "assistant",stringResponse, timestamp))
        return stringResponse

    def reset(self):
        self.messages = []
        self.randomId = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) 
        timestamp = int(round(time.time() * 1000)) 
        self.messages.append(self.buildMessage(self.randomId, "assistant","How can I help you today?", timestamp))

    def buildMessage(self, randomId, role, content, timestamp):
        who = "User: " if role == 'user' else "AI: "
        return {
            "id": randomId, 
            "role": role, 
            "content": content, 
            "who": who, 
            "timestamp": timestamp
        }
    
    def buildData(self, randomId, query):
        return {
            "botId": "default",
            "customId": None,
            "session": "N/A",
            "chatId": randomId,
            "contextId": (''.join(random.choice(string.digits) for _ in range(10) )),
            "messages": self.messages,
            "newMessage": query,
            "newImageId": None,
            "stream": True
        }
    
    def launchQuery(self, data, stream=True, queue=queue.Queue()):
        url = 'https://gpt4free.io/wp-json/mwai-ui/v1/chats/submit'
        response = requests.post(url, headers=self.headers, json=data, stream=stream)
        if stream:
            stringResponse = ''
            if(response.status_code == 200):
                # read stream
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if 'data: {"type":"live","data":"' in line:
                            resp = line.split('data: {"type":"live","data":"')[1].split('"}')[0]
                            queue.put(resp)
                            stringResponse += resp
                        
                #print(stringResponse)
        else:
            data = (response.text)
            values = data.split('data: {"type":"live","data":"')[1:]
            values = [value.split('"}')[0] for value in values]
            stringResponse = ''.join(values)

        return stringResponse