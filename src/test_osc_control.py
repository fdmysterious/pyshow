"""
┌──────────────────────────┐
│ Simple MIDI control test │
└──────────────────────────┘

 Florian Dupeyron
 July 2022
"""

import asyncio
import logging

from pyshow.osc.control import Control_Desk_OSC

async def main():
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_running_loop()
    ctrl = Control_Desk_OSC(host="0.0.0.0", port=5665)

    ctrl.event_register("/hello", lambda xx:    print("Hello world!")          )
    ctrl.event_register("/value", lambda value: print(f"Value set to {value}") )

    ctrl.start(loop)
    try:
        while True:
            await asyncio.sleep(5)
    except KeyboardInterrupt:
        pass
    finally:
        ctrl.stop()


asyncio.run(main())
