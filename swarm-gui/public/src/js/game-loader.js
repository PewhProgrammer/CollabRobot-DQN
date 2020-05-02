// prettify ALT + SHIFT + F

let episode = 0;
let move = 0;
let max_games_per_episode = 0;
let game_epoch = 1;
let pickups = [];
let dropoffs = [];
const data = [];
let board = [[]];

let stop = false;

function setup() {
  // Creating canvas
  cv = createCanvas(canvas_width, canvas_height);
  cv.parent("sketch-holder");
  cv.background(50, 89, 100);

  document.getElementById("log-file").onchange = function() {
    const file = this.files[0];
    const reader = new FileReader();

    var CHUNK_SIZE = 1024;
    var offset = 0;

    // display file name on input field
    $(`#log-file-label`).html(file.name);

    var navigator = new LineNavigator(file);

    let indexToStartWith = 0;

    let countLines = 0;

    navigator.readSomeLines(indexToStartWith, function linesReadHandler(
      err,
      index,
      lines,
      isEof,
      progress
    ) {
      countLines += lines.length;

      // End of file
      if (isEof) {
        console.log(countLines);
        return;
      }

      // Reading next chunk, adding number of lines read to first line in current chunk
      navigator.readSomeLines(index + lines.length, linesReadHandler);
    });

    reader.onload = function(progressEvent) {
      // construct data Table
      // let table = $("<tbody>");

      var view = new Uint8Array(reader.result);
      for (var i = 0; i < view.length; ++i) {
        if (view[i] === 10 || view[i] === 13) {
          // \n = 10 and \r = 13
          // column length = offset + position of \r or \n
          callback(offset + i);
          return;
        }
      }

      // \r or \n not found, continue seeking.
      offset += CHUNK_SIZE;
      seek();

      /* // By lines
      var lines = this.result.split("\n");
      for (var line = 0; line < lines.length; line++) {
        str = lines[line];
        // console.log(str);

        if (str != "") {
          // console.log(lines[line])
          let payload = JSON.parse(lines[line]);
          // data a new table row
          // table.append($("<tr>"));
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
          tr.append($("<th>").text("Yes"));
          table.append(tr);

          data.push(payload);
        }
      } */

      /*
      createStatistics(data);

      init_new_grid(data[0]);

      $("#dataTable").append(table);

      $("#dataTable").DataTable();

      $("#dataTable tbody").on("click", "tr", function(e) {
        episode = $(this)
          .children("th:first")
          .text();
        move = 0;
        init_new_grid(data[episode]);
        e.stopPropagation();
      });
      */
    };
<<<<<<< HEAD

    reader.onerror = function() {
      // Cannot read file... Do something, e.g. assume column size = 0.
      callback(0);
    };
    // seek();

    function seek() {
      if (offset >= file.size) {
        // No \r or \n found. The column size is equal to the full
        // file size
        callback(file.size);
        return;
      }
      var slice = file.slice(offset, offset + CHUNK_SIZE);
      reader.readAsArrayBuffer(slice);
    }

    // reader.readAsText(file);
=======
    reader.readAsText(file);
    //reader.readAsArrayBuffer(file)
>>>>>>> 59f8e705ca6bacd054bdf3aea9f92a01b13dd1ae
  };

  document.getElementById("map-file").onchange = function() {
    const file = this.files[0];
    const reader = new FileReader();
    // display file name on input field
    $(`#map-file-label`).html(file.name);

    reader.onload = function(progressEvent) {
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
  slider.oninput = function() {
    output.innerHTML = this.value;
    setFrameRate(parseInt(this.value));
  };

  $("#stop").click(function() {
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

  $("#prev").click(function() {
    move = move - 2 < 0 ? 0 : move - 2;
    redraw();
  });
}

function draw() {
  // if(!run) return

  background(0, 102, 102);
  fill(255);
  //displayLine();

  // TODO: parse the commands

  const c = get_Command();
  if (typeof c == "undefined") {
    // defaultDisplay(); // display current environment
    return;
  }

  // update
  obstacle_job(board, adjustedX, adjustedY);
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
      init_new_grid(episode_container);
    }
  }
}

function init_new_grid(board) {
  map_width = board.width;
  map_height = board.height;
  agents = board.agents;

  adjustedX = canvas_width * (1 / map_width);
  adjustedY = canvas_height * (1 / map_height);

  create_objectives(board.start_locations);
  create_agents(board.start_locations.agents);

  var x = document.getElementsByClassName("episode")[0];
  x.innerHTML = `Episode: ${board.episode}`;

  x = document.getElementsByClassName("reward")[0];
  x.innerHTML = `Reward: ${board.acc_rewards[0]}`;
}

function create_objectives(board) {
  pickups.push(fill_objective(board.pickup, "#CC6600", "P"));
  dropoffs.push(fill_objective(board.dropoff, "#3CB371", "D"));
}

function fill_objective(target_single, fill, letter) {
  t = null;
  target = [target_single];

  target.forEach(function(value, i) {
    if (i == 0) {
      t = new Target(value, adjustedX, adjustedY, fill, letter);
    } else {
      t.addPoints(value);
    }
  });

  return t;
}

function create_agents(agents) {
  for (var key in agents) {
    if (agents.hasOwnProperty(key)) {
      pos = agents[key];
      agent = key == 0 ? true : false;
      robot = new Robot(pos, 20, 1, agent);
      robot.setInterpolation(adjustedX, adjustedY);
      robots.push(robot);
    }
  }
}
