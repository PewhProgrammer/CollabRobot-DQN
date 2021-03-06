// prettify ALT + SHIFT + F

let episode = 0;
let move = 0;
let max_games_per_episode = 0;
let game_epoch = 1;
let pickups = [];
let dropoffs = [];
let data = [];
let board = [[]];
let completion_rate = 0
let sensor = false
let double_dqn = false
let dueling_dqn = false
let prioritized_dqn = false
let reward_function = "none"

let stop = false;

function setup() {
  // Creating canvas
  cv = createCanvas(canvas_width, canvas_height);
  cv.parent("sketch-holder");
  cv.background(50, 89, 100);

  document.getElementById("log-file").onchange = function () {
    const file = this.files[0];
    reset_game();

    // display file name on input field
    $(`#log-file-label`).html(file.name);

    var navigator = new FileNavigator(file);

    let countLines = 0;

    let table = $("<tbody>");

    // === Reading all lines ===
    var indexToStartWith = 0;
    navigator.readSomeLines(indexToStartWith, function linesReadHandler(
      err,
      index,
      lines,
      isEof,
      progress
    ) {
      // Error happened
      if (err) throw err;

      // Reading lines
      for (var i = 0; i < lines.length; i++) {
        const line = lines[i];
        // Do something with line

        if (line != "") {
          // console.log(lines[line])
          let payload = JSON.parse(line);
          // data a new table row

          if (payload.hasOwnProperty('episode')) {
            let tr = $("<tr>");
            tr.append($("<th>").text(`${payload.episode.substr(1)}`));
            tr.append($("<th>").text(`${payload.width}x${payload.height}`));
            tr.append(
              $("<th>").text(
                `${Object.keys(payload.start_locations.agents).length}`
              )
            );
            tr.append($("<th>").text(`${Object.keys(payload.games).length}`));
            tr.append($("<th>").text(`${payload.acc_rewards}`));
            tr.append($("<th>").text(`${payload.completed}`));
            table.append(tr);

            data.push(payload);
          } else {
            completion_rate = payload.completion;
            collided_rate = payload.collided;
            sensor = payload.sensor_information
            dueling_dqn = payload.dueling
            double_dqn = payload["double-dqn"]
            prioritized_dqn = payload.prioritized
            reward_function = payload.reward
          }
        }
      }

      countLines += lines.length;

      // progress is a position of the last read line as % from whole file length

      // End of file
      if (isEof) {

        createStatistics(data);

        init_new_grid(data[0]);

        $("#dataTable").append(table);


        $("#dataTable").DataTable();


        $("#dataTable tbody").on("click", "tr", function (e) {
          episode = $(this)
            .children("th:first")
            .text();
          move = 0;
          init_new_grid(data[episode]);
          e.stopPropagation();
        });
        return;
      }

      // Reading next chunk, adding number of lines read to first line in current chunk
      navigator.readSomeLines(index + lines.length, linesReadHandler);
    });
  };

  document.getElementById("map-file").onchange = function () {
    const file = this.files[0];
    const reader = new FileReader();
    // display file name on input field
    $(`#map-file-label`).html(file.name);

    reader.onload = function (progressEvent) {
      // By lines
      var lines = this.result.split("\n");
      for (let line = 0; line < lines.length; line++) {
        str = lines[line];

        board[line] = str.split("");
      }

      // display everything
      $(".data-ready")
        .css("visibility", "visible")
        .hide()
        .fadeIn("slow");
    };
    reader.readAsText(file);
  };

  frameRate(1);

  // Update the current slider value (each time you drag the slider handle)
  slider.oninput = function () {
    output.innerHTML = this.value;
    setFrameRate(parseInt(this.value));
  };

  $("#stop").click(function () {
    stop = !stop;
    if (stop) {
      $("#prev").prop("disabled", false);
      $("#next").prop("disabled", false);
      noLoop();
      $(".fa-stop")
        .removeClass("fa fa-play")
        .addClass("fa-play");
    } else {
      $("#prev").attr("disabled", true);
      $("#next").attr("disabled", true);
      loop();
      $(".fa-play")
        .removeClass("fa fa-play")
        .addClass("fa-stop");
    }
  });

  $("#prev").click(function () {
    move = move - 2 < 0 ? 0 : move - 2;
    redraw();
  });
}

