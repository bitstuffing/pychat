from core.openchat import OpenChat
import uuid
from PySide6.QtCore import QObject, QThread, Signal, QRunnable
from PySide6.QtWidgets import QMainWindow
from PySide6 import QtCore
import time
import queue
import base64

class Worker(QRunnable, QObject):

    _thread = None
    provider = None
    queue = None
    message = None
    identifier = None
    update_signal = QtCore.Signal(str,str)


    def __init__(self, _thread, view, provider, message, identifier):
        QObject.__init__(self)
        QRunnable.__init__(self)
        
        self.provider = provider
        self.view = view
        self.message = message
        self.identifier = identifier
        self._thread = _thread
        

    def run(self):
        print("Worker started.")
        self.queue = queue.Queue()
        self.provider.send_message(message=self.message,stream=True,queue=self.queue)
        print("worker sent message, receiving...")

        message = ""
        counter = 0
        limit = 10
        #while self.queue has messages or self.queue is not empty or wait for 3 seconds if self.queue is empty
        while not self.queue.empty() or self.queue.qsize() > 0 or counter < limit:
            print("waiting for message...")
            counter += 1
            time.sleep(0.1)
            try:
                new_message = self.queue.get_nowait()
                if new_message != "":
                    counter = 0
                    message += new_message
                    
                    sample_string_bytes = message.encode("utf-8") 
                    base64_bytes = base64.b64encode(sample_string_bytes) 
                    base64_string = base64_bytes.decode("utf-8")
                    print(f"base64_string: {base64_string}")
                    # talk with main thread
                    #self.view.page().runJavaScript("updateChatMessageNode('"+self.identifier+"', '"+base64_string+"')")
                    self.update_signal.emit(self.identifier,base64_string)
                else:
                    print("empty message, increaased counter")
            except:
                print("Bad worker exception :'(")
                pass

        print("Worker finished.")
        # kill worker
        self.deleteLater()
        self._thread.quit()

class JavascriptWindow(QMainWindow):
    view = None
    text_box = None
    provider = None

    def __init__(self):
        print("init... javascript window")
        super().__init__()
        self.provider = OpenChat()


    def send_message(self):
        print("hola!!!")
        random_identifier = uuid.uuid4().hex
        text_content = self.text_box.text()

        self.view.page().runJavaScript("createChatMessageNodeUser('User','" + text_content + "','https://randomuser.me/api/portraits/men/32.jpg')")
        
        random_identifier2 = uuid.uuid4().hex
        self.view.page().runJavaScript("createChatMessageNode('"+random_identifier2+"', 'Bot','" + random_identifier2 + "','https://randomuser.me/api/portraits/men/9.jpg')")
        
        print("message order sent")

        self._thread = QThread()
        self._thread.setObjectName("WorkerThread")
        self._worker = Worker(self._thread,self.view, self.provider, text_content, random_identifier2)
        self._worker.moveToThread(self._thread)

        self._worker.update_signal.connect(self.update_chat_message_node)

        self._thread.started.connect(self._worker.run)
        self._thread.start()

        print("background message sent")

    @QtCore.Slot(str,str)
    def update_chat_message_node(self, identifier, base64_string):
        print("signal received!")
        self.view.page().runJavaScript("updateChatMessageNode('"+identifier+"', '"+base64_string+"')")