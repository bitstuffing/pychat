import flask
from flask import Flask

def run_flask():
    app = Flask(__name__)

    # return files from the "static" folder
    @app.route('/<path:path>')
    def path(path):
        return flask.render_template(f"{path}.html")
    
    @app.route('/')
    def index():
        return flask.render_template('index.html')
    
    @app.route('/css/<path:path>')
    def css(path):
        return flask.send_from_directory('assets/css', path)
    
    @app.route('/js/<path:path>')
    def js(path):
        return flask.send_from_directory('assets/js', path)

    app.run()