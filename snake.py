from copy import copy
from time import sleep

import curses
from curses import wrapper


def get_terminal_dimentions(std_screen):
    return std_screen.getmaxyx()

def print_end_game(stdscr, points):
    print('The game has ended with {} points.'.format(points))
    stdscr.addstr(5, 5, 'The Game Has Ended', curses.color_pair(1))


def print_boarder(stdscr):
    # Clear screen
    stdscr.clear()
    init_colors()
    height, width = get_terminal_dimentions(stdscr)

    # Boarder
    for i in range(0, width-1):
        stdscr.addstr(0, i, ' ', curses.color_pair(1))
        stdscr.addstr(height-1, i, ' ', curses.color_pair(1))
    for i in range(0, height-1):
        stdscr.addstr(i, 0, ' ', curses.color_pair(1))
        stdscr.addstr(i, width-1, ' ', curses.color_pair(1))


class Snake(object):

    DIRECTION_UP = curses.KEY_UP
    DIRECTION_DOWN = curses.KEY_DOWN
    DIRECTION_LEFT = curses.KEY_LEFT
    DIRECTION_RIGHT = curses.KEY_RIGHT

    def __init__(self, stdscr):
        self.screen = stdscr
        self.screen_height, self.screen_width = get_terminal_dimentions(stdscr)
        self.snake_head_location = Location(self.screen_width * (2/3), self.screen_height / 2)
        self.snake_direction = self.DIRECTION_UP
        self.snake_tail_length = 0  # To make things easier, 0 means just the head
        self.snake_previous_locations = []

    def advance(self, new_snake_direction=None):
        if new_snake_direction and (new_snake_direction == self.DIRECTION_UP or
                                    new_snake_direction == self.DIRECTION_DOWN or
                                    new_snake_direction == self.DIRECTION_LEFT or
                                    new_snake_direction == self.DIRECTION_RIGHT):
            self.snake_direction = new_snake_direction
        self.snake_previous_locations.append(copy(self.snake_head_location))

        if self.snake_direction == self.DIRECTION_DOWN:
            self.snake_head_location.y += 1
        if self.snake_direction == self.DIRECTION_UP:
            self.snake_head_location.y -= 1
        if self.snake_direction == self.DIRECTION_RIGHT:
            self.snake_head_location.x += 1
        if self.snake_direction == self.DIRECTION_LEFT:
            self.snake_head_location.x -= 1

    def grow(self):
        if self.snake_tail_length < 10:
            self.snake_tail_length += 1

    def get_snake_length(self):
        return self.snake_tail_length + 1

    def print(self):
        self.screen.addstr(self.snake_head_location.y, self.snake_head_location.x, ' ', curses.color_pair(3))
        stored_points = len(self.snake_previous_locations)
        if self.snake_tail_length > 0:
            for i in range(stored_points - self.snake_tail_length, stored_points):
                location = self.snake_previous_locations[i]
                self.screen.addstr(location.y, location.x, ' ', curses.color_pair(3))

    def is_valid(self, max_x=None, min_x=None, max_y=None, min_y=None):
        """
        Snakes can't be on top of themselves and must be within the supplied
        parameters.
        :return:
        """
        all_locations = [self.snake_head_location]
        all_locations.extend(self.snake_previous_locations[-self.snake_tail_length:])
        for loc1 in all_locations:
            for loc2 in all_locations:
                if loc1 is not loc2 and loc1 == loc2:
                    return False

        return True


class Location(object):
    """
    A standard Data Object for holding things
    """

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def init_colors():
    # Boarder
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    # Board
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    # Snake
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
    # Apple
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)


def run_game(stdscr):
    # Set the cursor to invisible
    curses.curs_set(0)
    stdscr.nodelay(True)

    # Snake
    snake = Snake(stdscr)

    print_boarder(stdscr)
    snake.print()
    stdscr.refresh()

    while True:
        sleep(1.0/2)

        # User input
        last_input = user_input = stdscr.getch()
        while last_input != curses.ERR:
            user_input = last_input
            last_input = stdscr.getch()

        snake.advance(user_input)


        print_boarder(stdscr)
        snake.print()
        stdscr.refresh()

        # If there is a collision with an apple, then
        snake.grow()

        if not snake.is_valid():
            break

    print_end_game(stdscr, snake.get_snake_length())

if __name__ == '__main__':
    wrapper(run_game)

