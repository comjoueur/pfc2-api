
var controllerSocket = null;

function performWebSocket() {
    var token = document.getElementById("token").value;
    controllerSocket = new WebSocket(
        'ws://'
         + window.location.host
         + '/controller_action/'
    );
    controllerSocket.onopen = () => {
        controllerSocket.send('token:' + token);
    }
}
