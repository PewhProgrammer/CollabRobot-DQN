const canvas_width = 400;
const canvas_height = 300;
let map_width;
let map_height;

let robots = []


// prettify ALT + SHIFT + F 

function agent_job(command) {
  for (var id in command) {
    if (command.hasOwnProperty(id)) {
      tmp = command[id];
      robots[id].move(tmp[0], tmp[1]);
      // console.log("moved: " + robots[id].getPosition() + " id: " + id)
      robots[id].display();
    }
  }
}

function objective_job(pos) {
  pickup.display({
    x: pos[0],
    y: pos[1]
  });
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
    if (opts["x"] > -1 && opts["y"] > -1) {
      this.posX = opts["x"] * this.canvasSpeedX;
      this.posY = opts["y"] * this.canvasSpeedY;
    }
    fill(this.fill);
    rect(this.posX, this.posY, 20, 20);
    fill(0);
    textSize(20);
    text(this.letter, this.posX + 4, this.posY + 18);
  }

  setInterpolation(x, y) {
    this.canvasSpeedX = x;
    this.canvasSpeedY = y;
  }
}

// Robot class
class Robot {
  constructor(posX, posY, diam = 10, speed = 1, agent = false) {
    this.x = posX;
    this.y = posY;
    this.diameter = diam;
    this.speed = speed;
    this.agent = agent; // fill color; yellow if agent, white otherwise
  }

  move(x, y) {
    this.x = x * this.canvasSpeedX;
    this.y = y * this.canvasSpeedY;
  }

  setInterpolation(x, y) {
    this.canvasSpeedX = x * this.speed;
    this.canvasSpeedY = y * this.speed;
  }

  display() {
    if(this.agent) fill(255)
    else fill(155,155,155)
    // check if border has been reached and reset
    ellipse(this.x, this.y, this.diameter, this.diameter);
  }

  getPosition() {
    return this.x + ", " + this.y;
  }
}

var slider = document.getElementById("myRange");
var output = document.getElementById("speed");
output.innerHTML = slider.value; // Display the default slider value

