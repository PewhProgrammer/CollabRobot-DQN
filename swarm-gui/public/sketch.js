let color = '#FFF'
let strokeWidth = 4

let robots = [];
let socket

let window_x = 800
let window_y = 600

let lock = false
let run = false

let job_queue = [];

function setup() {

  // Start the socket connection
  socket = io.connect('http://localhost:5000')

  socket.on('init', data => {
    if (run) return
    run = true
    board = JSON.parse(data)
    console.log("board: " + JSON.stringify(board))
    window_x = board.width
    window_y = board.height
    for (i = 0; i < board.units.length; i++) {
      sentRobot = board.units[i]
      robo = new Robot(sentRobot.posX, sentRobot.posY,
        sentRobot.diam, sentRobot.speed)
      robots.push(robo)
    }


    // Creating canvas
    const cv = createCanvas(window_x, window_y)
    cv.position(400, 50)
    cv.background(50, 89, 100)

    socket.emit('reply', 'init completed')

  })

  // #command is equal to #robots
  socket.on('event', commandJSON => {
    try {
      requestLock()
      command = JSON.parse(commandJSON)
      job_queue.push(command)
      console.log("Queue length: "+job_queue.length)
    } finally {
      releaseLock()
    }
  })

  // Getting our buttons and the holder through the p5.js dom
  const color_btn = select('#color-btn')

  // Adding a mousePressed listener to the button
  color_btn.mousePressed(() => {
    socket.emit('reply', 'init')
  })
}

async function requestLock() {
  while (!lock) {
    await sleep(100);
  }
  lock = true
}

function releaseLock() {
  lock = false;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function mousePressed() {
  // socket.emit('reply', 'init')
}

function draw() {
  background(50, 89, 100);
  displayLine()

  if (typeof robots == 'undefined' || robots.length == 0) 
    return

  let command = job_queue.shift();
  if (typeof command !== 'undefined' && command.length > 0) { // queue is now [5]
    for (i = 0; i < command.length; i++) {
      data = command[i]
      robots[i].move(data.posX, data.posY);
      robots[i].display();
    }
  } else {
    for (i = 0; i < robots.length; i++) {
      robots[i].display();
    }
  }
}

let y = 100;
function displayLine() {
  y = y - 1;
  if (y < 0) {
    y = height;
  }
  line(0, y, width, y);
}

// Robot class
class Robot {

  constructor(posX, posY, diam, speed) {
    this.x = posX;
    this.y = posY;
    this.diameter = diam;
    this.speed = speed;
  }

  move(x, y) {
    this.x = x;
    this.y = y;
  }

  moveRandom() {
    this.x += random(-this.speed, this.speed);
    this.y += random(-this.speed, this.speed);
  }

  display() {
    // checck if border has been reached and reset
    if (this.x > window_x) this.x -= window_x
    else if (this.x < 0) this.x += window_x
    if (this.y > window_y) this.y -= window_y
    else if (this.y < 0) this.y += window_y

    ellipse(this.x, this.y, this.diameter, this.diameter);
  }

  getPosition() {
    return this.x + ", " + this.y
  }
}
