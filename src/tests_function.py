"""
┌───────────────────────────────┐
│ Simple tests around functions │
└───────────────────────────────┘

 Florian Dupeyron
 July 2022
"""

import asyncio
import time
import math

from pyshow.core.fixtures  import Fixture
from pyshow.core.functions import (
    Function_Static,
    Function_Animation,
    Function_Periodic,
    Function_Fade
)

from pyshow.core.interfaces import RangeValue

from tests_dumb import (
    DumbController,
    MyFixture
)

# ┌────────────────────────────────────────┐
# │ Dumb classes                           │
# └────────────────────────────────────────┘

class MyFunction(Function_Animation):
    def __init__(self, interface):
        super().__init__(interface)
        if not isinstance(interface, RangeValue):
            raise TypeError("This function is compatible only for RangeValues")

        self.__v_delta = interface.max - interface.min
        self.__v_min   = interface.min


    async def _compute_value(self, timestamp):
        phasor = timestamp-math.floor(timestamp)
        return self.__v_delta*phasor+self.__v_min


class MyFunctionPeriodic(Function_Periodic):
    def __init__(self, interface, period_s):
        super().__init__(interface, period_s)

        if not isinstance(interface, RangeValue):
            raise TypeError("This function is compatible only for RangeValues")

        self.__v_delta = interface.max - interface.min
        self.__v_min   = interface.min

    async def _compute_value(self, timestamp):
        phasor = timestamp-math.floor(timestamp)
        return self.__v_delta*phasor+self.__v_min


# ┌────────────────────────────────────────┐
# │ Test program                           │
# └────────────────────────────────────────┘

async def main():
    transport = DumbController()
    fixture   = MyFixture(transport=transport, channel_start=1)

    functions = [
        MyFunction(
            interface = fixture.interfaces["dimmer"]
        ),

        MyFunctionPeriodic(
            interface   = fixture.interfaces["color"].r,
            period_s    = 0.5
        ),

        Function_Fade(
            interface   = fixture.interfaces["color"].b,
            fade_time_s = 1
        )
    ]

    try:
        period           = 0.1
        last_exec        = time.time()

        timer_fade_stuff = time.time()
        current_target   = 1.0

        while True:
            tstamp = time.time()

            if tstamp-timer_fade_stuff > 3.0:
                timer_fade_stuff = tstamp
                functions[2].target_set(current_target)
                current_target = 1.0 - current_target

            # Update all functions (in parallel)
            await asyncio.gather(*[
                fkt.update(tstamp) for fkt in functions
            ])

            curtime = time.time()
            await asyncio.sleep(curtime-last_exec+period)
            last_exec = time.time()

    except KeyboardInterrupt:
        pass

asyncio.run(main())
