"""
┌───────────────────────────────────────┐
│ Simple MIDI Controller implementation │
└───────────────────────────────────────┘

 Florian Dupeyron
 July 2022
"""

import rtmidi

from pyshow.core.control import Control_Desk
from pyshow.midi         import codec as midi

# ┌────────────────────────────────────────┐
# │ Control_Desk_MIDI class                │
# └────────────────────────────────────────┘

class Control_Desk_MIDI(Control_Desk):
    def __init__(self, port_name: str = "PyShow MIDI In"):
        super().__init__()
        self._in_port   = rtmidi.MidiIn()
        self._port_name = port_name
        
    async def _hook_open(self):
        self._in_port.open_virtual_port(self._port_name)
        self._in_port.set_callback(self._callback)

    async def _hook_close(self):
        self._in_port.close()

    async def _hook_process(self, ev):
        print(f"Received MIDI: {ev}")

    def _callback(self, ev, data=None):
        msg,deltaT = ev

        try:
            parsed = midi.from_bytes(bytes(msg))
            self._push_event(parsed)
        except Exception as exc:
            # TODO # Better logging
            print(f"Failed to parse or store MIDI message: {exc}")
