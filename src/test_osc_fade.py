"""
┌───────────────────────┐
│ Basic tests for Scene │
└───────────────────────┘

 Florian Dupeyron
 July 2022
"""

import logging
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

from pyshow.osc.control import Control_Desk_OSC


async def main():
    logging.basicConfig(level=logging.DEBUG)

    transport = DumbController()
    fixture   = MyFixture(transport = transport, channel_start=1)

    scene   = Scene(functions=[
        Function_Fade(
            interface   = fixture.interfaces["dimmer"],
            target      = 100.0,
            fade_time_s = 0.3
        ),
        
        Function_Fade(
            interface   = fixture.interfaces["color"].r,
            target      = 0.3,
            fade_time_s = 0.1
        )
    ])

    ctrl = Control_Desk_OSC(host="0.0.0.0", port=5665)

    def test_ctrl(target):
        scene.functions[0].target = target*100
        scene.functions[0].trigger()

    ctrl.event_register("/value", test_ctrl)

    ctrl.start(asyncio.get_running_loop())
    try:
        period    = 0.01
        last_exec = time.time()

        fixture.interfaces["dimmer"].set(0)

        scene.trigger()
        while True:
            tstamp = time.time()

            # Update current scene
            await scene.update(tstamp)

            # Sleep
            curtime = time.time()
            await asyncio.sleep(curtime-last_exec+period)
            last_exec=time.time()
    except KeyboardInterrupt:
        pass
    finally:
        ctrl.stop()


asyncio.run(main())
