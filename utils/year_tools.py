import curses
from typing import Coroutine

import shared
from animations import curses_tools

from utils.game_scenario import PHRASES
from utils.sleep import sleep


async def increment_year(canvas: curses.window) -> Coroutine:
    phrase = ""
    while True:
        if shared.year in PHRASES:
            phrase = PHRASES.get(shared.year)
        if not shared.game_over:
            shared.year += 1
        curses_tools.draw_frame(canvas, 1, 5, f"{shared.year} | {phrase}")
        await sleep(15)
        curses_tools.draw_frame(canvas, 1, 5, f"{shared.year} | {phrase}", negative=True)
