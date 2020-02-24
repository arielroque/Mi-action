// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// No Node.js APIs are available in this process because
// `nodeIntegration` is turned off. Use `preload.js` to
// selectively enable features needed in the rendering
// process.



//Initial State

let device = document.getElementById("device-card");
device.style.display = "none";

// Variables

let isDropdownActive = false;


// Functions

connectDevice = (url) => {
    document.getElementById("dropdown-devices").innerHTML = "Connecting";

    handleConnectDevice(url, (err, data) => {
        if (err != null) {
            document.getElementById("dropdown-devices").innerHTML = "Disconnected";
            //put toaster to notify
            console.error(err);
        } else {
            let response = (JSON.parse(data)).Authentication;
            if (response == "True") {
                document.getElementById("dropdown-devices").innerHTML = "Connected";

                getInitialData();
            }
            else {
                document.getElementById("dropdown-devices").innerHTML = "Disconnected";
            }
        }
    });

}

deviceContainerVisibility = () => {

    let device = document.getElementById("device-card");
    if (device.style.display === "none") {
        device.style.display = "block";
    }
    else {
        device.style.display = "none";
    }
}

handleDisconnectDevice = (url, callback) => {
    let request = new XMLHttpRequest();

    request.open("DELETE", url, true);
    request.onload = () => {
        let status = request.status;
        if (status == 200) {
            callback(null, request.response);
        } else {
            callback(status);
        }
    }
    request.send(null);
}

handleConnectDevice = (url, callback) => {
    let request = new XMLHttpRequest();
    request.open("POST", url, true);
    request.onload = () => {
        let status = request.status;

        if (status == 200) {
            callback(null, request.response);
        } else {
            callback(status);
        }
    }
    request.send(null);
}



getBluetoothDevices = (url, callback) => {
    let request = new XMLHttpRequest();
    request.open("GET", url, true);
    request.onload = () => {
        let status = request.status;

        if (status == 200) {
            callback(null, request.response);
        } else {
            callback(status);
        }
    }
    request.send(null);
}


handleSteps = (callback) => {
    let request = new XMLHttpRequest();
    request.open("GET", "http://127.0.0.1:5000/steps", true);
    request.onload = () => {
        let status = request.status;

        if (status == 200) {
            callback(null, request.response);
        } else {
            callback(status);
        }
    }
    request.send(null);

}

getSteps = () => {
    document.getElementById("steps").innerHTML = "Getting Data";
    handleSteps((err, data) => {
        if (err != null) {
            console.error(err);
        } else {
            let steps = (JSON.parse(data)).Steps;
            let meters = (JSON.parse(data)).Meters;
            document.getElementById("steps").innerHTML = steps;
        }
    });
}

handleHeartRate = (callback) => {
    let request = new XMLHttpRequest();
    request.open("GET", "http://127.0.0.1:5000/heart", true);
    request.onload = () => {
        let status = request.status;

        if (status == 200) {
            callback(null, request.response);
        } else {
            callback(status);
        }
    }
    request.send(null);
}

getHeartRate = () => {
    document.getElementById("heart-rate").innerHTML = "Getting Data";
    handleHeartRate((err, data) => {
        if (err != null) {
            console.error(err);
        } else {
            console.log(JSON.parse(data));
            let heartRate = (JSON.parse(data)).HeartRate;
            document.getElementById("heart-rate").innerHTML = heartRate;
        }
    });

}

getInitialData = () => {

    document.getElementById("steps").innerHTML = "Getting";
    document.getElementById("heart-rate").innerHTML = "Getting";

    handleSteps((err, data) => {
        if (err != null) {
            console.error(err);
        } else {
            let steps = (JSON.parse(data)).Steps;
            let meters = (JSON.parse(data)).Meters;
            document.getElementById("steps").innerHTML = steps;

            handleHeartRate((err, data) => {
                if (err != null) {
                    console.error(err);
                } else {
                    console.log(JSON.parse(data));
                    let heartRate = (JSON.parse(data)).HeartRate;
                    document.getElementById("heart-rate").innerHTML = heartRate;
                }
            });

        }
    });

}

dropdownClick = () => {
    dropdownStatus = document.getElementById("dropdown-devices").innerHTML;
    console.log(dropdownStatus);

    if (isDropdownActive) {
        isDropdownActive = false;
        if (dropdownStatus == "Searching") {
            document.getElementById("dropdown-devices").innerHTML = "Disconnected";
        }
    }
    else {
        isDropdownActive = true;
        if (dropdownStatus == "Disconnected") {
            document.getElementById("dropdown-devices").innerHTML = "Searching";
        }

    }
    // Refresh elements

    getBluetoothDevices("http://127.0.0.1:5000/devices", (err, data) => {

        //Remove old elements

        var elements = document.getElementsByClassName("dropdown-item");

        while (elements[0]) {
            elements[0].parentNode.removeChild(elements[0]);
        }

        if (err != null) {
            console.error("Check Bluetooth Connection");
        } else {
            var devices = (JSON.parse(data).Devices);
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


            let dropStatus = document.getElementById("dropdown-devices").innerHTML;

            console.log(dropStatus);

            if (dropStatus == "Connected") {

                let dividerDiv = document.createElement("div");
                dividerDiv.className = "dropdown-divider";
                document.getElementById("dropdown-bluetooth").appendChild(dividerDiv);

                let dropItemDisconnect = document.createElement("button");
                dropItemDisconnect.className = "dropdown-item";
                dropItemDisconnect.type = "button";
                dropItemDisconnect.innerHTML = "Disconnect";
                dropItemDisconnect.id = "disconnectBtn";
                dropItemDisconnect.onclick = () => {

                    handleDisconnectDevice("http://127.0.0.1:5000/auth", (err, data) => {
                        if (err != null) {
                            //put toaster to notify
                            console.error(err);
                        } else {
                            let response = (JSON.parse(data)).Authentication;
                            if (response == "True") {
                                document.getElementById("dropdown-devices").innerHTML = "Connected";
                            }
                            else {
                                document.getElementById("dropdown-devices").innerHTML = "Disconnected";
                            }
                        }
                    });

                }
                document.getElementById("dropdown-bluetooth").appendChild(dropItemDisconnect);
            }


        }
    });
}

// Chart Config

var ctx1 = document.getElementById('stepsChart');
var stepsChart = new Chart(ctx1, {
    type: 'line',
    data: {
        labels: ["15/04", "1600", "1700", "1750", "1800", "1850", "1900", "1950", "1999", "2050"],
        datasets: [{
            data: [86, 114, 106, 106, 107, 111, 133, 221, 783, 2478],
            label: "Steps",
            backgroundColor: 'rgb(230,185,51)'
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
            backgroundColor: 'rgb(211,79,92)',
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
document.getElementById("btn-steps").addEventListener("click", getSteps);
document.getElementById("btn-heart").addEventListener("click", getHeartRate);