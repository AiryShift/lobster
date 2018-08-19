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

import random
from Player import Player
from util import Day, next_day, HOTEL_WORK, Strategy, Weather


POTS_PER_BOAT = 6

BOAT_COST = 150
BOAT_RESALE = BOAT_COST // 2
UPKEEP_PER_BOAT = 50
GOOD_IN = 3
GOOD_OFF = 5
BAD_IN = 5
BAD_OFF = -6
INTEREST_CHARGED = 0.1
HOTEL_WAGE = 15
HURRICANE_PERIOD = 3


def validate(player, strategy):
    return strategy is HOTEL_WORK or strategy.total == player.boats * POTS_PER_BOAT


def profit(player, strategy, weather):
    assert validate(player, strategy)

    if strategy is HOTEL_WORK:
        return HOTEL_WAGE + (max(player.cash, 0) * (1 + INTEREST_CHARGED))

    if weather is Weather.GOOD:
        return strategy.inshore * GOOD_IN + strategy.offshore * GOOD_OFF
    else:
        return strategy.inshore * BAD_IN + strategy.offshore * BAD_OFF


class Game:
    def __init__(self, num_players):
        self.day = Day.MON
        self.weather = None  # initialised at the end of the first day
        self.players = {i: Player() for i in range(num_players)}
        self.strategies = {}
        self.consecutive_bad = 0

    def submit_strategy(self, player, inshore, offshore, hotel=False):
        if player not in self.players:
            return False

        if hotel:
            self.strategies[player] = HOTEL_WORK
        else:
            strategy = Strategy(inshore, offshore)
            if not validate(player, strategy):
                return False
            self.strategies[player] = strategy

        return True

    def finish_day(self):
        self.update_weather()
        if self.day is Day.SUN:
            for player in self.players:
                if player.cash < 0:
                    player.cash = round(player.cash * (1 + INTEREST_CHARGED))
                player.cash -= 30 + player.boats * UPKEEP_PER_BOAT

        if consecutive_bad == HURRICANE_PERIOD:
            for player in self.players:
                player.boats = 1
                player.cash -= BOAT_COST
        else:
            for player in self.players:
                player.cash += profit(player, self.strategies[player], self.weather)

        self.day = next_day(self.day)
        self.strategies = {}

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
