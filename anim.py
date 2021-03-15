#!/usr/bin/env python3

# pylint doesn't fully support dataclasses yet, https://github.com/PyCQA/pylint/issues/2605
# pylint: disable=E1101,E1136,E1133,E1137

# TODO: when a sprite goes off screen, make it wrap

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
class Point:
    '''Point with (x,y) coordinates'''
    x: int
    y: int

    def __hash__(self):
        return hash(repr(self))


@dataclass
class Pixel:
    '''Materialise a pixel within a sprite'''
    point: Point
    colour: Colour

    def __hash__(self):
        return hash(repr(self))


@dataclass
class Key:
    key: str

    def __hash__(self):
        return hash(repr(self))


@dataclass
class Sprite:
    pixels: List[Pixel]

    def translate(self, top_left: Point): # -> Sprite: (dnw?!)
        translated = Sprite([])
        for pixel in self.pixels:
            new_pixel = Pixel(Point(pixel.point.x + top_left.x,
                              pixel.point.y + top_left.y),
                              pixel.colour)
            translated.pixels.append(new_pixel)
        return translated


@dataclass
class PixelMapper:
    def __post_init__(self):
        self.map = {
            Point(0, 0): Key("escape"), Point(1, 0): None,
            Point(2, 0): Key("F1"), Point(3, 0): Key("F2"),
            Point(4, 0): Key("F3"), Point(5, 0): Key("F4"),
            Point(6, 0): None, Point(7, 0): Key("F5"),
            Point(8, 0): Key("F6"), Point(9, 0): Key("F7"),
            Point(10, 0): Key("F8"), Point(11, 0): None,
            Point(12, 0): Key("F9"), Point(13, 0): Key("F10"),
            Point(14, 0): Key("F11"), Point(15, 0): Key("F12"),
            Point(16, 0): None, Point(17, 0): Key("print_screen"),
            Point(18, 0): Key("scroll_lock"), Point(19, 0): Key("pause_break"),
            Point(20, 0): None, Point(21, 0): None,
            Point(22, 0): None, Point(23, 0): None,
            Point(24, 0): None,

            Point(0, 1): Key("tilde"), Point(1, 1): Key("1"),
            Point(2, 1): Key("2"), Point(3, 1): Key("3"),
            Point(4, 1): Key("4"), Point(5, 1): Key("5"),
            Point(6, 1): Key("6"), Point(7, 1): None,
            Point(8, 1): Key("7"), Point(9, 1): Key("8"),
            Point(10, 1): Key("9"), Point(11, 1): Key("0"),
            Point(12, 1): Key("minus"), Point(13, 1): Key("equal"),
            Point(14, 1): Key("backspace"), Point(15, 1): Key("backspace"),
            Point(16, 1): None, Point(17, 1): Key("insert"),
            Point(18, 1): Key("home"), Point(19, 1): Key("page_up"),
            Point(20, 1): None, Point(21, 1): Key("num_lock"),
            Point(22, 1): Key("num_slash"), Point(23, 1): Key("asterisk"),
            Point(24, 1): Key("num_minus"),

            Point(0, 2): Key("tab"), Point(1, 2): Key("tab"),
            Point(2, 2): Key("q"), Point(3, 2): Key("w"),
            Point(4, 2): Key("e"), Point(5, 2): Key("r"),
            Point(6, 2): Key("t"), Point(7, 2): Key("y"),
            Point(8, 2): Key("u"), Point(9, 2): Key("i"),
            Point(10, 2): Key("o"), Point(11, 2): Key("p"),
            Point(12, 2): Key("open_bracket"), Point(13, 2): Key("close_bracket"),
            Point(14, 2): Key("enter"), Point(15, 2): Key("enter"),
            Point(16, 2): None, Point(17, 2): Key("del"),
            Point(18, 2): Key("end"), Point(19, 2): Key("pg_down"),
            Point(20, 2): None, Point(21, 2): Key("num_7"),
            Point(22, 2): Key("num_8"), Point(23, 2): Key("num_9"),
            Point(24, 2): Key("num_plus"),

            Point(0, 3): Key("caps_lock"), Point(1, 3): Key("caps_lock"),
            Point(2, 3): Key("a"), Point(3, 3): Key("s"),
            Point(4, 3): Key("d"), Point(5, 3): Key("f"),
            Point(6, 3): Key("g"), Point(7, 3): Key("h"),
            Point(8, 3): Key("j"), Point(9, 3): Key("k"),
            Point(10, 3): Key("l"), Point(11, 3): Key("semicolon"),
            Point(12, 3): Key("quote"), Point(13, 3): Key("dollar"), # <- need to figure this key
            Point(14, 3): Key("enter"), Point(15, 3): Key("enter"),
            Point(16, 3): None, Point(17, 3): None,
            Point(18, 3): None, Point(19, 3): None,
            Point(20, 3): None, Point(21, 3): Key("num_4"),
            Point(22, 3): Key("num_5"), Point(23, 3): Key("num_6"),
            Point(24, 3): Key("num_plus"),

            Point(0, 4): Key("shift_left"), Point(1, 4): Key("intl_backslash"),
            Point(2, 4): Key("z"), Point(3, 4): Key("x"),
            Point(4, 4): Key("c"), Point(5, 4): Key("c"),
            Point(6, 4): Key("v"), Point(7, 4): Key("b"),
            Point(8, 4): Key("n"), Point(9, 4): Key("m"),
            Point(10, 4): Key("comma"), Point(11, 4): Key("period"),
            Point(12, 4): Key("slash"), Point(13, 4): Key("shift_right"),
            Point(14, 4): Key("shift_right"), Point(15, 4): Key("shift_right"),
            Point(16, 4): None, Point(17, 4): None,
            Point(18, 4): Key("arrow_up"), Point(19, 4): None,
            Point(20, 4): None, Point(21, 4): Key("num_1"),
            Point(22, 4): Key("num_2"), Point(23, 4): Key("num_3"),
            Point(24, 4): Key("num_enter"),

            Point(0, 5): Key("ctrl_left"), Point(1, 5): Key("ctrl_left"),
            Point(2, 5): Key("win_left"), Point(3, 5): Key("alt_left"),
            Point(4, 5): Key("space"), Point(5, 5): Key("space"),
            Point(6, 5): Key("space"), Point(7, 5): Key("space"),
            Point(8, 5): Key("space"), Point(9, 5): Key("space"),
            Point(10, 5): Key("alt_right"), Point(11, 5): Key("alt_right"),
            Point(12, 5): Key("<<<fn key>>>"), Point(13, 5): Key("win_right"), # <- can the fn key be controlled?
            Point(14, 5): Key("ctrl_right"), Point(15, 5): Key("ctrl_right"),
            Point(16, 5): None, Point(17, 5): Key("arrow_left"),
            Point(18, 5): Key("arrow_down"), Point(19, 5): Key("arrow_right"),
            Point(20, 5): None, Point(21, 5): Key("num_0"),
            Point(22, 5): Key("num_0"), Point(23, 5): Key("num_dot"),
            Point(24, 5): Key("num_enter")
        }

    def translate(self, point: Point) -> Key:
        if point in self.map:
            return self.map[point]
        else:
            return None


