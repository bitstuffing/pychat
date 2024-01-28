from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtCore import QUrl, QEventLoop, QTimer
from PySide6.QtWidgets import QApplication, QVBoxLayout
import sys

# JavaScriptConsoleMessageLevel

class WebPage(QWebEnginePage):

    def __init__(self, parent=None):
       QWebEnginePage.__init__(self, parent)

    def javaScriptConsoleMessage(self, level, msg, linenumber, source_id):
        print(msg)
        prefix = {
            QWebEnginePage.JavaScriptConsoleMessageLevel.InfoMessageLevel: 'INFO',
            QWebEnginePage.JavaScriptConsoleMessageLevel.WarningMessageLevel: 'WARNING'
        }.get(level, 'ERROR')
        if prefix in ('ERROR') and not 'ResizeObserver loop limit exceeded' in msg:
            try:
                print('%s: %s:%s: %s' % (prefix, source_id, linenumber, msg), file=sys.stderr)
                sys.stderr.flush()
            except EnvironmentError:
                pass
    
    # experimental, put a return false at the end
    def acceptNavigationRequest(self, url, req_type, is_main_frame):
        if req_type == QWebEnginePage.NavigationType.NavigationTypeReload:
            return True
        if req_type == QWebEnginePage.NavigationType.NavigationTypeBackForward:
            return True
        if url.scheme() in ('data', 'file', 'blob'):
            return True
        if url.scheme() in ('http', 'https') and req_type == QWebEnginePage.NavigationType.NavigationTypeLinkClicked:
            print('Blocking external navigation request to: ', url.toString())
            return False
        print('NOT Blocking navigation request to:', url.toString())
        return True

# idea extracted from https://github.com/Sigil-Ebook/EpubJSReader/blob/master/reader_demo_v3.py
class WebView(QWebEngineView):
    def __init__(self, parent=None):
        QWebEngineView.__init__(self, parent)

        self._page = WebPage(self)
        self.setPage(self._page)


    def process_cookies(self, cookies):
        for cookie in cookies:
            print(f"Cookie: {cookie.name()}={cookie.value()}")

    def on_console_message(self, level, message, lineNumber, sourceID):
        print(f"Console message: {level} {message} {lineNumber} {sourceID}")

    def load_finished(self, ok):
        print("Load finished")
        if ok:
            print("ok")
            
            self.page().javaScriptConsoleMessage = self.on_console_message

            self.page().runJavaScript("console.log('Hello from JavaScript!')")
            # find the login input fields and fill them
            # username is an input with aria-label="Email / Username"
            self.page().runJavaScript("document.querySelector('input[aria-label=\"Email / Username\"]').value = 'parekot353@bitofee.com'")
            # password is an input with aria-label="Password"
            self.page().runJavaScript("document.querySelector('input[aria-label=\"Password\"]').value = 'Passwd.11'")
            
            # confirm that we have filled the fields
            self.page().runJavaScript("console.log(document.querySelector('input[aria-label=\"Email / Username\"]').value)")
            self.page().runJavaScript("console.log(document.querySelector('input[aria-label=\"Password\"]').value)")
            # read console output
            self.page().runJavaScript("console.log('Hello from JavaScript!')") 


            # javascript should redirect us to the main page, so we wait for it to load
            self.page().loadFinished.connect(self.load_finished_next)

            # well, at this point javascript should have finished, but we are not sure, so we can just take into account ajax requests and monitor them
            self.page().loadProgress.connect(self.load_finished_next)
            self.page().loadStarted.connect(self.load_finished_next)
            # monitor javascript working ajax requests

            # wait 1 seconds
            loop = QEventLoop()
            QTimer.singleShot(1000, loop.quit)
            loop.exec()

            # console log the button
            '''
            await fetch('/api/auth/signin', {
              method: 'POST',
              body: (0, a.Al) (g, 70614, 1)
            })
            '''
            # needs to build a and a.Al
            self.page().runJavaScript("console.log(a)")

            # find the login button and click it, button is a button with attribute type="button" node with content text "Sign in"
            #self.page().runJavaScript("document.querySelector('button[type=\"button\"]').click()")
            self.page().runJavaScript("console.log(document.querySelector('button[type=\"button\"]'))")




    def load_finished_next(self, ok):
        print("Load finished 2")
        if ok:
            print("ok")


def process_cookie(c):
    cookie = ""
    
    print(f"Name: {c.name()}, Value: {c.value()}, Domain: {c.domain()}")
    cookie += c.name() + "=" + c.value() + ";"
    

app = QApplication()
page = WebView()

layout = QVBoxLayout()
layout.addWidget(page)

cookie_store = page.page().profile().cookieStore()

page.load(QUrl("https://ch4.us.to/auth/signin"))

cookie_store.cookieAdded.connect(process_cookie)
page.loadFinished.connect(page.load_finished)

app.exec()