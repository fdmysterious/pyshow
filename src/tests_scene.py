"""
┌───────────────────────┐
│ Basic tests for Scene │
└───────────────────────┘

 Florian Dupeyron
 July 2022
"""

import asyncio
import time

from tests_dumb import (
    DumbController,
    MyFixture
)

from pyshow.core.scenes    import Scene
from pyshow.core.functions import (
    Function_Static,
    Function_Animation,
    Function_Periodic,
    Function_Fade
)

async def main():
    transport = DumbController()
    fixture   = MyFixture(transport = transport, channel_start=1)

    scene_1   = Scene(functions=[
        Function_Fade(
            interface   = fixture.interfaces["dimmer"],
            target      = 1.0,
            fade_time_s = 1.0
        ),
        
        Function_Fade(
            interface   = fixture.interfaces["color"].r,
            target      = 0.3,
            fade_time_s = 1.0
        )
    ])

    scene_2   = Scene(functions=[
        Function_Fade(
            interface   = fixture.interfaces["dimmer"],
            target      = 0.0,
            fade_time_s = 0.5
        ),
        
        Function_Fade(
            interface   = fixture.interfaces["color"].r,
            target      = 0.8,
            fade_time_s = 0.3 
        )
    ])

    try:
        period    = 0.1
        last_exec = time.time()

        current_scene = scene_1

        scene_1.trigger()

        fixture.interfaces["dimmer"].set(0)

        while True:
            tstamp = time.time()

            # Update current scene
            await scene_1.update(tstamp)

            # Sleep
            curtime = time.time()
            await asyncio.sleep(curtime-last_exec+period)
            last_exec=time.time()
    except KeyboardInterrupt:
        pass


asyncio.run(main())
