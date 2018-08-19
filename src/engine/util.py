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


import enum

POTS_PER_BOAT = 6
GOOD_IN = 3
GOOD_OFF = 5
BAD_IN = 5
BAD_OFF = -6


class Weather(enum.Enum):
    GOOD = enum.auto()
    BAD = enum.auto()


@enum.unique
class Day(enum.IntEnum):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6


def next_day(day):
    return (day + 1) % len(list(Day))


class Strategy:
    def __init__(self, inshore, offshore):
        self.inshore = inshore
        self.offshore = offshore

    @property
    def total(self):
        return self.inshore + self.offshore


def profit(strategy, weather):
    if weather is Weather.GOOD:
        return strategy.inshore * GOOD_IN + strategy.offshore * GOOD_OFF
    else:
        return strategy.inshore * BAD_IN + strategy.offshore * BAD_OFF
