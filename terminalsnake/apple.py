import curses
from random import randint
from .utilities import Location


class Apple(object):
    def __init__(self, max_x: int, max_y: int, min_x=0, min_y=0):
        self.location: Location = Location(randint(min_x, max_x), randint(min_y, max_y))

    def print(self, screen):
        screen.addstr(self.location.y, self.location.x, ' ', curses.color_pair(4))
