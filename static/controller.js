
var width = 0;

document.addEventListener('DOMContentLoaded', function (event) {
  if (! /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
    document.body.innerHTML = "<div>You need a mobile device to test this functionality!</div>";
    alert("You need a mobile device to test this functionality!");
  }
  else {
    alert("Please use horizontal orientation");
  }
})

var controllerSocket = null;
var ready = false;

window.onbeforeunload = function (evt) {
  controllerSocket.close()
  return null;
};

function performWebSocket() {
  var token = document.getElementById("token").value;
  controllerSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/controller_action/'
  );
  controllerSocket.onopen = () => {
    controllerSocket.send('token:' + token);
    var x = document.getElementById("input-token");
    x.style.display = "none";
    var controls = document.getElementById("controls");
    controls.style.display = "block";
    ready = true;
  }
}

function showCoordinates(event, button_id) {
  var x = event.touches[0].clientX;
  var y = event.touches[0].clientY;
  if (ready) {
    console.log('touch:' + x + ':' + y + ':' + button_id);
    controllerSocket.send('touch:' + x + ':' + y + ':' + button_id);
  }
}

function turnLeft() {
  if (controllerSocket.readyState === WebSocket.OPEN) {
    controllerSocket.send('action:LEFT');
  }
}

function turnRight() {
  if (controllerSocket.readyState === WebSocket.OPEN) {
    controllerSocket.send('action:RIGHT');
  }
}

function turnUp() {
  if (controllerSocket.readyState === WebSocket.OPEN) {
    controllerSocket.send('action:UP');
  }
}

function turnDown() {
  if (controllerSocket.readyState === WebSocket.OPEN) {
    controllerSocket.send('action:DOWN');
  }
}

function pause() {
  if (controllerSocket.readyState === WebSocket.OPEN) {
    controllerSocket.send('action:PAUSE');
  }
}

function start() {
  if (controllerSocket.readyState === WebSocket.OPEN) {
    controllerSocket.send('action:START');
  }
}
