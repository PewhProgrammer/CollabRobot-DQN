const canvas_width = 500;
const canvas_height = 500;
let map_width;
let map_height;

let robots = [];

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

function objective_job(positions) {
  // we only draw pickups

  pickups[0].display(positions);
  dropoffs[0].display({});
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
  constructor(pos, x2, y2, color, letter) {
    this.pos = [pos];
    this.fill = color;
    this.letter = letter;
    this.canvasSpeedX = x2;
    this.canvasSpeedY = y2;
    this.offsetY = 18;
    this.offsetX = 4;
    this.size = 20;
  }

  display(opts) {
    prev = [];

    if (typeof opts === "undefined" || Object.entries(opts).length === 0) {
      // display dropoff
      this.pos.forEach((  value, i) => {
        if (i > 0){
          this.display_connection(value, prev)
          this.display_single(prev);
        }
        prev = value
      });
      this.display_single(prev);
      return;
    }
    opts.forEach((value, i) => {

      if (i > 0){
        this.display_connection(value, prev)
        this.display_single(prev);
      }
      prev = value
    });

    this.display_single(prev);
  }

  display_connection(value, prev){
    stroke(this.fill);
    strokeWeight(7);
    line(
      value[0] * this.canvasSpeedX + this.offsetX + this.size * 0.5 ,
      value[1] * this.canvasSpeedY + this.offsetY - this.size * 0.4,
      prev[0] * this.canvasSpeedX + this.offsetX + this.size * 0.5,
      prev[1] * this.canvasSpeedY + this.offsetY - this.size * 0.4
    );
    stroke(0);
    strokeWeight(1);
  }

  display_single(opts) {
    let posX = opts[0] * this.canvasSpeedX;
    let posY = opts[1] * this.canvasSpeedY;

    fill(this.fill);
    rect(posX, posY, this.size, this.size);
    fill(0);
    textSize(20);
    text(this.letter, posX + this.offsetX, posY + this.offsetY);
  }

  addPoints(pos) {
    this.pos.push(pos);
  }
}

// Robot class
class Robot {
  constructor(pos, diam = 10, speed = 1, agent = false) {
    this.x = pos[0];
    this.y = pos[1];
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
    if (this.agent) fill(255);
    else fill(155, 155, 155);
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
