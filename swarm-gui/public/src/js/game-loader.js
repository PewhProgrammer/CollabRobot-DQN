// prettify ALT + SHIFT + F

let episode = 0;
let move = 0;
let max_games_per_episode = 0;
let game_epoch = 1;
let pickup = null;
let dropoff = null;
const data = [];

let stop = false

function setup() {
  // Creating canvas
  cv = createCanvas(canvas_width + 100, canvas_height + 100);
  cv.parent("sketch-holder");
  cv.background(50, 89, 100);

  document.getElementById("file").onchange = function() {
    const file = this.files[0];
    const reader = new FileReader();

    reader.onload = function(progressEvent) {
      console.log(file);
      // display file name on input field
      $(`.custom-file-label`).html(file.name);

      // construct data Table
      let table = $("<tbody>");

      // By lines
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
      }

      createStatistics(data);

      init_new_grid(data[0])

      $("#dataTable").append(table);

      $(".data-ready")
        .css("visibility", "visible")
        .hide()
        .fadeIn("slow");

      $("#dataTable").DataTable();

      $("tr").click(function(e){     //function_td
        // console.log($(this).index());
        episode = $(this).index()
        move = 0 
        init_new_grid(data[episode]);
        e.stopPropagation();
      });

    };
    reader.readAsText(file);
  };

  frameRate(1);

  // Update the current slider value (each time you drag the slider handle)
  slider.oninput = function() {
    output.innerHTML = this.value;
    setFrameRate(parseInt(this.value));
  };

  $("#stop").click(function(){
    stop = !stop;
    if(stop){
      $('#prev').prop('disabled', false);	
      $('#next').prop('disabled', false);
      noLoop()
      $('.fa-stop').removeClass('fa fa-play').addClass('fa-play')
    } else {
      $("#prev").attr("disabled", true);	
      $("#next").attr("disabled", true);	
      loop()
      $('.fa-play').removeClass('fa fa-play').addClass('fa-stop')
    }

  }); 

  $("#prev").click(function(){
    move = move - 2 < 0 ? 0 : move - 2 ;
    redraw()
  }); 

}

function draw() {
  // if(!run) return

  background(50, 89, 100);
  fill(255);
  //displayLine();

  // TODO: parse the commands

  const c = get_Command();
  if (typeof c == "undefined") {
    // defaultDisplay(); // display current environment
    return;
  }

  // update
  agent_job(c.locations.agents);
  objective_job(c.locations.pickup);
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
    if (Object.keys(episode_container.games).length <= move + 1) {
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
  x.innerHTML = `Reward: ${board.acc_rewards}`;
}

function create_objectives(board) {
  // assign objectives
  pickup = new Target(
    board.pickup[0] * adjustedX,
    board.pickup[1] * adjustedY,
    "#CC6600",
    "P"
  );
  dropoff = new Target(
    board.dropoff[0] * adjustedX,
    board.dropoff[1] * adjustedY,
    "#993300",
    "D"
  );

  pickup.setInterpolation(adjustedX, adjustedY);
}

function create_agents(agents) {
  for (var key in agents) {
    if (agents.hasOwnProperty(key)) {
      pos = agents[key];
      agent = key == 0 ? true : false;
      robot = new Robot(pos[0], pos[1], 20, 1, agent);
      robot.setInterpolation(adjustedX, adjustedY);
      robots.push(robot);
    }
  }
}
