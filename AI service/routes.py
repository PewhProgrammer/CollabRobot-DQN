"""Functions for routing the data correctly through the GUI interface.
"""

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from common.environment import get_env
from common.helper import update_env_encode, new_env_encode

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
        payload = new_env_encode(get_env())
        emit('init', payload)


def render_env(board):
    with app.test_request_context():
        # information to render

        payload = update_env_encode(board)
        socketio.emit('event', payload)


def start_server():
    print('starting flask server')
    socketio.run(app, port=5000)


def init_flask_app():
    socketio.start_background_task(start_server)
    return socketio
