#import os
#import tensorflow as tf
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import time
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.debug = False
socketio = SocketIO(app, cors_allowed_origins="*")

class Board(object):
    width = 0
    height = 0
    units = []

    # The class "constructor" - It's actually an initializer 
    def __init__(self, width, height, robots):
        self.width = width
        self.height = height
        self.units = robots

class Robot(object):
    posX = 0
    posY = 0
    diam = 0
    speed = 0

    # The class "constructor" - It's actually an initializer 
    def __init__(self, x, y, diameter, speed):
        self.posX = x
        self.posY = y
        self.diam = diameter
        self.speed = speed

def make_robot(x, y, diameter, speed):
    return Robot(x, y, diameter, speed)

def move_robot(board):
    for x in board.units:
        x.posX += random.randint(-1,1)
        x.posY += random.randint(-1,1)
    return board

def make_board(width, height, count):
    robots = []
    for x in range(count):
        robot = make_robot(width*random.uniform(0.0,1.0)
        ,height*random.uniform(0.0,1.0),20,1)
        robots.append(robot)
        
    return Board(width, height, robots)

board = make_board(800, 600, 10)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('reply')
def test_message(message):
    global board
    if message == 'init':
        emit('init', json.dumps(board, default=lambda o: o.__dict__), separators=(',', ':'))
    else:
        while True:
            board = move_robot(board)
            emit('event', json.dumps(board.units,default=lambda o: o.__dict__, separators=(',', ':')))
            time.sleep(0.02)

if __name__ == '__main__':
    socketio.run(app, port = 5000)

#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#print(tf.reduce_sum(tf.random.normal([1000, 1000])))