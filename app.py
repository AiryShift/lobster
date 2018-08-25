#!/usr/bin/env python

# Copyright 2018 Julian Tu

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from engine import Game
from views.game_view import game_view

app = Flask(__name__)
app.register_blueprint(game_view, url_prefix='/play')
socketio = SocketIO(app)
game = Game()


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('join')
def handle_join():
    print('got join')
    return game.add_player()


@socketio.on('restart')
def handle_restart():
    global game
    print('got restart')
    game = Game()
    emit('restart_ack', broadcast=True)


@socketio.on('request_info')
def handle_request_info(player_id):
    print('got request_info for', player_id)
    return {
        'cash': game.get_cash(player_id),
        'boats': game.get_boats(player_id),
        'pots': game.get_pots(player_id),
        'day': game.day,
        'consecutive_bad': game.consecutive_bad,
        'yesterday_weather': game.yesterday_weather,
    }


@socketio.on('validate_strategy')
def handle_validate_strategy(player_id, inshore, offshore):
    return game.validate_strategy(player_id, inshore, offshore)


@socketio.on('submit_strategy')
def handle_submit_strategy(player_id, strategy):
    print('submitting {} for {}'.format(strategy, player_id))
    if 'hotel_work' in strategy:
        game.submit_hotel_strategy(player_id)
    else:
        game.submit_fish_strategy(player_id, strategy['inshore'], strategy['offshore'])


@socketio.on('next_turn')
def handle_next_turn():
    print('attempting to advance turn...')
    if game.ready_to_finish():
        game.finish_day()
        emit('next_turn_ack', broadcast=True)
        print('success')


@socketio.on('message')
def handle_message(message):
    print(message)


if __name__ == '__main__':
    socketio.run(app)
