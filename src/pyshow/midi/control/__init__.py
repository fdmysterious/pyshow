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

        self._filters   = dict()

    def event_register(self, template_msg: midi.Midi_Msg, cbk):
        ch_num = template_msg.chan
        ttype  = template_msg.type
        values = template_msg.values

        if not ch_num in self._filters:
            self._filters[ch_num] = dict()

        if not ttype in self._filters[ch_num]:
            self._filters[ch_num][ttype] = dict()

        if values[0] in self._filters[ch_num][ttype]:
            raise ValueError(f"An event is already registered for event {ev}")
        else:
            self._filters[ch_num][ttype][values[0]] = cbk
        

    async def _hook_open(self):
        self._in_port.open_virtual_port(self._port_name)
        self._in_port.set_callback(self._callback)

    async def _hook_close(self):
        self._in_port.close()

    async def _hook_process(self, ev):
        print(f"Received MIDI: {ev}")

        # FIXME # Kinda ugly
        if ev.chan in self._filters:
            if ev.type in self._filters[ev.chan]:
                if ev.values[0] in self._filters[ev.chan][ev.type]:
                    self._filters[ev.chan][ev.type][ev.values[0]](ev)


    def _callback(self, ev, data=None):
        msg,deltaT = ev

        try:
            parsed = midi.from_bytes(bytes(msg))
            self._push_event(parsed)
        except Exception as exc:
            # TODO # Better logging
            print(f"Failed to parse or store MIDI message: {exc}")
