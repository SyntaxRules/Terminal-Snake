import curses
from copy import copy
from .utilities import Location


class Snake(object):

    DIRECTION_UP = curses.KEY_UP
    DIRECTION_DOWN = curses.KEY_DOWN
    DIRECTION_LEFT = curses.KEY_LEFT
    DIRECTION_RIGHT = curses.KEY_RIGHT

    def __init__(self, screen_height, screen_width):
        self.direction = self.DIRECTION_UP
        self.length: int = 1
        self.locations: List[Location] = [Location(screen_width * (2 / 3), screen_height / 2)]

    def advance(self, new_snake_direction=None):
        if new_snake_direction and (new_snake_direction == self.DIRECTION_UP or
                                    new_snake_direction == self.DIRECTION_DOWN or
                                    new_snake_direction == self.DIRECTION_LEFT or
                                    new_snake_direction == self.DIRECTION_RIGHT):
            self.direction = new_snake_direction

        new_snake_head: Location = copy(self.locations[0])
        if self.direction == self.DIRECTION_DOWN:
            new_snake_head.y += 1
        if self.direction == self.DIRECTION_UP:
            new_snake_head.y -= 1
        if self.direction == self.DIRECTION_RIGHT:
            new_snake_head.x += 1
        if self.direction == self.DIRECTION_LEFT:
            new_snake_head.x -= 1

        self.locations.insert(0, new_snake_head)
        if len(self.locations) > self.length:
            del self.locations[self.length:]

    def grow(self):
        if self.length < 10:
            self.length += 1

    def get_snake_length(self):
        return self.length + 1

    def print(self, screen):
        for location in self.locations:
            screen.addstr(location.y, location.x, ' ', curses.color_pair(3))

    def is_valid(self, max_x: int, min_x: int, max_y: int, min_y: int):
        """
        Snakes can't be on top of themselves and must be within the supplied
        parameters.
        :return:
        """
        for loc1 in self.locations:
            if loc1.x < min_x or loc1.x > max_x or loc1.y < min_y or loc1.y > max_y:
                return False
            for loc2 in self.locations:
                if loc1 is not loc2 and loc1 == loc2:
                    return False

        return True

    def collides(self, other_location: Location):
        for snake_location in self.locations:
            if other_location == snake_location:
                return True

        return False



