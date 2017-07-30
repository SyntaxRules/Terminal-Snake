from copy import copy

import curses
from curses import wrapper

def get_terminal_dimentions(std_screen):
    return std_screen.getmaxyx()

def print_board(stdscr):
    # Clear screen
    stdscr.clear()
    init_colors()
    height, width = get_terminal_dimentions(stdscr)

    # stdscr.border()

    # Boarder
    for i in range(0, width-1):
        stdscr.addstr(0, i, ' ', curses.color_pair(1))
        stdscr.addstr(height-1, i, ' ', curses.color_pair(1))
    for i in range(0, height-1):
        stdscr.addstr(i, 0, ' ', curses.color_pair(1))
        stdscr.addstr(i, width-1, ' ', curses.color_pair(1))

    # Apple

    # Snake
    snake = Snake(stdscr)
    snake.print()



    # # This raises ZeroDivisionError when i == 10.
    # for i in range(0, 11):
    #     v = i-10
    #     if v == 0:
    #         continue
    #     stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10/v), curses.A_REVERSE)
    #     stdscr.addstr('h: {} w: {}'.format(height, width), curses.A_REVERSE)

    stdscr.refresh()
    stdscr.getkey()

class Snake(object):

    DIRECTION_UP = 'UP'
    DIRECTION_DOWN = 'DOWN'
    DIRECTION_LEFT = 'LEFT'
    DIRECTION_RIGHT = 'RIGHT'

    def __init__(self, stdscr):
        self.screen = stdscr
        self.screen_height, self.screen_width = get_terminal_dimentions(stdscr)
        self.snake_head_location = Location(self.screen_width * (2/3), self.screen_height / 2)
        self.snake_direction = 'UP'
        self.snake_tail_length = 0  # To make things easier, 0 means just the head
        self.snake_previous_locations = []

    def advance(self):
        self.snake_previous_locations.append(copy(self.snake_head_location))

        if self.snake_direction == self.DIRECTION_UP:
            self.snake_head_location.y += 1

    def print(self):

        self.screen.addstr(self.snake_head_location.y, self.snake_head_location.x, ' ', curses.color_pair(3))

        if self.snake_tail_length > 0:
            for i in range(1, self.snake_tail_length):
                location = self.snake_previous_locations[i]
                self.screen.addstr(location.y, location.x, ' ', curses.color_pair(3))


class Location(object):

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)


def init_colors():
    # Boarder
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    # Board
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    # Snake
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
    # Apple
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)

if __name__ == '__main__':
    wrapper(print_board)

