from core.browser import Browser
import requests
import string
import random
import time
import queue
import json

class Gpt4free(Browser):

    KEY = 'sk-7IAYvtiat58wTdD155QtWob01oCRe44yGLUOPFe1BxEShnOY' # never changes, probably in the future...

    def __init__(self):

        self.session = requests.Session()
        self.main_url = 'https://chat.gpt4free.io/'
        self.main_domain = 'gptgod.site'
        self.url = 'https://gptgod.site/api/v1/chat/completions'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/event-stream',
            'Accept-Language': 'es-ES,es',
            'sec-ch-ua-platform': 'Linux',
            'sec-fetch-site': 'cross-site',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua' : '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'authority': self.main_domain,
            'authorization': f'Bearer {self.KEY}',
            'origin': self.main_url
        }

        self.headers['Cache-Control'] = 'no-cache'
        
        self.message = []

    def prompt(self, cmd="who are you?", stream=True, queue=queue.Queue()):
        data = self.buildData(cmd)
        stringResponse = self.launchQuery(data,stream,queue=queue)
        return stringResponse
    
    def buildData(self, query):
        self.message.append({"role":"user","content":query})
        return {"messages":self.message,"model":"gpt-3.5-turbo","temperature":1,"presence_penalty":0,"top_p":1,"frequency_penalty":0,"stream":True}
    
    def launchQuery(self, data, stream=True, queue=queue.Queue()):
        response = requests.post(self.url, headers=self.headers, json=data, stream=stream)
        if stream:
            stringResponse = ''
            if(response.status_code == 200):
                # read stream
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if 'data: {' in line:
                            resp = line.split('data: {')[1].split('"}]}')[0]
                            resp = '{'+resp # fill cut json
                            if resp[-1] != '}':
                                resp += '"}]}'
                            resp = json.loads(resp) # check if it's a valid json
                            delta = resp["choices"][0]["delta"]
                            if "content" in delta:
                                #print(delta["content"])
                                queue.put(delta["content"])
                                stringResponse += delta["content"]
                        
                #print(stringResponse)
        else:
            data = (response.text)
            values = data.split('data: {')[1:]
            values = [value.split('}]}')[0] for value in values]
            stringResponse = ''.join(values)

        return stringResponse