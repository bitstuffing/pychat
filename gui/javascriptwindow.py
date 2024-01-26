from core.openchat import OpenChat
from core.bing import Bing
from core.you import You
from core.chatgptspanish import ChatGPTSpanish
from core.gpt4free import Gpt4free
from core.helpers.binghelper import BingResponse, BingMessageType1, BingMessageType2
from core.watson import Watson
from core.wrtnai import WRTNAI
import uuid
from PySide6.QtCore import QObject, QThread, QRunnable
from PySide6.QtWidgets import QMainWindow
from PySide6 import QtCore
from PySide6.QtCore import QUrl
import time
import queue
import base64
import threading


class VoiceWorker(QRunnable, QObject):
    update_signal = QtCore.Signal(str)
    enable_signal = QtCore.Signal()
    thread = None

    def __init__(self, father, provider):
        QObject.__init__(self)
        QRunnable.__init__(self)
        
        self.provider = provider
        self.father = father

    def run(self):
        print("VoiceWorker started.")
        qe = queue.Queue()
        self.update_signal.emit("Listening...")

        self.thread = threading.Thread(target=self.provider.speech_to_text, args=(qe,))
        self.thread.start()

        recognizedText = ""

        #self.provider.speech_to_text(queue=qe)
        time.sleep(1)
        counter = 0
        while counter < 30:
            try:
                time.sleep(0.1)
                message = qe.get_nowait()
                recognizedText = ""

                if message.text != "":
                    counter = 0
                    recognizedText = message.text
                elif message.displayText != "":
                    recognizedText = message.displayText
                elif message.recognitionStatus == "EndOfDictation" or message.recognitionStatus == "Success":
                    #counter += 1
                    counter = 30
                    break
                time.sleep(0.1)
                # trim recognized text
                
                if recognizedText != None and recognizedText != "":
                    self.update_signal.emit(recognizedText)
            except Exception as e:
                counter += 1
                print("Exception: ",e)
                message = ""

        #self.update_signal.emit("Finished")
        self.enable_signal.emit()
        # kill worker
        self.deleteLater()
        self.father._voiceThread.quit()
        print("VoiceWorker finished.")

class ChatWorker(QRunnable, QObject):

    _thread = None
    provider = None
    queue = None
    message = None
    identifier = None
    update_signal = QtCore.Signal(str,str)
    enable_signal = QtCore.Signal()


    def __init__(self, father, view, provider, message, identifier):
        QObject.__init__(self)
        QRunnable.__init__(self)
        
        self.provider = provider
        self.view = view
        self.message = message
        self.identifier = identifier
        self.father = father

    def send_message_in_background(self):
        # if self.provider has send_message
        if hasattr(self.provider, 'send_message'):
            self.provider.send_message(message=self.message, stream=True, queue=self.queue)
        elif hasattr(self.provider, 'init_conversation'):
            self.provider.init_conversation(message=self.message, queue=self.queue)
        elif hasattr(self.provider, 'prompt'):
            self.provider.prompt(cmd=self.message, stream=True, queue=self.queue)

    def run(self):
        print("Worker started.")
        self.queue = queue.Queue()
        # send_message in background thread
        thread = threading.Thread(target=self.send_message_in_background)
        thread.start()

        #self.provider.send_message(message=self.message,stream=True,queue=self.queue)
        print("worker sent message, receiving...")

        message = ""
        counter = 0 # retry counter for empty queue
        limit = 50 # TODO configure limit in settings for each provider

        while not self.queue.empty() or self.queue.qsize() > 0 or counter < limit:
            print("waiting for message...")
            counter += 1
            time.sleep(0.1) # TODO configure refresh in settings for each provider
            try:
                new_message = self.queue.get_nowait()
                if new_message != "":
                    counter = 0
                    # if new_message is string
                    if isinstance(new_message, str):
                        message += new_message
                    #elif is instance of BingResponse
                    elif isinstance(new_message, BingResponse) and isinstance(new_message.chatmessage, BingMessageType1):
                        message = new_message.chatmessage.arguments.messages[0].text
                    
                    # encode message to base64
                    if isinstance(message, str):
                        print(f"message: {message}")
                        sample_string_bytes = message.encode("utf-8")
                    else:
                        sample_string_bytes = message 
                    base64_bytes = base64.b64encode(sample_string_bytes) 
                    base64_string = base64_bytes.decode("utf-8")
                    print(f"base64_string: {base64_string}")
                    # talk with main thread
                    #self.view.page().runJavaScript("updateChatMessageNode('"+self.identifier+"', '"+base64_string+"')")
                    self.update_signal.emit(self.identifier,base64_string)
                else:
                    print("empty message, increaased counter")
            except Exception as e:
                print("Bad worker exception :'(")
                print(e)
                pass
        self.enable_signal.emit()
        print("Worker finished.")
        # kill worker
        self.deleteLater()
        self.father._thread.quit()
        if self._thread is not None:
            self._thread.quit()
        

