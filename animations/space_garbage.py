import logging

import obstacle
import settings
from utils.sleep import sleep

from animations import curses_tools, exposion

logging.basicConfig(filename="example.log", level=logging.DEBUG)


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""

    if settings.year <= 1961:
        return

    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        curses_tools.draw_frame(canvas, row, column, garbage_frame)

        frame_row, frame_col = curses_tools.get_frame_size(garbage_frame)

        ob = obstacle.Obstacle(row, column, frame_row, frame_col)
        settings.obstacles.append(ob)

        await sleep()
        curses_tools.draw_frame(canvas, row, column, garbage_frame, negative=True)

        if ob in settings.obstacles_in_last_collisions:
            settings.obstacles_in_last_collisions.remove(ob)
            settings.obstacles.remove(ob)
            await exposion.explode(canvas, row + frame_row / 2, column + frame_col / 2)
            return

        settings.obstacles.remove(ob)
        row += speed
