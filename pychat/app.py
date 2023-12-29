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

        self.content += f"<b>Me: <span style='background-color: white;'>{content}</span></b><br/>"

        current_dir = os.path.dirname(os.path.abspath(__file__))

        self.webview.set_content(
            root_url="file://"+current_dir+"/resources/base.html",
            content = self.content,
        )
        self.do_background_petition(content)

    def do_background_petition(self, content):
       
        queue = q.Queue()
        
        #response = self.openchat.send_message(content, stream=True, queue=queue)
        send_message_thread = threading.Thread(target=self.openchat.send_message, args=(content, True, queue))
        send_message_thread.start()

        read_message_thread = threading.Thread(target=self.read_messages, args=(queue, content,))
        read_message_thread.start()


    def read_messages(self, queue, content):

        oldcontent = self.content
        
        response = ""
        newContent = ""
        counter = 0

        while counter < 20:
            newContent = f"<b>Me: <span style='background-color: white;'>{content}</span></b><br/>"

            try:
                response += queue.get(False)
            except q.Empty:
                counter+=1
                self.label.text = f"counter: {counter}"
                pass

            newContent += f"<b>Bot: <span style='background-color: grey;'>{response}</span></b><br/>"
            
            self.webview.set_content(
                root_url="file://resources/base.html",
                content = newContent,
            )

            #sleep 1 second
            import time
            time.sleep(0.2)

        self.label.text = "Response finished!"
        self.content += newContent

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
            #url="file://"+os.getcwd()+"/resources/base.html",
            on_webview_load=self.on_webview_load,
            style=Pack(flex=1),
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
        content_box = toga.SplitContainer(style=Pack(flex=1))
        content_box.content = [(self.left_panel, 1), (box, 3)]

        self.main_window.content = content_box
        self.main_window.show()


def main():
    return pyChat()
