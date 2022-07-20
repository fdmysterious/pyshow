"""
┌──────────────────────────┐
│ Simple MIDI control test │
└──────────────────────────┘

 Florian Dupeyron
 July 2022
"""

import asyncio
from pyshow.midi.control import Control_Desk_MIDI

async def main():
    loop = asyncio.get_running_loop()
    ctrl = Control_Desk_MIDI()

    ctrl.start(loop)
    try:
        while True:
            await asyncio.sleep(5)
    except KeyboardInterrupt:
        pass
    finally:
        ctrl.stop()


asyncio.run(main())
