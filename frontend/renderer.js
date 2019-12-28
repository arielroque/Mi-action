// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// No Node.js APIs are available in this process because
// `nodeIntegration` is turned off. Use `preload.js` to
// selectively enable features needed in the rendering
// process.



// Functions

dropdownClick = () => {

    //Remove old elements

    var elements = document.getElementsByClassName("dropdown-item");

    while (elements[0]) {
        elements[0].parentNode.removeChild(elements[0]);
    }

    // Refresh elements

    for (let i = 0; i < 10; i++) {
        let dropItem = document.createElement("button");
        dropItem.className = "dropdown-item";
        dropItem.type = "button";
        dropItem.innerHTML = "oi";
        dropItem.id = "di" + i;
        dropItem.onclick = ()=>{
            alert("opaaaa");
        }
        document.getElementById("dropdown-bluetooth").appendChild(dropItem);
    }
}

dropdownSelectItem = (e) => {
    console.log(e);
}

// Chart Config

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

// Trigger Listenings 

document.getElementById("dropdownMenuLink").addEventListener("click", dropdownClick);
//document.getElementsByClassName("dropdown-item").addEventListener("click", dropdownSelectItem);