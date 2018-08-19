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

import util
import random
from Player import Player
from util import Day, next_day, Strategy, Weather


UPKEEP_PER_BOAT = 50


def profit(player, strategy, weather):
    assert strategy.total == player.boats * POTS_PER_BOAT
    return util.profit(strategy, weather)


class Game:
    def __init__(self, num_players):
        self.day = Day.MON
        self.weather = None  # initialised at the end of the first day
        self.players = [Player(i) for i in range(num_players)]
        self.consecutive_bad = 0

    def finish_day():
        self.day = next_day(self.day)
        if self.day is Day.SAT:
            for player in self.players:
                player.cash -= 30 + player.boats * UPKEEP_PER_BOAT

    def update_weather(self):
        roll = random.randint(1, 6)
        if roll == 1:
            self.weather = Weather.BAD
            self.consecutive_bad += 1
        elif roll == 2 and self.consecutive_bad > 0:
            self.weather = Weather.BAD
            self.consecutive_bad += 1
        else:
            self.weather = Weather.GOOD
            self.consecutive_bad = 0
