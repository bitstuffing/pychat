import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from threading import Thread
import os
import threading
import queue as q
import asyncio
import time
import base64

#TODO
from core.openchat import OpenChat

PADDING = 2

class pyChat(toga.App):

    content = ""
    updating = False

    def on_reset(self, widget, **kwargs):
        self.label.text = "Reset!"

    async def read_messages(self, widget, **kwargs):

        oldcontent = self.content
        
        response = ""
        newContent = ""
        counter = 0
        import uuid
        random_identifier = uuid.uuid4().hex

        exit = False
        self.updating = True

        while not exit:
            try:
                self.webview.evaluate_javascript("createChatMessageNode('"+random_identifier+"', 'Bot','" + random_identifier + "','https://randomuser.me/api/portraits/men/9.jpg')")
                exit = True
            except:
                exit = False
                pass
        while counter < 10:
            try:
                response += self.queue.get(False)
                counter = 1 # reset counter
                # encode message to javascript base64    
                sample_string_bytes = response.encode("utf-8") 
                base64_bytes = base64.b64encode(sample_string_bytes) 
                base64_string = base64_bytes.decode("utf-8")
                self.webview.evaluate_javascript("updateChatMessageNode('"+random_identifier+"', '"+base64_string+"')")
            except q.Empty:
                counter+=1
                self.label.text = f"counter: {counter}"
                pass

            await asyncio.sleep(0.2)

        self.updating = False

        self.label.text = "Response finished!"
        self.content += newContent
        
        # encode message to javascript base64
        sample_string_bytes = response.encode("utf-8") 
        base64_bytes = base64.b64encode(sample_string_bytes) 
        base64_string = base64_bytes.decode("utf-8")
        self.webview.evaluate_javascript("updateChatMessageNode('"+random_identifier+"', '"+base64_string+"')")
        
        return response

    def do_gain_focus(self, widget, **kwargs):
        self.label.text = "waiting you!"

    def do_extract_values(self, widget, **kwargs):

        if self.updating:
            return
        
        content = self.text_input.value
        if self.content == "":
            self.create_conversation(content)

        self.label.text = content
        self.text_input.value = ""

        self.do_background_petition(content)

    def do_background_petition(self, content):
       
        self.queue = q.Queue()

        self.webview.evaluate_javascript("createChatMessageNodeUser('User','" + content + "','https://randomuser.me/api/portraits/men/32.jpg')")
        
        #read_message_thread = threading.Thread(target=self.read_messages, args=(self.queue, content,))
        #read_message_thread.start()
        self.add_background_task(self.read_messages)
        
        #response = self.openchat.send_message(content, stream=True, queue=queue)
        if isinstance(self.chat,OpenChat):
            send_message_thread = threading.Thread(target=self.chat.send_message, args=(content, True, self.queue, ), daemon=True)
            send_message_thread.start()

    def on_webview_load(self, widget, **kwargs):
        #self.label.text = "content loaded!"
        pass

    def on_get_url(self, widget, **kwargs):
        self.label.text = self.webview.url

    def delete_conversation(self, widget, **kwargs):
        self.label.text = "conversation deleted!"

    def create_conversation(self, content):
        
        self.chat = OpenChat()
            
        self.content = content


    def startup(self):
        
        self.main_window = toga.MainWindow(size=(1280, 800))
        self.label = toga.Label("waiting for you!", style=Pack(flex=0, padding=5))

        self.text_input = toga.TextInput(
            placeholder="Type something...",
            style=Pack(padding=PADDING, flex=1),
            on_confirm=self.do_extract_values,
            on_gain_focus=self.do_gain_focus
        )

        self.webview = toga.WebView(
            url='http://127.0.0.1:5000/',
            style=Pack(flex=1)
        ) 

        text_box = toga.Box(
            children=[
                toga.Box(
                    style=Pack(direction=ROW),
                    children=[
                        toga.Box(
                            style=Pack(flex=1, direction=COLUMN),
                            children=[
                                self.text_input
                            ]
                        ),
                        toga.Button("New", on_press=self.on_reset),
                    ],
                )
            ],
            style=Pack(flex=0, direction=COLUMN, padding=PADDING),
        )

        
        box = toga.Box(
            children=[
                self.webview,
                text_box,
                self.label,
            ],
            style=Pack(flex=1, direction=COLUMN),
        )

        self.main_window.content = box
        self.main_window.show()


def main():
    return pyChat()

if __name__ == '__main__':
    app = main()
    app.main_loop()