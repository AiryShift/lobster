// Copyright 2018 Julian Tu

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//     http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', () => {
    updateData();
});

socket.on('message', (msg) => {
    console.log(msg);
});

socket.on('should_update', () => {
    updateData();
})

socket.on('restart_ack', () => {
    console.log('restarting...');
    window.player_id = null;
    updateData();
});

socket.on('next_turn_ack', () => {
    console.log('advancing turn');
    updateData();
});

function nextTurn() {
    socket.emit('next_turn');
}

function join() {
    socket.emit('get_unused_id', (unused) => {
        bootbox.prompt({
            title: 'Join with which ID?',
            size: 'small',
            value: unused,
            callback: (player_id) => {
                if (player_id !== null) {
                    socket.emit('join', player_id);
                    window.player_id = player_id;
                    console.log('joined with id: ' + player_id);
                    updateData();
                }
            },
        });
    });
}

function exit() {
    if (window.player_id !== null) {
        bootbox.confirm({
            message: 'Are you sure?',
            buttons: { confirm: { label: "Yes", }, cancel: { label: "No", }, },
            callback: (result) => {
                if (result) {
                    socket.emit('exit', window.player_id);
                    window.player_id = null;
                    updateData();
                }
            },
        });
    }
}

function resetGame() {
    bootbox.confirm({
        message: 'Are you sure?',
        buttons: { confirm: { label: "Yes", }, cancel: { label: "No", }, },
        callback: (result) => {
            if (result) {
                socket.emit('restart');
            }
        }
    });
}

function updateData() {
    socket.emit('request_info', window.player_id, (info) => {
        setInfo(window.player_id, info['cash'], info['boats'], info['pots'], info['day'], info['consecutive_bad'], info['yesterday_weather'], info['day_num']);
    });
    socket.emit('request_ranking', (ranking) => {
        var ranking_body = document.getElementById('ranking_tbody');
        ranking_body.innerHTML = '';
        for (var i = 0; i < ranking.length; i++) {
            var row = ranking_body.appendChild(document.createElement('tr'));
            row.appendChild(document.createElement('td')).textContent = ranking[i]['rank'];
            row.appendChild(document.createElement('td')).textContent = ranking[i]['id'];
            row.appendChild(document.createElement('td')).textContent = ranking[i]['cash'];
            row.appendChild(document.createElement('td')).textContent = ranking[i]['submitted'] ? '✓' : '✗';
        }
    });
}

function setInfo(player_id = '-', cash = ' -', boats = '-', pots = '-', day = 'Monday', consecutive_bad = '0', yesterday_weather = 'Good', day_num = '0') {
    document.getElementById('my_id').textContent = player_id;
    document.getElementById('my_cash').textContent = '$' + cash;
    document.getElementById('my_boats').textContent = boats;
    document.getElementById('my_pots').textContent = pots;
    document.getElementById('day_of_week').textContent = day;
    document.getElementById('consecutive_bad_weather').textContent = consecutive_bad;
    document.getElementById('yesterday_weather').textContent = yesterday_weather;
    document.getElementById('day_num').textContent = day_num;
}

function buyBoat() {
    bootbox.confirm({
        message: 'Are you sure that you want to buy a boat?',
        buttons: { confirm: { label: "Yes", }, cancel: { label: "No", }, },
        callback: (result) => {
            if (result) {
                socket.emit('buy_boat', window.player_id, (money_missing) => {
                    if (money_missing > 0) {
                        bootbox.alert({
                            message: 'Missing $' + money_missing.toString() + ' cash.',
                            backdrop: true,
                            size: 'small',
                        });
                    } else {
                        updateData();
                    }
                });
            }
        },
    });
}

function sellBoat() {
    bootbox.confirm({
        message: 'Are you sure that you want to sell your boat?',
        buttons: { confirm: { label: "Yes", }, cancel: { label: "No", }, },
        callback: (result) => {
            if (result) {
                socket.emit('sell_boat', window.player_id, (success) => {
                    if (!success) {
                        bootbox.alert({
                            message: 'Cannot sell your last boat',
                            backdrop: true,
                            size: 'small',
                        });
                    } else {
                        updateData();
                    }
                });
            }
        },
    });
}

function submit_strategy() {
    var inshore = document.getElementById('inshore_input').value;
    var offshore = document.getElementById('offshore_input').value;
    var strategy;
    if (document.getElementById('fish_radio').checked) {
        strategy = { inshore: parseInt(inshore), offshore: parseInt(offshore) };
    } else {
        strategy = { hotel_work: null };
    }

    socket.emit('submit_strategy', window.player_id, strategy, (valid) => {
        if (valid) {
            console.log('submitting inshore: ' + inshore + ' offshore: ' + offshore);
        } else {
            bootbox.alert({
                message: 'Invalid fishing allocation.',
                backdrop: true,
                size: 'small',
            });
        }
    });
}

function enableFishing() {
    document.getElementById('inshore_input').disabled = false;
    document.getElementById('offshore_input').disabled = false;
}

function disableFishing() {
    document.getElementById('inshore_input').disabled = true;
    document.getElementById('offshore_input').disabled = true;
}
