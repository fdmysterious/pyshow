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

from pyshow.midi.control import Control_Desk_MIDI
from pyshow.midi         import codec as midi

async def main():
    transport = DumbController()
    fixture   = MyFixture(transport=transport, channel_start=1)


    chooser = Scene_Chooser(
        scenes = {
            "on": Scene(functions=[
                Function_Fade(
                    interface   = fixture.interfaces["dimmer"],
                    target      = 100.0,
                    fade_time_s = 0.1 
                )
            ]),

            "off": Scene(functions=[
                Function_Fade(
                    interface   = fixture.interfaces["dimmer"],
                    target      = 0.0,
                    fade_time_s = 0.1
                )
            ])
        }
    )

    ctrl = Control_Desk_MIDI()

    ctrl.event_register(midi.note_on (0, 21, 0), lambda ev: chooser.choose("off")    )
    ctrl.event_register(midi.note_on (0, 22, 0), lambda ev: chooser.choose("on")     )
    ctrl.event_register(midi.note_on (0, 23, 0), lambda ev: chooser.flash_start("on"))
    ctrl.event_register(midi.note_off(0, 23, 0), lambda ev: chooser.flash_end()      )

    ctrl.start(asyncio.get_running_loop())
    try:
        period      = 0.001
        last_exec   = time.time()

        timer_stuff = last_exec

        chooser.choose("off")

        while True:
            tstamp = time.time()
            await chooser.update(tstamp)

            # Choose scene
            #if tstamp-timer_stuff > 5.0:
            #    timer_stuff = tstamp
            #    chooser.choose("on" if chooser.current() == "off" else "off")

            # Sleep
            curtime   = time.time()
            await asyncio.sleep(curtime-last_exec+period)
            last_exec = time.time()
    except KeyboardInterrupt:
        pass
    finally:
        ctrl.stop()

asyncio.run(main())
