import curses
import os
import random
import time

from loguru import logger

import settings
from animations import space_garbage, spaceship_animation
from utils import game_scenario, stars_tools, year_tools
from utils.sleep import sleep


def get_garbage_frames():
    filenames = ["trash_xl.txt", "trash_small.txt", "trash_large.txt", "duck.txt", "hubble.txt", "lamp.txt"]
    frames_path = "animations/frames/"
    frames = []
    for filename in filenames:
        with open(os.path.join(frames_path, filename), "r") as garbage_file:
            frames.append(garbage_file.read())
    return frames


async def fill_orbit_with_garbage(canvas):
    frames = get_garbage_frames()
    _, max_x = canvas.getmaxyx()
    while True:
        random_column = random.randint(1, max_x)
        settings.coroutines.append(
            space_garbage.fly_garbage(
                canvas,
                column=random_column,
                garbage_frame=random.choice(frames),
            )
        )

        await sleep(game_scenario.get_garbage_delay_tics(settings.year) or 1)


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

    ship_animation = spaceship_animation.animate_spaceship(canvas, max_y / 2, max_x / 2, frames)
    settings.coroutines.append(ship_animation)

    years = year_tools.increment_year(canvas)
    settings.coroutines.append(years)

    settings.coroutines.extend(stars_tools.generate_stars(canvas))

    garbage = fill_orbit_with_garbage(canvas)
    settings.coroutines.append(garbage)

    while True:
        canvas.border()
        for coroutine in settings.coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                settings.coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(settings.tic_timeout)


if __name__ == "__main__":
    logger.remove(0)
    logger.add("example.log")
    settings.init()
    curses.update_lines_cols()
    try:
        curses.wrapper(draw)
    except KeyboardInterrupt:
        print("EXIT")
