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

import os

import mistune
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from engine import Game
from views.game_view import game_view

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
app = Flask(__name__)
app.register_blueprint(game_view, url_prefix='/play')
socketio = SocketIO(app)
game = Game()


@app.route('/')
def index():
    with open(os.path.join(SITE_ROOT, 'static', 'index.md')) as f:
        body_text = mistune.markdown(f.read(), escape=False)
    return render_template('index.html', body_text=body_text)


@socketio.on('get_unused_id')
def handle_get_unused_id():
    return game.get_unused_player_id()


@socketio.on('join')
def handle_join(player_id):
    app.logger.info('got join for ' + player_id)
    game.add_player(player_id)
    emit('should_update', broadcast=True)


@socketio.on('exit')
def handle_exit(player_id):
    game.delete_player(player_id)
    emit('should_update', broadcast=True)


@socketio.on('restart')
def handle_restart():
    global game
    app.logger.info('got restart')
    game = Game()
    emit('restart_ack', broadcast=True)


@socketio.on('request_info')
def handle_request_info(player_id):
    app.logger.info('got request_info for: {}'.format(player_id))
    return {
        'cash': game.get_cash(player_id),
        'boats': game.get_boats(player_id),
        'pots': game.get_pots(player_id),
        'day': game.day,
        'consecutive_bad': game.consecutive_bad,
        'yesterday_weather': game.yesterday_weather,
        'day_num': game.day_num,
    }


@socketio.on('request_ranking')
def handle_request_ranking():
    ranking = []
    for player_id in game.player_ids:
        ranking.append({
            'id': player_id,
            'cash': game.get_cash(player_id),
            'submitted': game.did_submit(player_id),
        })
    ranking.sort(key=lambda rank: int(rank['cash']), reverse=True)

    # assign a ranking with ties
    previous_cash = float('inf')
    rank = 0
    for entry in ranking:
        if entry['cash'] != previous_cash:
            rank += 1
        entry['rank'] = rank
        previous_cash = entry['cash']
    return ranking


@socketio.on('buy_boat')
def handle_buy_boat(player_id):
    if not game.buy_boat(player_id):
        return game.cash_needed_for_boat(player_id)
    game.delete_strategy(player_id)
    return 0


@socketio.on('sell_boat')
def handle_sell_boat(player_id):
    # deletes the strategy if the sell is successful
    return game.sell_boat(player_id) and game.delete_strategy(player_id)


@socketio.on('submit_strategy')
def handle_submit_strategy(player_id, strategy):
    app.logger.info('submitting {} for {}'.format(strategy, player_id))
    if 'hotel_work' in strategy:
        ret = game.submit_hotel_strategy(player_id)
    else:
        ret = game.submit_fish_strategy(player_id,
                                        strategy['inshore'],
                                        strategy['offshore'])
    if ret:
        emit('should_update', broadcast=True)
    return ret


@socketio.on('next_turn')
def handle_next_turn():
    app.logger.info('attempting to advance turn...')
    if game.ready_to_finish():
        game.finish_day()
        emit('next_turn_ack', broadcast=True)
        app.logger.info('success')


@socketio.on('message')
def handle_message(message):
    app.logger.info(message)


if __name__ == '__main__':
    socketio.run(app)
