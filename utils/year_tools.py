import settings
from animations import curses_tools

from utils.game_scenario import PHRASES
from utils.sleep import sleep


async def increment_year(canvas):
    phrase = ""
    while True:
        if settings.year in PHRASES:
            phrase = PHRASES.get(settings.year)
        settings.year += 1
        curses_tools.draw_frame(canvas, 1, 5, f"{settings.year} | {phrase}")
        await sleep(15)
        curses_tools.draw_frame(canvas, 1, 5, f"{settings.year} | {phrase}", negative=True)
