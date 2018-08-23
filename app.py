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
from flask_socketio import send, SocketIO

from src.engine.Game import Game
from src.views.game_view import game_view

app = Flask(__name__)
app.register_blueprint(game_view, url_prefix='/play')
socketio = SocketIO(app)
game = Game()


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('message')
def handle_message(message):
    print('got %s' % message)
    if message == 'join':
        send(str(game.add_player()))


if __name__ == '__main__':
    socketio.run(app)
