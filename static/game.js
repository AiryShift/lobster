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
    setInfo(window.player_id, info['cash'], info['boats'], info['pots'], info['day']);
});

function join() {
    socket.emit('join');
}

function resetGame() {
    socket.emit('restart');
    setInfo();
}

function requestInfo() {
    socket.emit('request_info', window.player_id);
}

function setInfo(player_id='-', cash=' -', boats='-', pots='-', day='Monday') {
    document.getElementById('my_id').textContent = player_id;
    document.getElementById('my_cash').textContent = '$' + cash;
    document.getElementById('my_boats').textContent = boats;
    document.getElementById('my_pots').textContent = pots;
    document.getElementById('day_of_week').textContent = day;
}
