import curses
import os
import random

import shared
from animations import space_garbage

from utils import game_scenario, sleep


def get_garbage_frames():
    filenames = ["trash_xl.txt", "trash_small.txt", "trash_large.txt", "duck.txt", "hubble.txt", "lamp.txt"]
    frames_path = "animations/frames/"
    frames = []
    for filename in filenames:
        with open(os.path.join(frames_path, filename), "r") as garbage_file:
            frames.append(garbage_file.read())
    return frames


async def fill_orbit_with_garbage(canvas: curses.window):
    frames = get_garbage_frames()
    _, max_x = canvas.getmaxyx()
    while True:
        random_column = random.randint(1, max_x)
        shared.coroutines.append(
            space_garbage.fly_garbage(
                canvas,
                column=random_column,
                garbage_frame=random.choice(frames),
            )
        )

        await sleep.sleep(game_scenario.get_garbage_delay_tics(shared.year) or 1)
