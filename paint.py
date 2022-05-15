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

    def __hash__(self):
        return hash(repr(self))

@dataclass
class KeyColours:
    '''List of key-colour mappings'''
    lights: Dict[Key, Colour] = field(default_factory=dict)

    def add(self, key, colour):
        lights[key] = colour

    def render(self):
        c = 'echo -e "'
        c += 'a 000000\\n'
        for keyColour in self.lights.items():
            #print(key, colour)
            if key is None:
                continue
            c += f'k {key.key} {colour.rgb_hex()}\\n'
        c += 'c\\n'
        c += '" | g810-led -pp'
        #c += '" | cat'
        print(c)
        subprocess.call(c, shell=True)
        time.sleep(.3)

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
    KeyColours.add(Key("fkeys"), Colour(0xff, 0x00, 0x00)),
    KeyColours.add(Key("keys"), Colour(0xff, 0xff, 0xff)),
    KeyColours.add(Key("modifiers"), Colour(0x00, 0xff, 0x00)),
    
    KeyColours.render()