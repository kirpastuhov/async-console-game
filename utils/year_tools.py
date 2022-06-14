import settings

from animations import curses_tools
from utils.sleep import sleep


async def increment_year(canvas):
    while True:
        settings.year += 1
        curses_tools.draw_frame(canvas, 50, 50, str(settings.year))
        await sleep(15)
        curses_tools.draw_frame(canvas, 50, 50, str(settings.year), negative=True)
