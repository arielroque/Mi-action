// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// No Node.js APIs are available in this process because
// `nodeIntegration` is turned off. Use `preload.js` to
// selectively enable features needed in the rendering
// process.


// Functions


connectDevice = (url) => {
    let request = new XMLHttpRequest();
    request.open("POST", url, false);
    request.send(null);

    let response = (JSON.parse(request.responseText)).Authentication;
    if (response == "True") {
        console.log("Connected");
        document.getElementById("dropdown-devices").innerHTML = "Connected";
    }

    else {
        console.log("Ocorreu um erro");
        document.getElementById("dropdown-devices").innerHTML = "Desconnected";
        alert("Failed to connect to device")
    }
}

getBluetoothDevices = (theUrl) => {
    let request = new XMLHttpRequest();
    request.open("GET", theUrl, false);
    request.send(null);

    var devices = (JSON.parse(request.responseText).Devices);
    console.log(devices);
    console.log(devices[0].address);
    console.log(devices.lenght);

    for (let i = 0; i < devices.length; i++) {
        let dropItem = document.createElement("button");
        dropItem.className = "dropdown-item";
        dropItem.type = "button";
        dropItem.innerHTML = devices[i].name;
        dropItem.id = "di" + i;
        dropItem.onclick = () => {
            document.getElementById("dropdown-devices").innerHTML = "Connecting...";
            connectDevice("http://127.0.0.1:5000/auth/" + devices[i].address);

        }
        document.getElementById("dropdown-bluetooth").appendChild(dropItem);
    }


    console.log(request.responseText);
}


dropdownClick = () => {


    document.getElementById("dropdown-devices").innerHTML = "Searching";

    //Remove old elements

    var elements = document.getElementsByClassName("dropdown-item");

    while (elements[0]) {
        elements[0].parentNode.removeChild(elements[0]);
    }

    // Refresh elements

    getBluetoothDevices("http://127.0.0.1:5000/devices");
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

document.getElementById("dropdown-devices").addEventListener("click", dropdownClick);
//document.getElementsByClassName("dropdown-item").addEventListener("click", dropdownSelectItem);