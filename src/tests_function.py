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
    Function_Periodic
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

        MyFunction(
            interface = fixture.interfaces["color"].r
        ),


        MyFunction(
            interface = fixture.interfaces["color"].g
        )
    ]

    try:
        period    = 0.1
        last_exec = time.time()
        while True:
            tstamp = time.time()
            await asyncio.gather(*[
                fkt.update(tstamp) for fkt in functions
            ])

            curtime = time.time()
            await asyncio.sleep(curtime-last_exec+period)
            last_exec = time.time()

    except KeyboardInterrupt:
        pass

asyncio.run(main())
