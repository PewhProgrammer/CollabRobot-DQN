const canvas_width = 700;
let canvas_height = 500;
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
  const _amount_objectives$ = pickups.length;
  for(let i = 0; i < _amount_objectives$; i++){
    pickups[i].display([positions]);
    dropoffs[i].display({});
  }
}

function obstacle_job(board, scaledX, scaledY) {
  for (let y = 0; y < board.length; y++) {
    row = board[y];

    let placeholderX = 0;
    // char by char
    for (let x = 0; x < row.length; x++) {
      let char = row[x];

      if (char != "#") {
        if (char === "P") {
          placeholderX++;
          continue;
        }
        // console.log((x - placeholderX) * scaledX)
        fill(255);
        rect((x - placeholderX) * scaledX, y * scaledY, scaledX, scaledY);
      } else {
        fill("#465453");
        rect((x - placeholderX) * scaledX, y * scaledY, scaledX, scaledY);
      }
    }
  }
}

function defaultDisplay() {
  for (i = 0; i < robots.length; i++) {
    robots[i].display();
  }
  obstacle_job();
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
  constructor(pos, x2, y2, color, letter, scale) {
    this.pos = [pos];
    this.fill = color;
    this.letter = letter;
    this.canvasSpeedX = x2;
    this.canvasSpeedY = y2;
    this.offsetY = scale * 0.75;
    this.offsetX = scale * 0.15;
    this.size = scale;
  }

  display(opts) {
    prev = [];

    if (typeof opts === "undefined" || Object.entries(opts).length === 0) {
      // display dropoff
      this.pos.forEach((value, i) => {
        if (i > 0) {
          this.display_single(prev);
        }
        prev = value;
      });
      this.display_single(prev);
      return;
    }
    opts.forEach((value, i) => {
      if (i > 0) {
        this.display_single(prev);
      }
      prev = value;
    });

    strokeWeight(4);
    stroke(51);
    this.display_single(prev);
    noStroke();
  }

  display_single(opts) {
    let posX = opts[1] * this.canvasSpeedX;
    let posY = opts[0] * this.canvasSpeedY;


    fill(this.fill);
    rect(posX, posY, this.size, this.size);
    fill(0);
    strokeWeight(1);
    stroke(0);
    if (this.letter == "P") 
    {
      textSize(0.57*this.size);
      text(this.letter, posX + this.offsetX + 5, posY + this.offsetY);
    } else {
      textSize(0.25*this.size);
      text(this.letter, posX + this.offsetX - 6, posY + this.offsetY - 7);
    }
    noStroke();
  }

  addPoints(pos) {
    this.pos.push(pos);
  }
}

// Robot class
class Robot {
  constructor(id, pos, diam = 6, speed = 1, agent = false) {
    this.letter = id
    this.x = pos[0];
    this.y = pos[1];
    this.diameter = diam;
    this.dia_scale = -6
    this.speed = speed;
    this.agent = agent; // fill color; yellow if agent, white otherwise
  }

  move(y, x) {
    this.x = x * this.canvasSpeedX + this.diameter * 0.5;
    this.y = y * this.canvasSpeedY + this.diameter * 0.5;
  }

  setInterpolation(x, y) {
    this.canvasSpeedX = x * this.speed;
    this.canvasSpeedY = y * this.speed;
  }

  display() {
    if (this.agent) fill("#cc3853");
    else fill(155, 155, 155);
    // check if border has been reached and reset
    strokeWeight(2);
    stroke(51);
    ellipse(this.x, this.y, this.diameter + this.dia_scale, this.diameter + this.dia_scale);

    fill(0);
    textSize(0.70 * this.canvasSpeedX);
    text(this.letter, this.x - this.canvasSpeedX * 0.18, this.y + 12);
    noStroke();

  }

  getPosition() {
    return this.x + ", " + this.y;
  }
}

var slider = document.getElementById("myRange");
var output = document.getElementById("speed");
output.innerHTML = slider.value; // Display the default slider value
