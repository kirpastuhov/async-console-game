import curses
import random

import settings

from utils.sleep import sleep


async def blink(canvas, row, column, symbol="*"):
    while True:
        curses.curs_set(False)
        star_state_time = random.randint(3, 20)

        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(star_state_time)

        canvas.addstr(row, column, symbol)
        await sleep(star_state_time)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(star_state_time)

        canvas.addstr(row, column, symbol)
        await sleep(star_state_time)


def get_star_coordinates(max_y, max_x):
    offset = 1
    new_y = random.randint(1, max_y - offset)
    new_x = random.randint(1, max_x - offset)

    return new_y, new_x


def generate_stars(canvas):
    max_y, max_x = canvas.getmaxyx()
    max_row, max_column = max_y - 1, max_x - 1
    for _ in range(100):
        symbol = random.choice(settings.star_symbols)
        row, column = get_star_coordinates(max_row, max_column)
        star = blink(canvas, row, column, symbol)
        settings.coroutines.append(star)

    return settings.coroutines
