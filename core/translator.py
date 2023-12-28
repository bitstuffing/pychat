import requests
import os
import time
import urllib.parse
import subprocess
from core.browser import Browser

'''
Just used to transcribe text to audio
'''
class Translator:

    PLAYER = "mpg123"

    def __init__(self):
        self.lang = 'es'
        self.url = 'https://translate.google.com/translate_tts?client=tw-ob&ie=UTF-8&idx=0&total=1&textlen={}&tl={}&q={}'
        self.headers = {'User-agent': Browser.USER_AGENT}
        #self.pwd = os.getcwd()+"/"
        self.pwd = "/tmp/"
        self.fileName = self.pwd+f"audio{str(time.time()).replace('.','')}.mp3"

    def play(self, text, play=True):
        urlText = urllib.parse.quote_plus(text)
        url = self.url.format(len(text), self.lang, urlText)
        response = requests.get(url, headers=self.headers)
        with open(self.fileName, "wb") as local_file:
            local_file.write(response.content)
        if play:
            subprocess.call([self.PLAYER, self.fileName])
            os.remove(self.fileName)
        else:
            return self.fileName
