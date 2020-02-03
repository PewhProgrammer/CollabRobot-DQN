"""Functions for routing the data correctly through the GUI interface.
"""

from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from common.serializer import export_state, export_start_state

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.debug = False
socketio = SocketIO(app, cors_allowed_origins="*")

# enable CORS
CORS(app)

# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

env = None


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('reply')
def test_message(message):
    if message == 'init':
        payload = export_start_state(env)
        emit('init', payload)


def render_env(sio):
    if sio is None:
        return
    sio.sleep(0.000001)  # forced, else the stream will block
    with app.test_request_context():
        payload = export_state(env)
        socketio.emit('event', payload)


def start_server():
    print('starting flask server')
    socketio.run(app, port=5000)


def init_flask_app(envWrap):
    global env
    env = envWrap.get_env()
    socketio.start_background_task(start_server)
    return socketio
