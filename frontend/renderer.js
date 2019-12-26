// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// No Node.js APIs are available in this process because
// `nodeIntegration` is turned off. Use `preload.js` to
// selectively enable features needed in the rendering
// process.

var ctx1 = document.getElementById('stepsChart');
var stepsChart = new Chart(ctx1, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Steps',
            data: [12, 39, 40, 5, 2, 3, 0],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});

var ctx2 = document.getElementById('heartChart');
var heartChart = new Chart(ctx2, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Heart',
            data: [12, 39, 40, 5, 2, 3, 0],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});