#!/usr/bin/env python3

# pylint doesn't fully support dataclasses yet, https://github.com/PyCQA/pylint/issues/2605
# pylint: disable=E1101,E1136,E1133,E1137

import argparse

from dataclasses import dataclass, field
from typing import List
from typing import Dict


@dataclass
class Colour:
    '''RGB colour'''
    red: int
    green: int
    blue: int


@dataclass
class Point:
    '''Point with (x,y) coordinates'''
    x: int
    y: int


@dataclass
class Pixel:
    '''Materialise a pixel within a sprite'''
    point: Point
    colour: Colour


@dataclass
class Sprite:
    pixels: List[Pixel]


@dataclass
class AnimatedSprite:
    sprite: Sprite
    topleft: Point

    def move(self, horizontal: int, vertical: int):
       self.topleft.x += horizontal
       self.topleft.y += vertical

    def move_left(self):
        self.move(-1, 0)

    def move_right(self):
        self.move(1, 0)

    def move_up(self):
        self.move(0, -1)

    def move_down(self):
        self.move(0, 1)


@dataclass
class VirtualDisplay:
    sprites: List[AnimatedSprite]

    def add_sprite(self, sprite: Sprite):
        self.sprites.append(sprite)

    def animate(self):
        for sprite in self.sprites:
            sprite.move_left()


@dataclass
class Key:
    key: str


@dataclass
class PhysicalDisplay:
    lights: Dict[Key, Colour] = field(default_factory=dict)


@dataclass
class View:
    virtual_display: VirtualDisplay

    def __post_init__(self):
        self.last_drawn = PhysicalDisplay()

    def animate(self):
        self.virtual_display.animate()

    def update_view(self):
        # Clear the keyboard

        # Convert virtual to physical display

        # Convert to commands

        # Execute commands

        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Keyboard animations')
    args = parser.parse_args()

    p = Pixel(Point(0, 0), Colour(0xff, 0xbb, 0x99))
    s = Sprite([p])
    a = AnimatedSprite(s, Point(1, 1))
    d = VirtualDisplay([])
    d.add_sprite(a)
    v = View(d)

    print(f"{v}")
    v.animate()
    print(f"{v}")
