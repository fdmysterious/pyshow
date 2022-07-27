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

from pyshow.core.scenes    import Scene, Scene_Sequence
from pyshow.core.functions import (
    Function_Static,
    Function_Animation,
    Function_Periodic,
    Function_Fade,

    Function_Delay
)

async def main():
    transport = DumbController()
    fixture   = MyFixture(transport = transport, channel_start=1)

    scene = Scene_Sequence(steps=[
        Scene(functions=[Function_Static(interface = fixture.interfaces["dimmer"], target=100.0)]),
        Scene(functions=[Function_Delay (delay_s   = 1)                                         ]),
        Scene(functions=[Function_Fade  (interface = fixture.interfaces["dimmer"], target=0.0, fade_time_s=1)  ]),
        Scene(functions=[Function_Delay (delay_s   = 1)                                         ]),
    ])

    try:
        period    = 0.01
        last_exec = time.time()

        while True:
            # Initial scene trigger
            if scene.finished():
                scene.trigger()

            tstamp = time.time()

            # Update current scene
            await scene.update(tstamp)

            # Sleep
            curtime = time.time()
            await asyncio.sleep(curtime-last_exec+period)
            last_exec=time.time()
    except KeyboardInterrupt:
        pass


asyncio.run(main())