function reset_game() {
  episode = 0;
  move = 0;
  max_games_per_episode = 0;
  game_epoch = 1;
  pickups = [];
  dropoffs = [];
  data = [];
  completion_rate = 0
  collided_rate = 0
  sensor = false
  double_dqn = false
  dueling_dqn = false
  prioritized_dqn = false
  reward_function = "none"
}

function draw() {
  // if(!run) return

  background(0, 102, 102);
  fill(255);
  strokeWeight(2);
  stroke(155, 155, 155);
  //displayLine();

  // TODO: parse the commands

  const c = get_Command();
  if (typeof c == "undefined") {
    // defaultDisplay(); // display current environment
    return;
  }

  // update
  obstacle_job(board, adjustedX, adjustedY);

  noStroke()
  objective_job(c.locations.pickup);
  agent_job(c.locations.agents);
}

function get_Command() {
  if (episode >= Object.keys(data).length) {
    return;
  }

  const episode_container = data[episode];

  try {
    return JSON.parse(episode_container.games[move]);
  } finally {
    move++;
    if (Object.keys(episode_container.games).length <= move) {
      move = 0;
      episode++;
      init_new_grid(data[episode]);
    }
  }
}

function init_new_grid(board) {
  map_width = board.width;
  map_height = board.height;
  agents = board.agents;

  ratio = map_height / map_width;
  canvas_height = canvas_width * ratio

  cv = createCanvas(canvas_width, canvas_height);
  cv.parent("sketch-holder");

  adjustedX = canvas_width * (1 / map_width);
  adjustedY = canvas_height * (1 / map_height);

  create_objectives(board.start_locations);
  create_agents(board.start_locations.agents);

  var x = document.getElementsByClassName("episode")[0];
  x.innerHTML = `Episode: ${board.episode}`;

  x = document.getElementsByClassName("reward")[0];
  x.innerHTML = `Episode Reward: ${Math.round(board.acc_rewards * 100) / 100}`;

  var x = document.getElementsByClassName("completion")[0];
  x.innerHTML = `Completion Rate: ${Math.round(completion_rate * 100) / 100}`;

  var x = document.getElementsByClassName("collided")[0];
  x.innerHTML = `Collision Rate: ${Math.round(collided_rate * 100) / 100}`;

  var x = document.getElementsByClassName("sensor")[0];
  x.innerHTML = `Sensor Information: ${sensor}`;

  var x = document.getElementsByClassName("reward_function")[0];
  x.innerHTML = `R-Function: ${reward_function}`;

  var x = document.getElementsByClassName("ddp")[0];
  x.innerHTML = `double/dueling/prioritized: ${double_dqn}/${dueling_dqn}/${prioritized_dqn}`;


}

function create_objectives(board) {
  pickups = [];
  dropoffs = [];
  let amount_objectives = board.dropoff.length / 2
  while(amount_objectives > 0){
    const _idx$ = amount_objectives * 2

    dropoffs.push(fill_objective(board.dropoff.slice(_idx$ - 2, _idx$), "#c3bcc3", "DZONE", adjustedX));
    pickups.push(fill_objective(board.pickup.slice(_idx$ - 2, _idx$), "#CC6600", "P", adjustedX));
    amount_objectives--;
  }
}

function fill_objective(pos, fill, letter, size) {
  return new Target(pos, adjustedX, adjustedY, fill, letter, size)
}

function create_agents(agents) {
  for (var key in agents) {
    if (agents.hasOwnProperty(key)) {
      pos = agents[key];
      agent = key == 0 ? true : false;
      robot = new Robot(key, pos, adjustedX, 1, agent);
      robot.setInterpolation(adjustedX, adjustedY);
      robots.push(robot);
    }
  }
}
