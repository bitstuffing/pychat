import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QComboBox, QLabel
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
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
        #self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.page().settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, False)
        self.view.load(QUrl('http://localhost:5000/'))
        layout.addWidget(self.view)

        hbox = QHBoxLayout()

        self.text_box = QLineEdit()
        self.text_box.setPlaceholderText('Type a message...')
        self.text_box.returnPressed.connect(self.send_message)
        hbox.addWidget(self.text_box)

        transcribe_button = QPushButton('Voice')
        transcribe_button.clicked.connect(self.transcribe)
        hbox.addWidget(transcribe_button)

        voice_provider = QComboBox()
        voice_provider.addItem("Watson")
        voice_provider.addItem("Bing")
        voice_provider.currentIndexChanged.connect(self.voiceSelectionChange)
        hbox.addWidget(voice_provider)

        send_button = QPushButton('Send')
        send_button.clicked.connect(self.send_message)
        hbox.addWidget(send_button)

        layout.addLayout(hbox)

        hbox2 = QHBoxLayout()
        self.label = QLabel("Provider: OpenChat")
        combobox = QComboBox()
        combobox.addItem("OpenChat")
        combobox.addItem("ChatGPT Spanish")
        combobox.addItem("GPT4Free")
        combobox.addItem("You")
        combobox.addItem("Bing")
        combobox.addItem("Wrtn(ai)")
        combobox.currentIndexChanged.connect(self.selectionchange)
        hbox2.addWidget(self.label)
        hbox2.addWidget(combobox)
        layout.addLayout(hbox2)

        self.setCentralWidget(window)
        print("layout added")
        
        
