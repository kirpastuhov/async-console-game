import time
import asyncio
import curses
import random

from animations.spaceship_animation import animate_spaceship

TIC_TIMEOUT = 0.1
STAR_SYMBOLS = ["+", "*", ".", ":"]


async def blink(canvas, row, column, symbol="*"):
    while True:
        curses.curs_set(False)
        star_state_time = random.randint(3, 20)

        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(star_state_time):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(star_state_time):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(star_state_time):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(star_state_time):
            await asyncio.sleep(0)


def get_star_coordinates(max_y, max_x):
    offset = 1
    new_y = random.randint(1, max_y - offset)
    new_x = random.randint(1, max_x - offset)

    return new_y, new_x


def generate_stars(canvas):
    max_y, max_x = canvas.getmaxyx()
    max_row, max_column = max_y - 1, max_x - 1
    coroutines = []
    for _ in range(250):
        symbol = random.choice(STAR_SYMBOLS)
        row, column = get_star_coordinates(max_row, max_column)
        star = blink(canvas, row, column, symbol)
        coroutines.append(star)

    return coroutines


def draw(canvas):
    canvas.nodelay(True)
    max_y, max_x = canvas.getmaxyx()

    frames = []
    with open("animations/frames/rocket_frame_1.txt", "r") as f:
        frame = f.read()
        frames.extend([frame, frame])
    with open("animations/frames/rocket_frame_2.txt", "r") as f:
        frame = f.read()
        frames.extend([frame, frame])

    spaceship_animation = animate_spaceship(canvas, max_y / 2, max_x / 2, frames)
    coroutines = [spaceship_animation]
    coroutines.extend(generate_stars(canvas))

    while True:
        canvas.border()
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(draw)
