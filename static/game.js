var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', () => {
});

socket.on('message', (msg) => {
    console.log(msg);
});

socket.on('restart_ack', () => {
    console.log('restarting...')
    setInfo();
});

function join() {
    socket.emit('join', (player_id) => {
        window.player_id = player_id;
        console.log('joined with id: ' + window.player_id);
        requestInfo();
    });
}

function resetGame() {
    socket.emit('restart');
}

function requestInfo() {
    socket.emit('request_info', window.player_id, (info) => {
        setInfo(window.player_id, info['cash'], info['boats'], info['pots'], info['day']);
    });
}

function setInfo(player_id='-', cash=' -', boats='-', pots='-', day='Monday') {
    window.player_id = player_id;
    document.getElementById('my_id').textContent = player_id;
    document.getElementById('my_cash').textContent = '$' + cash;
    document.getElementById('my_boats').textContent = boats;
    document.getElementById('my_pots').textContent = pots;
    document.getElementById('day_of_week').textContent = day;
}

function validate_strategy() {
    var inshore = document.getElementById('inshore_input').value;
    var offshore = document.getElementById('offshore_input').value;
    socket.emit('validate_strategy', window.player_id, parseInt(inshore), parseInt(offshore), (valid) => {
        console.log(valid);
        if (valid) {
            console.log('validated inshore: ' + inshore + ' offshore: ' + offshore);
        }
    });
}
