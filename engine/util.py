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


class Weather(enum.Enum):
    GOOD = enum.auto()
    BAD = enum.auto()


@enum.unique
class Day(enum.Enum):
    MON = 'Monday'
    TUE = 'Tuesday'
    WED = 'Wednesday'
    THU = 'Thursday'
    FRI = 'Friday'
    SAT = 'Saturday'
    SUN = 'Sunday'

    def __str__(self):
        return self.value


def next_day(day):
    if day is Day.MON:
        return Day.TUE
    elif day is Day.TUE:
        return DAY.WED
    elif day is Day.WED:
        return Day.THU
    elif day is Day.THU:
        return Day.FRI
    elif day is Day.FRI:
        return Day.SAT
    elif day is Day.SAT:
        return Day.SUN
    return Day.MON


class Strategy:
    def __init__(self, inshore, offshore):
        self.inshore = inshore
        self.offshore = offshore

    @property
    def total(self):
        return self.inshore + self.offshore


HOTEL_WORK = Strategy(0, 0)
