"""
┌──────────────────────────────────────────────┐
│ Simple adapter for STM32 dumb dmx controller │
└──────────────────────────────────────────────┘

 Florian Dupeyron
 July 2022
"""

import serial
import logging

from enum        import IntEnum
from dataclasses import dataclass, field

from pyshow.dmx.controller import DMX_Controller


# ┌────────────────────────────────────────┐
# │ Data classes                           │
# └────────────────────────────────────────┘

class DMX_STM32_Cmd(IntEnum):
    CH_SET   = 0x00
    BLACKOUT = 0x01

    OK       = 0x70
    ERR      = 0x71


@dataclass
class DMX_STM32_Msg:
    cmd:    DMX_STM32_Cmd
    value0: int
    value1: int

    # ───────────── Encode/decode ──────────── #
    def to_bytes(self):
        return bytes([
            self.cmd.value,
            self.value0>>2,
            ((self.value0&0x3)<<5)|(self.value1>>7),
            self.value1&0x7f
        ])

    @classmethod
    def from_bytes(cls, data):
        return None # TODO
        #return cls(
        #    cmd    = DMX_STM32_Cmd(data[0]>>1),
        #    value0 = ((data[0] & 0x1)<<8) | (data[1]&0xFF),
        #    value1 = (data[2]&0xFF)
        #)


# ┌────────────────────────────────────────┐
# │ Controller class                       │
# └────────────────────────────────────────┘

class DMX_Controller_STM32(DMX_Controller):
    def __init__(self, path):
        self.dev               = serial.serial_for_url(path, do_not_open=True)

        self.dev.baudrate      = 576000
        self.dev.bytesize      = serial.EIGHTBITS
        self.dev.parity        = serial.PARITY_NONE
        self.dev.stopbits      = serial.STOPBITS_ONE
        self.dev.rtscts        = 0

        self.dev.timeout       = 5
        self.dev.write_timeout = 5

        self.buffer            = bytes()

        self.log               = logging.getLogger(f"STM32 controller on {path}")


    # ┌────────────────────────────────────────┐
    # │ Controller hooks                       │
    # └────────────────────────────────────────┘
    
    def _on_ch_set(self, ch: int, value: int):
        self.log.debug(f"#{ch} = {value}")
        self._req(DMX_STM32_Msg(
            cmd    = DMX_STM32_Cmd.CH_SET,
            value0 = ch,
            value1 = value
        ))


    # ┌────────────────────────────────────────┐
    # │ Controller specific functions          │
    # └────────────────────────────────────────┘

    def open(self):
        self.dev.open()

    def close(self):
        self.dev.close()
    
    def _wrap(self, cmd):
        return bytes([cmd[0] | 0x80]) + cmd[1:] + bytes([0xFF])

    def _req(self, cmd):
        self.buffer += self._wrap(cmd.to_bytes())

    def flush(self):
        self.dev.write(self.buffer)
        self.buffer = bytes()
