// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily =
  '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = "#292b2c";

function createStatistics(payload) {
  // Area Chart Example
  var ctx = document.getElementById("myAreaChart");
  var myLineChart = new Chart(ctx, {
    type: "scatter",
    data: {
      labels: ["Completed", "Not Completed"],
      datasets: [
        {
          label: "Points",
          lineTension: 0.3,
          backgroundColor: "rgba(2,216,25,0.2)",
          borderColor: "rgba(2,117,216,1)",
          pointRadius: 5,
          pointBackgroundColor: "rgba(2,217,26,1)",
          pointBorderColor: "rgba(255,255,255,0.8)",
          pointHoverRadius: 5,
          pointHoverBackgroundColor: "rgba(2,117,216,1)",
          pointHitRadius: 50,
          pointBorderWidth: 2,
          data: []
        },
        {
          label: "Points",
          lineTension: 0.3,
          backgroundColor: "rgba(215,12,21,0.2)",
          borderColor: "rgba(2,117,216,1)",
          pointRadius: 5,
          pointBackgroundColor: "rgba(224,17,21,1)",
          pointBorderColor: "rgba(255,255,255,0.8)",
          pointHoverRadius: 5,
          pointHoverBackgroundColor: "rgba(2,117,216,1)",
          pointHitRadius: 50,
          pointBorderWidth: 2,
          data: []
        }
      ]
    },
    options: {
      scales: {
        xAxes: [
          {
            gridLines: {
              display: false
            },
            ticks: {
              maxTicksLimit: 7
            }
          }
        ],
        yAxes: [
          {
            ticks: {
              maxTicksLimit: 5,
              beginAtZero: true
            },
            gridLines: {
              color: "rgba(0, 0, 0, .125)"
            }
          }
        ]
      },
      legend: {
        display: false
      }
    }
  });

  for (var key in payload) {
    if (payload.hasOwnProperty(key)) {
      addData(myLineChart, payload[key].episode, payload[key].acc_rewards, payload[key].completed);
    }
  }
}

function addData(chart, label, data, completed) {
  // updateConfigByMutating(chart, completed)
  point = {x:parseInt(label.substr(1)), y:data}
  
  if (completed){
    chart.data.labels.push(label);
    chart.data.datasets[0].data.push(point);
  } else {
    chart.data.labels.push(label);
    chart.data.datasets[1].data.push(point);
  }

  chart.update();
}

function updateConfigByMutating(chart, completed) {
  if (completed) chart.data.datasets.pointBackgroundColor = "rgba(0,255,0,1)";
  else chart.options.title.text = "rgba(255,0,0,1)";

  console.log(chart.data.datasets)
  
  chart.update();
}

function removeData(chart) {
  chart.data.labels.pop();
  chart.data.datasets.forEach(dataset => {
    dataset.data.pop();
  });
  chart.update();
}
