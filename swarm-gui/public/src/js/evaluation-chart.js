// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily =
  '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = "#292b2c";

function createStatistics(payload) {
  // Area Chart Example
  var ctx = document.getElementById("myAreaChart");
  var myLineChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          label: "Points",
          lineTension: 0.3,
          backgroundColor: "rgba(2,117,216,0.2)",
          borderColor: "rgba(2,117,216,1)",
          pointRadius: 5,
          pointBackgroundColor: "rgba(2,117,216,1)",
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
              maxTicksLimit: 5
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
      addData(myLineChart, payload[key].episode, payload[key].acc_rewards);
    }
  }
}

function addData(chart, label, data) {
  chart.data.labels.push(label);
  chart.data.datasets.forEach(dataset => {
    dataset.data.push(data);
  });
  chart.update();
}

function removeData(chart) {
  chart.data.labels.pop();
  chart.data.datasets.forEach(dataset => {
    dataset.data.pop();
  });
  chart.update();
}
