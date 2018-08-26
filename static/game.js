var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', () => {
});

socket.on('message', (msg) => {
    console.log(msg);
});

socket.on('restart_ack', () => {
    console.log('restarting...');
    setInfo();
});

socket.on('next_turn_ack', () => {
    console.log('advancing turn');
    requestInfo();
});

function nextTurn() {
    socket.emit('next_turn');
}

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
        setInfo(window.player_id, info['cash'], info['boats'], info['pots'], info['day'], info['consecutive_bad'], info['yesterday_weather'], info['day_num']);
    });
}

function setInfo(player_id='-', cash=' -', boats='-', pots='-', day='Monday', consecutive_bad='0', yesterday_weather='Good', day_num='0') {
    window.player_id = player_id;
    document.getElementById('my_id').textContent = player_id;
    document.getElementById('my_cash').textContent = '$' + cash;
    document.getElementById('my_boats').textContent = boats;
    document.getElementById('my_pots').textContent = pots;
    document.getElementById('day_of_week').textContent = day;
    document.getElementById('consecutive_bad_weather').textContent = consecutive_bad;
    document.getElementById('yesterday_weather').textContent = yesterday_weather;
    document.getElementById('day_num').textContent = day_num;
}

function submit_strategy() {
    if (document.getElementById('fish_radio').checked) {
        var inshore = document.getElementById('inshore_input').value;
        var offshore = document.getElementById('offshore_input').value;
        socket.emit('validate_strategy', window.player_id, parseInt(inshore), parseInt(offshore), (valid) => {
            if (valid) {
                console.log('submitting inshore: ' + inshore + ' offshore: ' + offshore);
                socket.emit('submit_strategy', window.player_id, {
                    'inshore': parseInt(inshore),
                    'offshore': parseInt(offshore),
                });
            }
        });
    } else {
        socket.emit('submit_strategy', window.player_id, {'hotel_work': null});
    }
}

function enableFishing() {
    document.getElementById('inshore_input').disabled = false;
    document.getElementById('offshore_input').disabled = false;
}

function disableFishing() {
    document.getElementById('inshore_input').disabled = true;
    document.getElementById('offshore_input').disabled = true;
}
