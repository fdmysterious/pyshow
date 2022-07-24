"""
┌───────────────────────┐
│ Basic tests for Scene │
└───────────────────────┘

 Florian Dupeyron
 July 2022
"""

import asyncio
import time
import logging

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

from pyshow.fixtures.nobrand.moving_head_60w import NoBrand_60W_MovingHead_11Ch
from pyshow.dmx.stm32dmx import DMX_Controller_STM32

async def main():
    transport = DMX_Controller_STM32("/dev/ttyACM0")
    fixture   = NoBrand_60W_MovingHead_11Ch(transport=transport, channel_start=0)

    scene_1   = Scene(functions=[
        Function_Fade(
            interface   = fixture.interfaces["dimmer"],
            target      = 100.0,
            fade_time_s = 2.5
        ),
        
        Function_Fade(
            interface   = fixture.interfaces["pos"].tilt,
            target      = 0,
            fade_time_s = 5 
        ),

        Function_Fade(
            interface   = fixture.interfaces["pos"].pan,
            target      = 0,
            fade_time_s = 5 
        )
    ])

    scene_2   = Scene(functions=[
        Function_Fade(
            interface   = fixture.interfaces["dimmer"],
            target      = 0.0,
            fade_time_s = 2.5
        ),
        
        Function_Fade(
            interface   = fixture.interfaces["pos"].tilt,
            target      = 360,
            fade_time_s = 5.0
        ),

        Function_Fade(
            interface = fixture.interfaces["pos"].pan,
            target    = 360.0,
            fade_time_s = 5.0
        )
    ])

    transport.open()
    try:
        period    = 0.015
        last_exec = time.time()

        current_scene = scene_1


        fixture.interfaces["dimmer"].set(0)
        #fixture.interfaces["gobo"].set("rocks")

        while True:
            # Initial scene trigger
            if current_scene.finished():
                current_scene.trigger()

            tstamp = time.time()

            # Update current scene
            await current_scene.update(tstamp)

            # Change scene ,
            if current_scene.finished():
                current_scene = scene_2 if current_scene == scene_1 else scene_1

            # flush controller
            transport.flush()

            # Sleep
            curtime = time.time()
            await asyncio.sleep(curtime-last_exec+period)
            last_exec=time.time()
    except KeyboardInterrupt:
        pass
    finally:
        transport.close()


asyncio.run(main())
