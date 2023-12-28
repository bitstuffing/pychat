from core.browser import Browser

class OpenChat(Browser):

    main_origin = "https://openchat.team"
    main_referer = "https://openchat.team/es"

    history = {}

    def __init__(self):
        super().__init__()
        self.url = "https://openchat.team/"
        self.url_api = "https://openchat.team/api/chat"
        self.url_api_models = "https://openchat.team/api/models"
        self.headers = {
            'User-Agent': Browser.USER_AGENT,
            'Accept': '*/*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer' : self.main_referer,
            'Content-Type' : 'application/json',
            'Origin': self.main_origin,
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site' : 'same-origin',
            'TE': 'trailers'
        }

    def obtain_models(self):
        return self.session.post(self.url_api_models, json={'key': ''}, headers=Browser.headers)

    def send_message(self, message, stream=True):

        if self.history == {}:
            self.history = self.build_history()
        
        response = None
        self.history["messages"].append(self.build_message(message))
        
        if stream:
            response = self.session.post(self.url_api, json=self.history, stream=True, headers=self.headers)

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
                        print(resp, end='')
                print("")
                return stringResponse
            else:
                print(f"Error obtaining information: {response.status_code}")
        else:
            response = self.session.post(self.url_api, json=self.history, headers=self.headers)
            return response.text


    def build_history(self):
        return {
            "model": {
                "id": "openchat_v3.2_mistral",
                "name": "OpenChat Aura",
                "maxLength": 24576,
                "tokenLimit": 8192
            },
            "messages": [ ],
            "key": "",
            "prompt": "",
            "temperature": 0.5
        }

    def build_message(self, message = "hi"):
        return {
            "role": "user",
            "content": message
        }
    
