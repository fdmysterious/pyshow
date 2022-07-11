"""
┌──────────────────────────┐
│ Classes for DMX Fixtures │
└──────────────────────────┘

 Florian Dupeyron
 July 2022
"""

from dataclasses           import dataclass, field, InitVar
from pyshow.core.fixtures  import Fixture

from pyshow.dmx.controller import DMX_Controller

from typing                import Dict


# ┌────────────────────────────────────────┐
# │ Fixture_DMX base class                 │
# └────────────────────────────────────────┘

@dataclass
class Fixture_DMX(Fixture):
    transport: InitVar[DMX_Controller]
    channel_start: int

    brand: str
    name: str

    interfaces: Dict[str, any]

    # ──────────── Post init hook ──────────── #
    
    def __post_init__(self, transport):
        self._transport = transport
        super().__post_init__()


    # ────────── Shorthand functions ───────── #

    def ch_set(self, offset, value):
        self._transport.ch_set(self.channel_start+offset, value)
