#!/usr/bin/env python3

# pylint doesn't fully support dataclasses yet, https://github.com/PyCQA/pylint/issues/2605
# pylint: disable=E1101,E1136,E1133,E1137

# TODO: when a sprite goes off screen, make it wrap

import argparse
import time

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

    def render(self, top_left: Point): # -> Sprite: (dnw?!)
        rendered = Sprite([])
        for pixel in self.pixels:
            new_pixel = Pixel(pixel.point.x + top_left.x,
                                pixel.point.y + top_left.y)
            rendered.pixels.append(new_pixel)
        return rendered


@dataclass
class AnimatedSprite:
    sprite: Sprite
    top_left: Point

    def move(self, horizontal: int, vertical: int):
       self.top_left.x += horizontal
       self.top_left.y += vertical

    def move_left(self):
        self.move(-1, 0)

    def move_right(self):
        self.move(1, 0)

    def move_up(self):
        self.move(0, -1)

    def move_down(self):
        self.move(0, 1)

    def render(self) -> Sprite:
        return self.sprite.render(self.top_left)


@dataclass
class VirtualDisplay:
    animated_sprites: List[AnimatedSprite]

    def __post_init__(self):
        self.rendered = List[Sprite]

    def add_sprite(self, animated_sprite: AnimatedSprite):
        self.animated_sprites.append(animated_sprite)

    def animate(self):
        self.rendered = []
        for animated_sprite in self.animated_sprites:
            animated_sprite.move_left()
            self.rendered.append(animated_sprite.render())


@dataclass
class Key:
    key: str


@dataclass
class PhysicalDisplay:
    lights: Dict[Key, Colour] = field(default_factory=dict)


@dataclass
class View:
    virtual_display: VirtualDisplay
    refresh_interval: float = 0.1

    def __post_init__(self):
        self.last_drawn = PhysicalDisplay()

    def animate(self):
        self.virtual_display.animate()

    def update_view(self):
        # Clear the keyboard

        # Render the sprites

        # Convert virtual to physical display
        print(f"{v}")

        # Convert to commands

        # Execute commands

        pass

    def run(self):
        while True:
            self.animate()
            self.update_view()
            time.sleep(self.refresh_interval)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Keyboard animations')
    args = parser.parse_args()

    p = Pixel(Point(0, 0), Colour(0xff, 0xbb, 0x99))
    s = Sprite([p])
    a = AnimatedSprite(s, Point(1, 1))
    d = VirtualDisplay([])
    d.add_sprite(a)
    v = View(d)
    v.run()
