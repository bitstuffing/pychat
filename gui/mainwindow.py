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

        self.transcribe_button = QPushButton('Voice')
        self.transcribe_button.clicked.connect(self.transcribe)
        hbox.addWidget(self.transcribe_button)

        voice_provider = QComboBox()
        voice_provider.addItem("Bing")
        voice_provider.addItem("Watson")
        voice_provider.setEnabled(False) # just for code uploaded to github, when watson is going to be integrated, this line must be removed 
        voice_provider.currentIndexChanged.connect(self.voiceSelectionChange)
        hbox.addWidget(voice_provider)

        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.send_message)
        hbox.addWidget(self.send_button)

        layout.addLayout(hbox)

        hbox2 = QHBoxLayout()
        self.label = QLineEdit("Provider: Bing")
        self.label.setReadOnly(True)
        self.label.setStyleSheet("border: none;")
        self.combobox = QComboBox()
        self.combobox.addItem("OpenChat")
        self.combobox.addItem("Bing")
        self.combobox.addItem("ChatGPT Spanish")
        self.combobox.addItem("GPT4Free")
        self.combobox.addItem("You")
        self.combobox.addItem("Wrtn(ai)")
        self.combobox.currentIndexChanged.connect(self.selectionchange)
        hbox2.addWidget(self.label)
        hbox2.addWidget(self.combobox)

        reset_button = QPushButton('Reset')
        reset_button.clicked.connect(self.reset)
        hbox2.addWidget(reset_button)
        layout.addLayout(hbox2)

        self.setCentralWidget(window)
        self.reset() # Bing needs it
