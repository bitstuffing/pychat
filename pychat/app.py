import os
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from core.bing import Bing
from core.helpers.binghelper import *
from core.you import You
from core.chatgptspanish import ChatGPTSpanish

import os
import time
import threading
import queue as q
import asyncio
from urllib.parse import quote
import base64


class PyChat(toga.App):

    content = ""
    chat = None

    def startup(self):
        self.main_window = toga.MainWindow(title=self.name)

        self.webview = toga.WebView()

        self.reset_webview()

        self.text_input = toga.TextInput(placeholder='Enter URL', style=Pack(flex=1), on_confirm=self.load_page)
        self.back_button = toga.Button('<', on_press=self.go_back)
        self.forward_button = toga.Button('>', on_press=self.go_forward)
        self.go_button = toga.Button('Go', on_press=self.load_page)
        self.selection = toga.Selection(
            items=[
                {"name": "ChatGPTSpanish"},
                {'name': 'WRTNAI'},
                {"name": "Ch4UsTo"},
                {"name": "Bing"},
                {"name": "You"},
            ],
            accessor="name",
        )

        option_panel = toga.Box(
            style=Pack(direction=ROW),
            children=[
                self.back_button,
                self.forward_button,
                self.text_input,
                self.go_button, 
            ]
        )

        self.option_panel = toga.Box(
                children=[
                    toga.Box(
                        style=Pack(direction=COLUMN),
                        children=[
                            option_panel,
                            self.selection
                        ]
                    ),
                ]
            )

        self.label = toga.Label("waiting for you!", style=Pack(flex=0, padding=5))

        self.left_panel = toga.Box(
            style=Pack(direction=COLUMN, padding=5),
            children=[
                toga.Label('Historical', style=Pack(padding=5)),
                toga.Button('Conversation 1', style=Pack(padding=5)),
            ]
        )

        vertical_split = toga.SplitContainer(
            content=[self.left_panel, self.main_content()],
            style=Pack(flex=1),
            direction=toga.SplitContainer.VERTICAL
        )

        self.main_window.content = vertical_split

        self.main_window.show()

    def main_content(self):
        return toga.SplitContainer(
            content=[self.webview, self.option_panel],
            style=Pack(flex=1),
            direction=toga.SplitContainer.HORIZONTAL
        )

    def reset_webview(self):
        # Obtener la ruta al directorio resources donde está base.html
        resource_dir = os.path.join(os.path.dirname(__file__), 'resources')
        base_html_path = os.path.join(resource_dir, 'base.html')

        with open(base_html_path, 'r', encoding='utf-8') as file:
            base_html_content = file.read()

        if 'ANDROID_STORAGE' not in os.environ:
            self.webview.set_content(
                root_url="",
                content=base_html_content,
            )
        else:
            self.webview.set_content(
                "data:text/html", base_html_content,
            )

    def create_conversation(self, content):
        
        if 'ANDROID_STORAGE' not in os.environ:
            selected = self.selection.value
            print("selected: ", selected)
            
            if selected.name == "Bing":
                self.chat = Bing()
            elif selected.name == "You":
                self.chat = You()
            elif selected.name == "ChatGPTSpanish":
                self.chat = ChatGPTSpanish()
            elif selected.name == "Ch4UsTo":
                self.chat = Ch4UsTo()
            elif selected.name == "WRTNAI":
                self.chat = WRTNAI()
            
        else:
            self.chat = OpenChat()
            
        self.content = content

        self.add_conversation(content)

    def add_conversation(self, content):
        self.left_panel.children.append(
            toga.Button(content, style=Pack(padding=5))
        )


    def load_page(self, widget, **kwargs):
        content = self.text_input.value
        if self.content == "":
            self.create_conversation(content)

        #self.label.text = content
        self.text_input.value = ""

        self.do_background_petition(content)

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
                tempResponse = self.queue.get(False)
                if isinstance(tempResponse, BingResponse):
                    if isinstance(tempResponse.chatmessage, BingMessageType1):
                        print(f"BingMessageType1, author: {tempResponse.chatmessage.arguments.messages[0].author}, message: {tempResponse.chatmessage.arguments.messages[0].text}")
                        tempResponse = str(tempResponse.chatmessage.arguments.messages[0].text)
                        response = tempResponse
                    else:
                        tempResponse = str(tempResponse)
                else:
                    response += tempResponse
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
            if response == "":
                await asyncio.sleep(0.2)
            else:
                await asyncio.sleep(0.1)

        self.label.text = "Response finished!"
        self.content += newContent
        
        # encode message to javascript base64
        sample_string_bytes = response.encode("utf-8") 
        base64_bytes = base64.b64encode(sample_string_bytes) 
        base64_string = base64_bytes.decode("utf-8")
        self.webview.evaluate_javascript("updateChatMessageNode('"+random_identifier+"', '"+base64_string+"')")
        
        return response

    def do_background_petition(self, content):
       
        self.queue = q.Queue()

        self.webview.evaluate_javascript("createChatMessageNodeUser('User','" + content + "','https://randomuser.me/api/portraits/men/32.jpg')")

        #sleep 0.5 seconds
        time.sleep(0.5)

        #read_message_thread = threading.Thread(target=self.read_messages, args=(self.queue, content,))
        #read_message_thread.start()
        self.add_background_task(self.read_messages)
        
        #response = self.openchat.send_message(content, stream=True, queue=queue)
        if isinstance(self.chat,Bing):
            #send_message_thread = threading.Thread(target=self.chat.init_conversation, args=(content, ))
            self.bingMessage = content
            self.add_background_task(self.bing_background_task)

        elif isinstance(self.chat,You) or isinstance(self.chat,ChatGPTSpanish):
            send_message_thread = threading.Thread(target=self.chat.send_message, args=(content, True, self.queue, ), daemon=True)
            send_message_thread.start()

        

    async def bing_background_task(self, widget, **kwargs):
        self.label.text = "Bing background task"
        await self.chat.init_conversation_async2(self.bingMessage, self.queue)

    def go_back(self, widget):
        if self.webview.can_go_back():
            self.webview.go_back()

    def go_forward(self, widget):
        if self.webview.can_go_forward():
            self.webview.go_forward()


def main():
    return PyChat('PyChat', 'com.example.pychat')


if __name__ == '__main__':
    main().main_loop()
