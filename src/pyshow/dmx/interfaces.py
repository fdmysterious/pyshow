"""
┌─────────────────────────────┐
│ Interfaces specific for DMX │
└─────────────────────────────┘

 Florian Dupeyron
 July 2022
"""

from pyshow.core.interfaces import (
    RangeValue,

    DiscreteValue_Choice,
    DiscreteValue
)

from pyshow.dmx.fixtures import (Fixture_DMX)

from dataclasses import dataclass, field

from typing import Optional, Dict


# ┌────────────────────────────────────────┐
# │ 8BitsRangeValue class                  │
# └────────────────────────────────────────┘

@dataclass(kw_only=True)
class RangeValue_DMX_8Bits(RangeValue):
    channel: int

    min: float
    max: float

    unit: Optional[str] = ""

    class_id: str = "RangeValue_DMX_8Bits"

    # ─────────────── Post init ────────────── #

    def __post_init__(self):
        super().__post_init__()


    # ───────────────── Hooks ──────────────── #

    def _on_set(self, v):
        if self.fixture is None:
            raise ValueError("No DMX fixture attached")
        elif not isinstance(self.fixture, Fixture_DMX):
            raise ValueError("Attached fixture is not DMX compatible.")

        v_byte = ((v-self.min)/self.max)*((1<<8)-1)
        self.fixture.ch_set(self.channel, int(v_byte))
    

# ┌────────────────────────────────────────┐
# │ 16BitsRangeValue class value           │
# └────────────────────────────────────────┘

@dataclass(kw_only=True)
class RangeValue_DMX_16Bits(RangeValue):
    channel_msb: int
    channel_lsb: int

    min: float
    max: float

    unit: Optional[str] = ""

    class_id: str = "RangeValue_DMX_16Bits"


    # ─────────────── Post init ────────────── #
    
    def __post_init__(self):
        super().__post_init__()


    # ───────────────── Hooks ──────────────── #
    
    def _on_set(self, v):
        if self.fixture is None:
            raise ValueError("No DMX fixture attached")
        elif not isinstance(self.fixture, Fixture_DMX):
            raise ValueError("Attached fixture is not DMX compatible.")

        v_short = ((v-self.min)/self.max)*((1<<16)-1)
        self.fixture.ch_set(self.channel_msb, (int(v_short)>>8))
        self.fixture.ch_set(self.channel_lsb, (int(v_short) & 0xFF))


# ┌────────────────────────────────────────┐
# │ DiscreteValue_DMX class                │
# └────────────────────────────────────────┘

@dataclass(kw_only=True)
class DiscreteValue_DMX_8Bits(DiscreteValue):
    channel: int

    choices: Dict[str, DiscreteValue_Choice]
    class_id: str = "DiscreteValue_DMX_8Bits"

    
    def _on_set(self, v):
        if self.fixture is None:
            raise ValueError("No DMX fixture atteched")
        elif not isinstance(self.fixture, Fixture_DMX):
            raise ValueError("Attached fixture is not DMX compatible")
        
        self.fixture.ch_set(self.channel, int(self.choices[v].value))
