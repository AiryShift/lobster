var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', () => {
});

socket.on('message', (msg) => {
    console.log(msg);
});

socket.on('join_ack', (data) => {
    window.player_id = data['id'];
    console.log('joined with id: ' + window.player_id);
    requestInfo();
});

socket.on('restart_ack', () => {
    console.log('restarting...')
});

socket.on('request_info_ack', (info) => {
    console.log('cash: ' + info['cash']);
    console.log('boats: ' + info['boats']);
});

function join() {
    socket.emit('join');
}

function resetGame() {
    socket.emit('restart');
}

function requestInfo() {
    socket.emit('request_info', window.player_id);
}