class JavascriptWindow(QMainWindow):
    view = None
    text_box = None
    provider = None
    _worker = None
    _thread = None # background thread for workers updating backend answers
    _voiceThread = None
    _voiceWorker = None

    def __init__(self):
        print("init... javascript window")
        super().__init__()
        self.provider = Bing()#ChatGPTSpanish()#Gpt4free()#You()#OpenChat()
        self.voiceProvider = Bing()#Watson()

    def voiceSelectionChange(self,i):
        print("Items in the list are :")
        print(self.sender().currentText())
        if self.sender().currentText() == "Watson":
            self.voiceProvider = Watson()
        elif self.sender().currentText() == "Bing":
            self.voiceProvider = Bing()

    @QtCore.Slot()
    def update_text_box(self, text):
        self.text_box.setText(text)

    @QtCore.Slot()
    def update_transcribe_button(self):
        self.transcribe_button.setEnabled(True)

    def transcribe(self):
        print("transcribe")
        self.transcribe_button.setEnabled(False)

        self._voiceThread = None
        self._voiceWorker = None
        
        self._voiceThread = QThread()
        self._voiceThread.setObjectName("VoiceWorkerThread")
        self._voiceWorker = VoiceWorker(self,self.voiceProvider)
        self._voiceWorker.moveToThread(self._voiceThread)

        self._voiceWorker.update_signal.connect(self.update_text_box)
        self._voiceWorker.enable_signal.connect(self.update_transcribe_button)

        self._voiceThread.started.connect(self._voiceWorker.run)
        self._voiceThread.start()

    def process_cookie(self, c):
        reloadMainPage = False
        cookie = ""
        
        print(f"Name: {c.name()}, Value: {c.value()}, Domain: {c.domain()}")
        cookie += c.name() + "=" + c.value() + ";"
        if c.name() == b'cct':
            print("cct found")
            reloadMainPage = True
        else:
            print("cct not found: " + str(c.name()))

        print(f"Updated cookie: {cookie}")
        if(self.provider is not None and isinstance(self.provider, Bing)):
            self.provider.cookies += cookie
            print("Bing cookies updated")

        if reloadMainPage:
            print("reset main page")
            self.view.load(QUrl('http://localhost:5000/'))

    def proccessBingCaptha(self, view):

        print("proccessBingCaptha")
        url = self.provider.getCaptchaSolverUrl()

        cookie_store = view.page().profile().cookieStore()
        view.load(QUrl(url))
        # getAll doesn't exists so I need a replacement
        cookie_store.cookieAdded.connect(self.process_cookie)

        view.loadFinished.connect(self.onLoadFinished)

    def onLoadFinished(self, ok):
        if ok:
            print("Page loaded")
        else:
            print("Error loading page")
    
    def reset(self):
        solveCaptcha = False
        if self.combobox.currentText() == "ChatGPT Spanish":
            self.provider = ChatGPTSpanish()
        elif self.combobox.currentText() == "GPT4Free":
            self.provider = Gpt4free()
        elif self.combobox.currentText() == "You":
            self.provider = You()

        elif self.combobox.currentText() == "Bing":
            self.provider = Bing()
            solveCaptcha = True
            self.proccessBingCaptha(self.view)
        elif self.combobox.currentText() == "OpenChat":
            self.provider = OpenChat()
        elif self.combobox.currentText() == "Wrtn(ai)":
            self.provider = WRTNAI()

        if self._worker is not None:
            try:
                self._worker.deleteLater()
                self._worker = None
            except Exception as e:
                print(e)
                pass


        # refresh label
        self.label.setText("Provider: " + self.combobox.currentText())
        if(not solveCaptcha):
            # refresh self.view
            self.view.load(QUrl('http://localhost:5000/'))

    def selectionchange(self,i):
        print("Items in the list are :")
        print(self.sender().currentText())
        self.reset()
        

    def send_message(self):
        random_identifier = uuid.uuid4().hex
        text_content = self.text_box.text()
        self.text_box.setText("")
        #avoid writing new message disabling text box
        self.text_box.setEnabled(False)
        self.send_button.setEnabled(False)
    
        self.view.page().runJavaScript("createChatMessageNodeUser('User','" + text_content + "','https://randomuser.me/api/portraits/men/32.jpg')")
        
        self.view.page().runJavaScript("createChatMessageNode('"+random_identifier+"', 'Bot','" + random_identifier + "','https://randomuser.me/api/portraits/men/9.jpg')")
        
        print("message order sent")

        self._thread = QThread()
        self._thread.setObjectName("WorkerThread")
        self._worker = ChatWorker(self,self.view, self.provider, text_content, random_identifier)
        self._worker.moveToThread(self._thread)

        self._worker.update_signal.connect(self.update_chat_message_node)
        self._worker.enable_signal.connect(self.enable_text_box)

        self._thread.started.connect(self._worker.run)
        self._thread.start()

        print("background message sent")

    @QtCore.Slot()
    def enable_text_box(self):
        self.text_box.setEnabled(True)
        self.send_button.setEnabled(True)

    @QtCore.Slot(str,str)
    def update_chat_message_node(self, identifier, base64_string):
        self.view.page().runJavaScript("updateChatMessageNode('"+identifier+"', '"+base64_string+"')")