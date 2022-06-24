import os
import random

import settings
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

        await sleep.sleep(game_scenario.get_garbage_delay_tics(settings.year) or 1)
