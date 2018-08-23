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
        return HOTEL_WAGE

    if weather is Weather.GOOD:
        return strategy.inshore * GOOD_IN + strategy.offshore * GOOD_OFF
    else:
        return strategy.inshore * BAD_IN + strategy.offshore * BAD_OFF


class Game:
    def __init__(self, num_players=0):
        self.day = Day.MON
        self.weather = None  # initialised at the end of the first day
        self.players = {i: Player() for i in range(num_players)}
        self.strategies = {}
        self.consecutive_bad = 0

    @property
    def num_players(self):
        return len(self.players)

    def add_player(self):
        new_id = len(self.players)
        self.players[new_id] = Player()
        return new_id

    def get_player(self, player_id):
        return self.players[player_id]

    def submit_strategy(self, player_id, inshore, offshore, hotel=False):
        if player_id not in self.players:
            return False

        player = self.get_player(player_id)
        if hotel:
            self.strategies[player_id] = HOTEL_WORK
        else:
            strategy = Strategy(inshore, offshore)
            if not validate(player, strategy):
                return False
            self.strategies[player_id] = strategy

        return True

    def num_strategies(self):
        return len(self.strategies)

    def buy_boat(self, player_id):
        if player_id not in self.players:
            return False
        player = self.get_player(player_id)

        if player.cash < BOAT_COST:
            return False

        player.cash -= 1
        player.boats += 1
        return True

    def sell_boat(self, player_id):
        if player_id not in self.players:
            return False
        player = self.get_player(player_id)

        if player.boats == 1:
            return False

        player.boats -= 1
        player.cash += BOAT_RESALE
        return True

    def finish_day(self):
        if self.num_strategies() != self.num_players:
            return False

        self.update_weather()
        if self.day is Day.SUN:
            for player in self.players.values():
                if player.cash < 0:
                    player.cash = round(player.cash * (1 + INTEREST_CHARGED))
                player.cash -= 30 + player.boats * UPKEEP_PER_BOAT

        if self.consecutive_bad == HURRICANE_PERIOD:
            for player in self.players.values():
                player.boats = 1
                player.cash -= BOAT_COST
        else:
            for player in self.players.values():
                player.cash += profit(player,
                                      self.strategies[player], self.weather)

        self.day = next_day(self.day)
        self.strategies = {}
        return True

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
