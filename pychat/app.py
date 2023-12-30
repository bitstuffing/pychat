"""
GUI for pyChat core
"""
import toga
from toga.style import Pack
from toga.constants import CENTER, COLUMN, HIDDEN, ROW, VISIBLE

from core.openchat import OpenChat
import os
import threading
import queue as q
import asyncio

import base64
#import platform


PADDING = 2

class pyChat(toga.App):

    content = ""

    def on_webview_load(self, widget, **kwargs):
        #self.label.text = "content loaded!"
        pass

    def on_get_url(self, widget, **kwargs):
        self.label.text = self.webview.url

    def do_extract_values(self, widget, **kwargs):

        content = self.text_input.value
        if self.content == "":
            summary = content[0 : min(20, len(content))]
            self.left_panel.add(toga.Button(summary, on_press=self.on_click))
            self.openchat = OpenChat()

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
        send_message_thread = threading.Thread(target=self.openchat.send_message, args=(content, True, self.queue))
        send_message_thread.start()


    #def read_messages(self, queue, content):
    async def read_messages(self, widget, **kwargs):

        oldcontent = self.content
        
        response = ""
        newContent = ""
        counter = 0
        import uuid
        random_identifier = uuid.uuid4().hex

        self.webview.evaluate_javascript("createChatMessageNode('"+random_identifier+"', 'Bot','" + random_identifier + "','https://randomuser.me/api/portraits/men/9.jpg')")

        while counter < 20:
            try:
                response += self.queue.get(False)
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

    def on_click(self, widget, **kwargs):
        self.label.text = "Hola Mundo!"

    def startup(self):
        
        self.main_window = toga.MainWindow(size=(1280, 800))
        self.label = toga.Label("waiting for you!", style=Pack(flex=0, padding=5))

        self.text_input = toga.TextInput(
            placeholder="Type something...",
            style=Pack(padding=PADDING),
            on_confirm=self.do_extract_values,
            on_gain_focus=self.do_gain_focus
        )

        text_box = toga.Box(
            children=[
                toga.Box(
                    style=Pack(direction=COLUMN),
                    children=[
                        self.text_input
                    ],
                )
            ],
            style=Pack(flex=0, direction=COLUMN, padding=PADDING),
        )

        self.webview = toga.WebView(
            on_webview_load=self.on_webview_load,
            style=Pack(flex=1),
        )

        # get file content from resources/base.html
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(current_dir+"/resources/base.html", "r") as f:
            content = f.read()
        self.webview.set_content(
            root_url="",
            content = content,
        )

        self.left_panel = toga.Box(
            style=Pack(padding=PADDING, flex=1, direction=ROW)
        )

        box = toga.Box(
            children=[
                self.webview,
                text_box,
                self.label,
            ],
            style=Pack(flex=1, direction=COLUMN),
        )

        #print(content)
        #if platform.system() == 'Linux':
        if 'ANDROID_STORAGE' not in os.environ:
            content_box = toga.SplitContainer(style=Pack(flex=1))
            content_box.content = [(self.left_panel, 1), (box, 3)]
            self.main_window.content = content_box
        else:
            self.main_window.content = box

        self.main_window.show()


def main():
    return pyChat()
