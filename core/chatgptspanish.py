from core.browser import Browser
import requests

class ChatGPTSpanish(Browser):
    def __init__(self):
        self.reload()

    def reload(self):
        self.main_url = 'https://chatgptspanish.org/gpt-4/'
        self.headers = {
            'User-Agent': Browser.USER_AGENT,
            'Accept': '*/*',
            'Accept-Language': 'es-ES,es;q=0.8',
            'Origin': 'https://chatgptspanish.org',
            'Alt-Used': 'chatgptspanish.org',
            'Connection': 'keep-alive',
            'Referer': 'https://chatgptspanish.org/gpt-4/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }

        self.session = requests.Session()

        response = self.session.get(self.main_url, headers=self.headers)
        resp = response.text
        self.nonce = resp.split('data-nonce="')[1].split('"')[0]
        self.post_id = resp.split('data-post-id="')[1].split('"')[0]
        self.bot_id = resp.split('data-bot-id="')[1].split('"')[0]

    def send_message(self, message):
        # is this a joke, right? who are they? wordpress developers? have they ever heard about minimal security?
        # when I see this, I think where we are going as a society, they probably have asked to chatgpt to make this
        url = 'https://chatgptspanish.org/wp-admin/admin-ajax.php' 
        data = {
            '_wpnonce': self.nonce,
            'post_id': self.post_id,
            'url': 'https://chatgptspanish.org/gpt-4',
            'action': 'wpaicg_chat_shortcode_message',
            'message': message,
            'bot_id': self.bot_id
        }

        response = requests.post(url, headers=self.headers, data=data)
        import json
        json_response = json.loads(response.text)
        return json_response['data']