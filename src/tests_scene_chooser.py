"""
┌────────────────────┐
│ Test Scene chooser │
└────────────────────┘

 Florian Dupeyron
 July 2022
"""

import asyncio
import time

from tests_dumb import (
    DumbController,
    MyFixture
)

from pyshow.core.scenes import (
    Scene,
    Scene_Chooser
)

from pyshow.core.functions import (
    Function_Static,
    Function_Animation,
    Function_Periodic,
    Function_Fade
)

async def main():
    transport = DumbController()
    fixture   = MyFixture(transport=transport, channel_start=1)


    chooser = Scene_Chooser(
        scenes = {
            "on": Scene(functions=[
                Function_Fade(
                    interface   = fixture.interfaces["dimmer"],
                    target      = 100.0,
                    fade_time_s = 1.0
                )
            ]),

            "off": Scene(functions=[
                Function_Fade(
                    interface   = fixture.interfaces["dimmer"],
                    target      = 0.0,
                    fade_time_s = 1.0
                )
            ])
        }
    )

    try:
        period      = 0.01
        last_exec   = time.time()

        timer_stuff = last_exec

        chooser.choose("off")

        while True:
            tstamp = time.time()
            await chooser.update(tstamp)

            # Choose scene
            if tstamp-timer_stuff > 5.0:
                timer_stuff = tstamp
                chooser.choose("on" if chooser.current() == "off" else "off")

            # Sleep
            curtime   = time.time()
            await asyncio.sleep(curtime-last_exec+period)
            last_exec = time.time()
    except KeyboardInterrupt:
        pass

asyncio.run(main())
