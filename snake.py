from copy import copy
from time import sleep

import curses
from curses import wrapper


def get_terminal_dimentions(std_screen):
    return std_screen.getmaxyx()

def print_end_game(points):
    print('The game has ended with {} points.'.format(points))


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

    def __init__(self, screen_height, screen_width):
        self.snake_direction = self.DIRECTION_UP
        self.snake_length: int = 1
        self.snake_locations: List[Location] = [Location(screen_width * (2 / 3), screen_height / 2)]

    def advance(self, new_snake_direction=None):
        if new_snake_direction and (new_snake_direction == self.DIRECTION_UP or
                                    new_snake_direction == self.DIRECTION_DOWN or
                                    new_snake_direction == self.DIRECTION_LEFT or
                                    new_snake_direction == self.DIRECTION_RIGHT):
            self.snake_direction = new_snake_direction

        new_snake_head: Location = copy(self.snake_locations[0])
        if self.snake_direction == self.DIRECTION_DOWN:
            new_snake_head.y += 1
        if self.snake_direction == self.DIRECTION_UP:
            new_snake_head.y -= 1
        if self.snake_direction == self.DIRECTION_RIGHT:
            new_snake_head.x += 1
        if self.snake_direction == self.DIRECTION_LEFT:
            new_snake_head.x -= 1

        self.snake_locations.insert(0, new_snake_head)
        if len(self.snake_locations) > self.snake_length:
            del self.snake_locations[self.snake_length:]

    def grow(self):
        if self.snake_length < 10:
            self.snake_length += 1

    def get_snake_length(self):
        return self.snake_length + 1

    def print(self, screen):
        for location in self.snake_locations:
            screen.addstr(location.y, location.x, ' ', curses.color_pair(3))

    def is_valid(self, max_x: int, min_x: int, max_y: int, min_y: int):
        """
        Snakes can't be on top of themselves and must be within the supplied
        parameters.
        :return:
        """
        for loc1 in self.snake_locations:
            if loc1.x < min_x or loc1.x > max_x or loc1.y < min_y or loc1.y > max_y:
                return False
            for loc2 in self.snake_locations:
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
    height, width = get_terminal_dimentions(stdscr)
    snake = Snake(height, width)

    while True:
        height, width = get_terminal_dimentions(stdscr)
        print_boarder(stdscr)
        snake.print(stdscr)
        stdscr.refresh()

        # User input
        last_input = user_input = stdscr.getch()
        while last_input != curses.ERR:
            user_input = last_input
            last_input = stdscr.getch()

        snake.advance(user_input)
        snake.grow()

        if not snake.is_valid(width-1, 0, height-1, 0):
            break

        sleep(1.0/2)

    return snake.get_snake_length()

if __name__ == '__main__':
    score = wrapper(run_game)
    print_end_game(score)


