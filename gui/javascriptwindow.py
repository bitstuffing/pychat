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

class Worker(QRunnable, QObject):

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
        limit = 40 # TODO configure limit in settings for each provider

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
                    
                    
                    
                    sample_string_bytes = message.encode("utf-8") 
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

class JavascriptWindow(QMainWindow):
    view = None
    text_box = None
    provider = None
    _thread = None # background thread for workers updating backend answers

    def __init__(self):
        print("init... javascript window")
        super().__init__()
        self.provider = OpenChat()#ChatGPTSpanish()#Gpt4free()#You()#Bing()
        self.voiceProvider = Watson()

    def voiceSelectionChange(self,i):
        print("Items in the list are :")
        print(self.sender().currentText())
        if self.sender().currentText() == "Watson":
            self.voiceProvider = Watson()
        elif self.sender().currentText() == "Bing":
            self.voiceProvider = Bing()

    def transcribe(self):
        print("transcribe")

    def selectionchange(self,i):
        print("Items in the list are :")
        print(self.sender().currentText())
        if self.sender().currentText() == "ChatGPT Spanish":
            self.provider = ChatGPTSpanish()
        elif self.sender().currentText() == "GPT4Free":
            self.provider = Gpt4free()
        elif self.sender().currentText() == "You":
            self.provider = You()
        elif self.sender().currentText() == "Bing":
            self.provider = Bing()
        elif self.sender().currentText() == "OpenChat":
            self.provider = OpenChat()
        elif self.sender().currentText() == "Wrtn(ai)":
            self.provider = WRTNAI()

        # refresh label
        self.label.setText("Provider: " + self.sender().currentText())
        # refresh self.view
        self.view.load(QUrl('http://localhost:5000/'))
        

    def send_message(self):
        random_identifier = uuid.uuid4().hex
        text_content = self.text_box.text()
        self.text_box.setText("")
        #avoid writing new message disabling text box
        self.text_box.setEnabled(False)
    
        self.view.page().runJavaScript("createChatMessageNodeUser('User','" + text_content + "','https://randomuser.me/api/portraits/men/32.jpg')")
        
        self.view.page().runJavaScript("createChatMessageNode('"+random_identifier+"', 'Bot','" + random_identifier + "','https://randomuser.me/api/portraits/men/9.jpg')")
        
        print("message order sent")

        self._thread = QThread()
        self._thread.setObjectName("WorkerThread")
        self._worker = Worker(self,self.view, self.provider, text_content, random_identifier)
        self._worker.moveToThread(self._thread)

        self._worker.update_signal.connect(self.update_chat_message_node)
        self._worker.enable_signal.connect(self.enable_text_box)

        self._thread.started.connect(self._worker.run)
        self._thread.start()

        print("background message sent")

    @QtCore.Slot()
    def enable_text_box(self):
        self.text_box.setEnabled(True)

    @QtCore.Slot(str,str)
    def update_chat_message_node(self, identifier, base64_string):
        self.view.page().runJavaScript("updateChatMessageNode('"+identifier+"', '"+base64_string+"')")