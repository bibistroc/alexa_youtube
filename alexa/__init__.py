from flask import Flask
from flask_ask import Ask
from flask_socketio import SocketIO

app = Flask(__name__)
ask = Ask(app, '/alexa')
sio = SocketIO(app)

import intents
import controller
