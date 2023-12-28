import websocket
import speech_recognition as sr
import json

from core.browser import Browser

class Watson(Browser):

    def __init__(self):
        super().__init__()

        self.session, API_KEY = self.get_api_key()
        LANGUAGE_MODEL = 'es-ES' # could be en-US 
        self.url = f'wss://api.us-south.speech-to-text.watson.cloud.ibm.com/v1/recognize?access_token={API_KEY}&model={LANGUAGE_MODEL}_NarrowbandModel'

        self.headers = {
            'User-Agent': Browser.USER_AGENT,
            'Accept': 'audio/wav',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Sec-WebSocket-Version': '13',
            'Origin': 'https://www.ibm.com',
            'Connection': 'keep-alive, Upgrade',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'websocket',
            'Sec-Fetch-Site': 'same-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade': 'websocket'
        }

    def get_api_key(self):
        
        response = self.session.get('https://www.ibm.com/demos/live/speech-to-text/self-service/home')
        #print(response.headers)
        headers = {
            'User-Agent': Browser.USER_AGENT,
            'Accept': 'application/json',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': 'https://www.ibm.com/demos/live/speech-to-text/self-service/home',
            'Content-Type': 'application/json',
            'Origin': 'https://www.ibm.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers',
            'Pragma': 'no-cache'
        }
        response2 = self.session.get('https://www.ibm.com/demos/live/speech-to-text/api/stt/token', headers=headers)
        #print(response2.text)
        return self.session, json.loads(response2.text)['token']
    
    def on_open(self, ws):
        print("open connection...")
        
        self.send_initial(ws)

        self.send_audio(ws)

    def send_initial(self, ws):
        ws.send(json.dumps({
            "action": "start",
            "content-type": "audio/l16;rate=44100",
            "accept": "audio%2Fwav%3Brate%3D44100", # audio/wav;rate=44100, readthedocs of IBM
            "interim_results": True,
            "word_alternatives_threshold": 0.01,
            "smart_formatting": True,
            "speaker_labels": True,
            "inactivity_timeout": -1,
            "timestamps": True
        }))
        print("Sent start message.")

    def send_audio(self, ws):
        r = sr.Recognizer()
        self.sending_audio = True
        try:
            with sr.Microphone(sample_rate=44100) as source:
                print('Speek now...')
                
                audio = r.listen(source, phrase_time_limit=5)
                audio_data = audio.get_raw_data()
                ws.send(audio_data, opcode=websocket.ABNF.OPCODE_BINARY)
                print(f"Chunk sent: {len(audio_data)} bytes")
            
            self.sending_audio = False
            ws.send(json.dumps({"action": "stop"}))
        except Exception as e:
            print("Error sending audio: " + str(e))
            self.sending_audio = False
            ws.send(json.dumps({"action": "stop"}))

    def on_message(self, ws, message):
        print("Received message:")
        message = json.loads(message)
        if("state" in message and message["state"] == "listening"):
            print("listening...")
            print(message)
            if not self.sending_audio:
                self.send_initial(ws)
                self.send_audio(ws)
                print("Sent audio message.")
            else:
                print("Not sending audio because it's already sending audio")
        elif "results" in message:
            # get transcript
            print(message)
            transcript = message["results"][0]["alternatives"][0]["transcript"]
            print("message received: " + transcript)

    # handle close event
    def on_close(self, ws, close_status_code, close_msg):
        print("connection closed!")
        print(close_status_code, close_msg)

    def on_data(self, ws, data, is_binary, frame):
        #print("Datos recibidos:")
        #print(data)
        pass

    def speech_to_text(self):

        ws = websocket.WebSocketApp(
            self.url,
            header=self.headers,
            on_open=self.on_open,
            on_message=self.on_message,
            on_data=self.on_data,
            on_close=self.on_close
        )
        #websocket.enableTrace(True)
        # start the app
        ws.run_forever()