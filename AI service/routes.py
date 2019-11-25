"""Functions for routing the data correctly through the GUI interface.
"""

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from common.environment import get_env
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.debug = False
socketio = SocketIO(app, cors_allowed_origins="*")


# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('reply')
def test_message(message):
    if message == 'init':
        emit('init', json.dumps(get_env(), default=lambda o: o.__dict__), separators=(',', ':'))


def render_state(board):
    with app.test_request_context():
        # information to render
        # TODO: more efficient to decode x/y into one state value; maybe in new JSON format
        # TODO: include pickup object and dropoff zone
        socketio.emit('event', json.dumps(board.units, default=lambda o: o.__dict__, separators=(',', ':')))


def start_server():
    print('starting flask server')
    socketio.run(app, port=5000)


def init_flask_app():
    socketio.start_background_task(start_server)
    # socketio.sleep(5)
    return socketio
