import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from gui.javascriptwindow import JavascriptWindow

class MainWindow(JavascriptWindow):

    def __init__(self):
        super().__init__()

        window = QWidget()
        self.setWindowTitle('pyChat')
        self.setGeometry(100, 100, 1280, 800)
        
        layout = QVBoxLayout()
        window.setLayout(layout)

        self.view = QWebEngineView()
        self.view.load(QUrl('http://localhost:5000/'))
        layout.addWidget(self.view)

        hbox = QHBoxLayout()

        self.text_box = QLineEdit()
        hbox.addWidget(self.text_box)

        send_button = QPushButton('Send')
        send_button.clicked.connect(self.send_message)
        hbox.addWidget(send_button)

        layout.addLayout(hbox)

        self.setCentralWidget(window)
        print("layout added")
        
        
