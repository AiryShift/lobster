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

from .Player import Player
from .util import HOTEL_WORK, Day, Strategy, Weather, next_day

ID_LENGTH = 40

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


def is_hurricane(consecutive_bad):
    return consecutive_bad == HURRICANE_PERIOD


class Game:
    def __init__(self, num_players=0):
        self.day_num = 0
        self._day = Day.MON
        self.weather = Weather.GOOD
        self.players = {str(i): Player() for i in range(num_players)}
        self.strategies = {}
        self.consecutive_bad = 0

    @property
    def day(self):
        return str(self._day)

    @property
    def yesterday_weather(self):
        return str(self.weather)

    @property
    def num_players(self):
        return len(self.players)

    @property
    def player_ids(self):
        return self.players.keys()

    def get_unused_player_id(self):
        test = random.getrandbits(ID_LENGTH)
        while test in self.players:
            test = random.getrandbits(ID_LENGTH)
        return str(test)

    def add_player(self, player_id):
        if player_id not in self.players:
            self.players[player_id] = Player()

    def delete_player(self, player_id):
        # this always succeeds, don't KeyError
        self.players.pop(player_id, None)
        self.strategies.pop(player_id, None)

    def get_player(self, player_id):
        return self.players[player_id] if player_id in self.players else Player(0, 0)

    def get_cash(self, player_id):
        return str(self.get_player(player_id).cash)

    def get_boats(self, player_id):
        return str(self.get_player(player_id).boats)

    def get_pots(self, player_id):
        return str(self.get_player(player_id).boats * POTS_PER_BOAT)

    def validate_strategy(self, player_id, inshore, offshore):
        return validate(self.get_player(player_id), Strategy(inshore, offshore))

    def submit_fish_strategy(self, player_id, inshore, offshore):
        if player_id not in self.players:
            return False

        player = self.get_player(player_id)
        strategy = Strategy(inshore, offshore)
        if not validate(player, strategy):
            return False
        self.strategies[player_id] = strategy
        return True

    def submit_hotel_strategy(self, player_id):
        if player_id not in self.players:
            return False

        player = self.get_player(player_id)
        self.strategies[player_id] = HOTEL_WORK
        return True

    def delete_strategy(self, player_id):
        # don't raise KeyError, this always succeeds
        return bool(self.strategies.pop(player_id, True))

    def did_submit(self, player_id):
        return player_id in self.strategies

    def num_strategies(self):
        return len(self.strategies)

    def cash_needed_for_boat(self, player_id):
        return max(BOAT_COST - self.get_player(player_id).cash, 0)

    def buy_boat(self, player_id):
        if player_id not in self.players:
            return False
        player = self.get_player(player_id)

        if player.cash < BOAT_COST:
            return False

        player.boats += 1
        player.cash -= BOAT_COST
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

    def ready_to_finish(self):
        return self.num_strategies() == self.num_players

    def finish_day(self):
        if self.num_strategies() != self.num_players:
            return False

        self.update_weather()
        if self._day is Day.SUN:
            for player in self.players.values():
                if player.cash < 0:
                    player.cash = round(player.cash * (1 + INTEREST_CHARGED))
                player.cash -= 30 + player.boats * UPKEEP_PER_BOAT

        if is_hurricane(self.consecutive_bad):
            for player in self.players.values():
                while player.boats > 1:
                    player.boats -= 1
                    player.cash -= BOAT_COST
        else:
            for player_id, player in self.players.items():
                player.cash += profit(player,
                                      self.strategies[player_id],
                                      self.weather)

        self._day = next_day(self._day)
        self.strategies = {}
        self.day_num += 1

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
