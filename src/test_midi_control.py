"""
┌──────────────────────────┐
│ Simple MIDI control test │
└──────────────────────────┘

 Florian Dupeyron
 July 2022
"""

import asyncio
from pyshow.midi.control import Control_Desk_MIDI
from pyshow.midi         import codec as midi

async def main():
    loop = asyncio.get_running_loop()
    ctrl = Control_Desk_MIDI()

    ctrl.event_register(midi.note_on(0, 32, 0), lambda ev: print("Special ev!"))
    ctrl.event_register(midi.cc     (0, 1 , 0), lambda ev: print(f"Modulation! {ev.values[1]}"))

    ctrl.start(loop)
    try:
        while True:
            await asyncio.sleep(5)
    except KeyboardInterrupt:
        pass
    finally:
        ctrl.stop()


asyncio.run(main())
