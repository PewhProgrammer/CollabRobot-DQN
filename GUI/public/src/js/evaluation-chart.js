// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily =
  '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = "#292b2c";

let loaded = false
let myLineChart

function createStatistics(payload) {
  // Area Chart Example

  if (loaded) {
    myLineChart.destroy();
  }
  loaded = true
  // resetCanvas("chart", "chart-container")
  const ctx = document.getElementById("chart");
  myLineChart = new Chart(ctx, {
    type: "scatter",
    data: {
      labels: ["Completed", "Not Completed"],
      datasets: [
        {
          label: "Completed",
          lineTension: 0.3,
          backgroundColor: "rgba(2,217,26,1)",
          pointRadius: 5,
          pointBackgroundColor: "rgba(2,217,26,1)",
          pointBorderColor: "rgba(255,255,255,0.8)",
          pointHoverRadius: 5,
          pointHoverBackgroundColor: "rgba(2,117,216,1)",
          pointHitRadius: 5,
          pointBorderWidth: 2,
          fontColor: 'black',
          data: []
        },
        {
          label: "Pickup",
          lineTension: 0.3,
          pointRadius: 5,
          pointBackgroundColor: "#CC6600",
          pointBorderColor: "rgba(255,255,255,0.8)",
          pointHoverRadius: 5,
          pointHoverBackgroundColor: "rgba(2,117,216,1)",
          pointHitRadius: 5,
          pointBorderWidth: 2,
          fontColor: 'black',
          pointStyle: 'rect',
          data: []
        },
        {
          label: "Not Completed",
          lineTension: 0.3,
          pointRadius: 5,
          pointBackgroundColor: "rgba(224,1,1,1)",
          pointBorderColor: "rgba(255,255,255,0.8)",
          pointHoverRadius: 5,
          pointHoverBackgroundColor: "rgba(2,117,216,1)",
          pointHitRadius: 5,
          pointBorderWidth: 2,
          pointStyle: 'rectRot',  
          data: []
        }
      ]
    },
    options: {
      scales: {
        xAxes: [
          {
            display: true,
            scaleLabel: {
              display: true,
              labelString: 'Episodes',
              fontSize: 14
            },
            gridLines: {
              display: false
            },
            ticks: {
              minTicksLimit: 5,
              maxTicksLimit: 7
            }
          }
        ],
        yAxes: [
          {
            display: true,
            scaleLabel: {
              display: true,
              labelString: 'Rewards',
              fontSize: 14
            },
            ticks: {
              maxTicksLimit: 7,
              beginAtZero: true
            },
            gridLines: {
              color: "rgba(0, 0, 0, .125)"
            }
          }
        ]
      },
      legend: {
        display: true,
        labels: {
          usePointStyle: true,
          fontColor: 'rgb(0, 0, 0)',
          fontSize: 14
        }
      }
    }
  });


  for (var key in payload) {
    if (payload.hasOwnProperty(key)) {
      pickup = false
      if (payload[key].hasOwnProperty("picked_up")) {
        pickup = payload[key].picked_up[0];
      }
      addData(myLineChart, payload[key].episode, payload[key].acc_rewards, payload[key].completed, pickup);
    }
  }
}

function addData(chart, label, data, completed, pickup) {
  // updateConfigByMutating(chart, completed)
  point = { x: parseInt(label.substr(1)), y: data }

  if (completed) {
    chart.data.labels.push(label);
    chart.data.datasets[0].data.push(point);
  } else if (pickup) {
    chart.data.labels.push(label);
    chart.data.datasets[1].data.push(point);
  } else {
    chart.data.labels.push(label);
    chart.data.datasets[2].data.push(point);
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
