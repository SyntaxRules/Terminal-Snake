import curses
from time import sleep
from .snake import Snake
from .apple import Apple


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
    apple = Apple(width-1, height-1, 1, 1)

    while True:
        height, width = get_terminal_dimentions(stdscr)
        print_boarder(stdscr)
        snake.print(stdscr)
        apple.print(stdscr)
        stdscr.refresh()

        # User input
        last_input = user_input = stdscr.getch()
        while last_input != curses.ERR:
            user_input = last_input
            last_input = stdscr.getch()

        snake.advance(user_input)

        if not snake.is_valid(width-1, 0, height-1, 0):
            break

        if snake.collides(apple.location):
            snake.grow()
            apple = Apple(width - 2, height - 2, 1, 1)

        sleep(1.0/4)

    return snake.get_snake_length()


def run():
    score = curses.wrapper(run_game)
    print_end_game(score)
