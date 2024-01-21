from pychat.backend import run_flask
from threading import Thread
from pychat.app import main
        
if __name__ == '__main__':
    server_thread = Thread(target=run_flask)
    server_thread.start()
        
    main().main_loop()
