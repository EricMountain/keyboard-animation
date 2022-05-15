#!/usr/bin/env python3

# pylint doesn't fully support dataclasses yet, https://github.com/PyCQA/pylint/issues/2605
# pylint: disable=E1101,E1136,E1133,E1137

import argparse
import time
import subprocess

from dataclasses import dataclass, field
from typing import List
from typing import Dict
from typing import ClassVar

@dataclass
class Colour:
    '''RGB colour'''
    red: int
    green: int
    blue: int

    def __hash__(self):
        return hash(repr(self))

    def rgb_hex(self):
        return f'{self.red:02x}{self.green:02x}{self.blue:02x}'

@dataclass
class Key:
    key: str
    isGroup: False

    def __hash__(self):
        return hash(repr(self))


@dataclass
class KeyColours:
    '''List of key-colour mappings'''
    lights: Dict[Key, Colour] = field(default_factory=dict)

    def add(self, key, colour):
        self.lights[key] = colour

    def render(self):
        c = 'echo -e "'
        c += 'a 000000\\n'
        for key, colour in self.lights.items():
            #print(key, colour)
            if key is None:
                continue
            if key.isGroup:
                c += 'g '
            else:
                c += 'k '
            c += f'{key.key} {colour.rgb_hex()}\\n'
        c += 'c\\n'
        c += '" | g810-led -pp'
        #c += '" | cat'
        print(c)
        subprocess.call(c, shell=True)
        # time.sleep(.3)

# Available keys: (run `g810-led --help-keys` to see all possibilities including groups)
#
# a-z, 0-9
# tilde, minus, equal, semicolon, quote, dollar(?), slash, comma, period, intl_backslash
# backspace, insert, home
# tab, page_up, page_down, or pg_down (or both?)? 
# escape, print_screen, scroll_lock, pause_break, caps_lock
# F1-F12
# open_bracket, close_bracket
# enter
# shift_left, shift_right, ctrl_left, ctrl_right, win_left, win_right, alt_left, alt_right
# insert, del
# num_0, …, num_9, num_lock, num_slash, asterisk, num_minus, num_plus, num_enter, num_dot
# arrow_up, arrow_down, arrow_right, arrow_left
# space
# fn??

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Keyboard animations')
    args = parser.parse_args()

    keyColours = KeyColours()
    
    # This example uses key groups
    keyColours.add(Key("space", False), Colour(0xff, 0x00, 0x00)),
    keyColours.add(Key("keys", True), Colour(0xff, 0xff, 0xff)),
    keyColours.add(Key("modifiers", True), Colour(0x00, 0xff, 0x00)),

    keyColours.render()

    # Sample animation
    prevKey = 0
    currKey = 1
    direction = 1
    refresh_interval = .3
    while True:
        keyColours2 = KeyColours()

        if i != 0:
            # Turn off the previous key
            keyColours2.add(Key(f'F{prevKey}', False), Colour(0x00, 0x00, 0x00))
            prevKey = currKey

        keyColours2.add(Key(f'F{currKey}', False), Colour(0xdd, 0x00, 0x00))
        
        if currKey == 12:
            direction = -1
        elif currKey == 1 and direction == -1:
            direction = 1
        currKey += direction

        keyColours.render()
        time.sleep(refresh_interval)
