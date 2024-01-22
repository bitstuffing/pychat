from gui.backend import run_flask
from threading import Thread
from gui.mainwindow import MainWindow
from PySide6.QtWidgets import QApplication, QWidget
import sys
        
def main():
    server = Thread(target=run_flask)
    # start in background
    server.daemon = True
    server.start()
    
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
    #sys.exit(app.exec())


if __name__ == '__main__':
    main()