import time
import asyncio
import curses
import random

from animations.fire_animation import fire
from animations.spaceship_animation import animate_spaceship


async def blink(canvas, row, column, symbol="*"):
    while True:
        canvas.border()
        curses.curs_set(False)
        canvas.addstr(row, column, symbol, curses.A_DIM)
        i = random.randint(3, 20)

        for _ in range(i):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(i):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(i):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(i):
            await asyncio.sleep(0)


def get_coordinates(max_y, max_x):
    new_y = random.randint(0, max_y - 3)
    new_x = random.randint(0, max_x - 3)

    return new_y, new_x


def get_star_symbol():
    i = random.randint(0, len(STAR_SYMBOLS))
    return STAR_SYMBOLS[i - 1]


def generate_stars(canvas):
    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1
    coroutines = []
    for _ in range(250):
        symbol = get_star_symbol()
        row, column = get_coordinates(max_row, max_column)
        star = blink(canvas, row, column, symbol)
        coroutines.append(star)

    return coroutines


def draw(canvas):
    rows, columns = canvas.getmaxyx()

    frames = []
    with open("animations/frames/rocket_frame_1.txt", "r") as f:
        frames.append(f.read())
    with open("animations/frames/rocket_frame_2.txt", "r") as f:
        frames.append(f.read())

    # fire_animation = fire(canvas, MAX_Y / 2, MAX_X / 2)
    # coroutines = [fire_animation]

    spaceship_animation = animate_spaceship(canvas, rows / 2, columns / 2, frames)
    coroutines = [spaceship_animation]
    coroutines.extend(generate_stars(canvas))

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == "__main__":
    TIC_TIMEOUT = 0.1
    STAR_SYMBOLS = ["+", "*", ".", ":"]
    curses.update_lines_cols()
    curses.wrapper(draw)