@dataclass
class PhysicalDisplay:
    width: int = 20
    height: int = 6
    lights: Dict[Key, Colour] = field(default_factory=dict)
    pixel_mapper: PixelMapper = PixelMapper()

    def add_sprite(self, sprite: Sprite):
        for pixel in sprite.pixels:
            point = pixel.point
            visible_point = Point(point.x % self.width, point.y % self.height)
            self.lights[self.pixel_mapper.translate(visible_point)] = pixel.colour
        
    def to_keyboard(self):
        c = 'echo -e "'
        c += 'a 000000\\n'
        for key, colour in self.lights.items():
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

    def translate(self) -> Sprite:
        return self.sprite.translate(self.top_left)


@dataclass
class VirtualDisplay:
    animated_sprites: List[AnimatedSprite]

    def __post_init__(self):
        self.rendered = List[Sprite]
        self.pixel_mapper = PixelMapper()

    def add_sprite(self, animated_sprite: AnimatedSprite):
        self.animated_sprites.append(animated_sprite)

    def animate(self):
        for animated_sprite in self.animated_sprites:
            animated_sprite.move_right()

    def render(self, physical_display: PhysicalDisplay):
        for sprite in self.animated_sprites:
            translated_sprite = sprite.translate()
            physical_display.add_sprite(translated_sprite)


@dataclass
class View:
    virtual_display: VirtualDisplay
    refresh_interval: float = 0.1

    def __post_init__(self):
        self.last_drawn = PhysicalDisplay()

    def animate(self):
        self.virtual_display.animate()

    def update_view(self):
        physical_display = PhysicalDisplay()
        self.virtual_display.render(physical_display)
        physical_display.to_keyboard()

    def run(self):
        while True:
            self.update_view()
            time.sleep(self.refresh_interval)
            self.animate()

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Keyboard animations')
    args = parser.parse_args()

    p = [
            Pixel(Point(0, 0), Colour(0xff, 0xa5, 0x00)),
            Pixel(Point(4, 0), Colour(0xff, 0xa5, 0x00)),
            Pixel(Point(5, 0), Colour(0xff, 0xa5, 0x00)),
            Pixel(Point(6, 0), Colour(0xff, 0xa5, 0x00)),
            Pixel(Point(0, 1), Colour(0xff, 0xa5, 0x00)),
            Pixel(Point(1, 1), Colour(0xff, 0xa5, 0x00)),
            Pixel(Point(3, 1), Colour(0xff, 0xa5, 0x00)),
            Pixel(Point(6, 1), Colour(0x41, 0x69, 0xe1)),
            Pixel(Point(7, 1), Colour(0xff, 0xa5, 0x00)),
            Pixel(Point(1, 2), Colour(0xff, 0xa5, 0x00)),
            Pixel(Point(2, 2), Colour(0xff, 0xa5, 0x00)),
            Pixel(Point(6, 2), Colour(0xff, 0xa5, 0x00)),
            Pixel(Point(7, 2), Colour(0xff, 0xa5, 0x00)),
            Pixel(Point(0, 3), Colour(0xff, 0xa5, 0x00)),
            Pixel(Point(1, 3), Colour(0xff, 0xa5, 0x00)),
            Pixel(Point(3, 3), Colour(0xff, 0xa5, 0x00)),
            Pixel(Point(5, 3), Colour(0xff, 0xa5, 0x00)),
            Pixel(Point(6, 3), Colour(0xff, 0xa5, 0x00)),
            Pixel(Point(0, 4), Colour(0xff, 0xa5, 0x00)),
            Pixel(Point(4, 4), Colour(0xff, 0xa5, 0x00)),
            Pixel(Point(5, 4), Colour(0xff, 0xa5, 0x00))
        ]
    s = Sprite(p)
    a = AnimatedSprite(s, Point(0, 1))
    d = VirtualDisplay([])
    d.add_sprite(a)
    v = View(d)
    v.run()
