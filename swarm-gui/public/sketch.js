let color = "#FFF";
let strokeWidth = 4;

let robots = [];
let pickup;
let dropoff;
let socket;

const canvas_width = 800
const canvas_height = 600
let map_width
let map_height

let lock = false;
let run = false;

let job_queue = [];

// prettify ALT + SHIFT + F

function setup() {
  // Start the socket connection
  socket = io.connect("http://localhost:5000");

  socket.on("init", data => {
    if (run) return;
    run = true;
    board = JSON.parse(data);

    map_width = board.width;
    map_height = board.height;
    agents = board.agents;

    adjustedX = canvas_width * (1 / map_width)
    adjustedY = canvas_height * ( 1 / map_height)

    // assign agents to robot array
    for (var key in agents) {
      if (agents.hasOwnProperty(key)) {
        sentRobot = agents[key];
        robot = new Robot(
          sentRobot.posX,
          sentRobot.posY,
          sentRobot.diam,
          sentRobot.speed
        );
        robot.setInterpolation(adjustedX, adjustedY);
        robots.push(robot);
      }
    }

    // assign objectives
    pickup = new Target(board.pickupX * adjustedX, board.pickupY * adjustedY, "#CC6600", "P");
    dropoff = new Target(board.dropoffX * adjustedX, board.dropoffY * adjustedY, "#993300", "D");

    pickup.setInterpolation(adjustedX, adjustedY)

    // Creating canvas
    const cv = createCanvas(canvas_width, canvas_height);
    cv.position(400, 50);
    cv.background(50, 89, 100);

    socket.emit("reply", "init completed");
  });

  // #command is equal to #robots
  socket.on("event", payload => {
    if (!run) return;
    try {
      requestLock();
      // console.log("Command: "+ commandJSON )
      command = payloadDecoder(payload);
      job_queue.push(command);
      // console.log("Queue length: " + job_queue.length);
      if (job_queue.length > 100) job_queue = [];
    } finally {
      releaseLock();
    }
  });

  socket.on("connect_failed", connect_failed)
  socket.io.on("connect_error", connect_error)

  // Getting our buttons and the holder through the p5.js dom
  const color_btn = select("#color-btn");

  // Adding a mousePressed listener to the button
  color_btn.mousePressed(() => {
    console.log("send reply")
    socket.emit("reply", "init");
  });
}

function connect_failed(){
  console.log("lemao")
}

function connect_error(){
  console.log("Server offline")
}

function payloadDecoder(payload) {
  payload = JSON.parse(payload);

  return payload;
}

async function requestLock() {
  while (!lock) {
    await sleep(100);
  }
  lock = true;
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
  fill(255);
  displayLine();

  if (typeof robots == "undefined" || robots.length == 0) return;

  const c = job_queue.shift();
  if (typeof c == "undefined") {
    defaultDisplay(); // display current environment
    return;
  }

  agent_job(c.agents);
  objective_job(c.pickupX, c.pickupY);
}

function agent_job(command) {
  for (var id in command) {
    if (command.hasOwnProperty(id)) {
      data = command[id];
      robots[id].move(data.posX, data.posY);
      // console.log("moved: " + robots[id].getPosition())
      robots[id].display();
    }
  }
}

function objective_job(x, y) {
  pickup.display(
    {
      'x':x,
      'y':y
    } 
  );
  dropoff.display({});
}

function defaultDisplay() {
  for (i = 0; i < robots.length; i++) {
    robots[i].display();
  }
  objective_job();
}

let y = 100;
function displayLine() {
  y = y - 1;
  if (y < 0) {
    y = height;
  }
  line(0, y, width, y);
}

// Target class
class Target {
  constructor(x, y, color, letter) {
    this.posX = x;
    this.posY = y;
    this.fill = color;
    this.letter = letter;
  }
  display(opts) {
    if (opts['x'] > -1 && opts['y'] > -1){
      this.posX = opts['x'] * this.canvasSpeedX
      this.posY = opts['y'] * this.canvasSpeedY
    }
    fill(this.fill);
    rect(this.posX, this.posY, 20, 20);
    fill(0);
    textSize(20);
    text(this.letter, this.posX + 4, this.posY + 18);
  }

  setInterpolation(x, y) {
    this.canvasSpeedX = x
    this.canvasSpeedY = y
  }
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
    this.x = x * this.canvasSpeedX;
    this.y = y * this.canvasSpeedY;
  }

  moveRandom() {
    this.x += random(-this.speed, this.speed);
    this.y += random(-this.speed, this.speed);
  }

  setInterpolation(x, y) {
    this.canvasSpeedX = x * this.speed;
    this.canvasSpeedY = y * this.speed;
  }

  display() {
    // check if border has been reached and reset

    ellipse(this.x, this.y, this.diameter, this.diameter);
  }

  getPosition() {
    return this.x + ", " + this.y;
  }
}
