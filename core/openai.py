import requests
from core.browser import Browser
import time
import uuid
import random
import base64
import json
import hashlib



class OpenAI(Browser):

    def __init__(self):
        self.session = requests.Session()
        headers = {
            'User-Agent' : Browser.USER_AGENT,
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Connection' : 'keep-alive',
            'Host' : 'chatgpt.com',
            'Priority' : 'u=0, i',
            'Referer' : 'https://chatgpt.com',
            'Sec-Fetch-Dest' : 'document',
            'Sec-Fetch-Mode' : 'navigate',
            'Sec-Fetch-Site' : 'same-origin',
            'TE' : 'trailers',
            'Upgrade-Insecure-Requests' : '1'
        }
        resp = self.session.get('https://chatgpt.com', headers=headers)
        resp.raise_for_status()
        time.sleep(1)

        self.headers = {
            'User-Agent' : Browser.USER_AGENT,
            'OAI-Language' : 'en',
            'Referer' : 'https://chatgpt.com',
            'Connection' : 'keep-alive',
            'Sec-Fetch-Dest' : 'empty',
            'Sec-Fetch-Mode' : 'cors',
            'Sec-Fetch-Site' : 'same-origin',
            'sec-ch-ua-platform' : 'Windows',
            'sec-ch-ua' : '"Edge";v="114", " Not;A Brand";v="114", "Chromium";v="24"',
            'sec-ch-ua-mobile' : '?0',
        }

        resp = self.session.get('https://chatgpt.com/backend-anon/me', headers=self.headers)
        resp.raise_for_status()
        print(resp.json())

    '''
    return {
    accept: accept,
    "Content-Type": "application/json",
    "cache-control": "no-cache",
    Referer: "https://chatgpt.com/",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "oai-device-id": preOaiUUID || uuid,
    "User-Agent": simulated.agent,
    pragma: "no-cache",
    priority: "u=1, i",
    "sec-ch-ua": `"${simulated.ua}"`,
    "sec-ch-ua-mobile": simulated.mobile,
    "sec-ch-ua-platform": `"${simulated.platform}"`,
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    ...(spoofAddress
      ? {
          "X-Forwarded-For": ip,
          "X-Originating-IP": ip,
          "X-Remote-IP": ip,
          "X-Remote-Addr": ip,
          "X-Host": ip,
          "X-Forwarded-Host": ip,
        }
      : {}),
  };
    '''
    def get_csrf_token(self, uuid_value):
        self.token_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "Referer": "https://chatgpt.com/",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "oai-device-id": uuid_value,
            "User-Agent": Browser.USER_AGENT,
            "pragma": "no-cache",
            "priority": "u=1, i",
            "sec-ch-ua": '"Edge";v="114", " Not;A Brand";v="114", "Chromium";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors"
        }        
        resp = self.session.get('https://chatgpt.com/api/auth/csrf', headers=self.token_headers)
        resp.raise_for_status()

        data = resp.json()

        if "csrfToken" not in data:
            raise Exception("Failed to fetch required CSRF token")

        return data["csrfToken"]
    
    def generate_fake_sentinel_token(self):
        prefix = "gAAAAAC"
        config = [
            random.randint(3000, 6000),
            time.strftime("%a, %d %b %Y %H:%M:%S GMT+0100 (Central European Time)"),
            4294705152,
            0,
            Browser.USER_AGENT,
            "de",
            "de",
            401,
            "mediaSession",
            "location",
            "scrollX",
            round(random.uniform(1000, 5000), 4),
            str(uuid.uuid4()),
            "",
            12,
            int(time.time() * 1000),
        ]
        #base64 = base64.b64encode(json.dumps(config).encode()).decode()
        #return prefix + base64
        encoded_config = base64.b64encode(json.dumps(config).encode()).decode()
        return prefix + encoded_config


    def get_sentinel_token(self, uuid_value, csrf_token):

        self.token_headers["Cookie"] = f"__Host-next-auth.csrf-token={csrf_token}; oai-did={uuid_value};"

        test = self.generate_fake_sentinel_token()
        resp = self.session.post('https://chatgpt.com/backend-anon/sentinel/chat-requirements', headers=self.token_headers, json=test)
        resp.raise_for_status()
        return resp.json()
    
    def solveSentinelChallenge(self, seed: str, difficulty: str) -> str:
        cores = [8, 12, 16, 24]
        screens = [3000, 4000, 6000]

        core = random.choice(cores)
        screen = random.choice(screens)

        now = time.time() - 8 * 3600
        parse_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT+0100 (Central European Time)", time.gmtime(now))

        config = [core + screen, parse_time, 4294705152, 0, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"]
        diff_len = len(difficulty) // 2

        for i in range(100000):
            config[3] = i
            json_data = json.dumps(config)
            base = base64.b64encode(json_data.encode()).decode()
            hash_value = hashlib.sha3_512((seed + base).encode()).hexdigest()

            if hash_value[:diff_len] <= difficulty:
                result = "gAAAAAB" + base
                return result

        fallback_base = base64.b64encode(f'"{seed}"'.encode()).decode()
        return "gAAAAABwQ8Lk5FbGpA2NcR9dShT6gYjU7VxZ4D" + fallback_base


    def init_conversation(self):
        self.headers['Content-Type'] = 'application/json'
        uuid_value = str(uuid.uuid4())
        csrf_token = self.get_csrf_token(uuid_value)
        sentinel_token = self.get_sentinel_token(uuid_value, csrf_token)
        oai_sc = self.session.cookies.get("oai-sc")
        #print(sentinel_token)
        #print("OAI-SC: ", oai_sc)
        form = {
            "action": "next",
            "messages": [
                {
                    "id": str(uuid.uuid4()),
                    "author": {
                        "role": "user",
                    },
                    "content": {
                        "content_type": "text",
                        "parts": ["Hola, ¿cómo estás?"],
                    },
                    "metadata": {},
                },
            ],
            "parent_message_id": str(uuid.uuid4()),
            "model": "auto",
            "timezone_offset_min": -120,
            "suggestions": [],
            "history_and_training_disabled": False,
            "conversation_mode": {
                "kind": "primary_assistant",
                "plugin_ids": None,
            },
            "force_paragen": False,
            "force_paragen_model_slug": "",
            "force_nulligen": False,
            "force_rate_limit": False,
            "reset_rate_limits": False,
            "websocket_request_id": str(uuid.uuid4()),
            "force_use_sse": True,
        }

        headers = self.token_headers.copy()
        cookies = self.session.cookies.get_dict()
        # now append f"__Host-next-auth.csrf-token={csrf_token}; oai-did={uuid_value};" to cookies
        cookies = {**cookies, "__Host-next-auth.csrf-token": csrf_token, "oai-did": uuid_value}
        self.session.cookies.clear()
        self.session.cookies.update(cookies)
        print(self.session.cookies.get_dict())

        headers["openai-sentinel-chat-requirements-token"] = sentinel_token["token"]
        headers["openai-sentinel-proof-token"] = self.solveSentinelChallenge(sentinel_token["proofofwork"]["seed"], sentinel_token["proofofwork"]["difficulty"])

        resp = self.session.post('https://chatgpt.com/backend-anon/conversation', headers=headers, json=form)
        print(resp.text)
        resp.raise_for_status()
        print(resp.json())


    