"""
┌────────────────────────────────────────┐
│ Starway maxkolor 18 fixture definition │
└────────────────────────────────────────┘

 Florian Dupeyron
 July 2022
"""

from typing import Dict
from pyshow.core.interfaces import (
    DiscreteValue_Choice,
    RotationValue,
    ColorValue
)

from pyshow.dmx.fixtures   import Fixture_DMX
from pyshow.dmx.interfaces import (
    RangeValue_DMX_8Bits,
    RangeValue_DMX_16Bits,

    DiscreteValue_DMX_8Bits
)

from pyshow.dmx.controller import DMX_Controller
from dataclasses           import dataclass, field, InitVar

@dataclass(kw_only=True)
class Starway_Maxkolor18_11Ch(Fixture_DMX):
    transport: InitVar[DMX_Controller]
    channel_start: int

    brand: str = "Starway"
    name: str  = "Maxkolor18"

    interfaces: Dict[str, any] = field(default_factory=lambda: dict(
        mode  = DiscreteValue_DMX_8Bits( channel=0,
            choices = {
                "rgb"  : DiscreteValue_Choice(label="RGB"   , value=0  ),
                "auto1": DiscreteValue_Choice(label="Auto 1", value=25 ),
                "auto2": DiscreteValue_Choice(label="Auto 2", value=50 ),
                "auto3": DiscreteValue_Choice(label="Auto 3", value=75 ),
                "auto4": DiscreteValue_Choice(label="Auto 4", value=100),
                "auto5": DiscreteValue_Choice(label="Auto 5", value=125),
                "auto6": DiscreteValue_Choice(label="Auto 6", value=150),
                "auto7": DiscreteValue_Choice(label="Auto 7", value=175),
                "auto8": DiscreteValue_Choice(label="Auto 8", value=200),
                "auto9": DiscreteValue_Choice(label="Auto 9", value=250)
            }
        ),

        color = ColorValue(
            r = RangeValue_DMX_8Bits(channel=1, min=0.0, max=1.0),
            g = RangeValue_DMX_8Bits(channel=2, min=0.0, max=1.0),
            b = RangeValue_DMX_8Bits(channel=3, min=0.0, max=1.0)
        ),

        strobe    = RangeValue_DMX_8Bits(channel=4, min=0.0, max=100, unit="%"             ),
        prg_speed = RangeValue_DMX_8Bits(channel=4, min=0.0, max=100, unit="%", invert=True),

        dimmer    = RangeValue_DMX_8Bits(channel=5, min=0.0, max=100, unit="%", invert=True),
        speed     = RangeValue_DMX_8Bits(channel=8, min=0.0, max=100, unit="%"             ),
        pos       = RotationValue(
            pan = RangeValue_DMX_16Bits(
                channel_msb = 6,
                channel_lsb = 9,

                min         = 0.0,
                max         = 360.0,
                unit        = "°"
            ),


            tilt = RangeValue_DMX_16Bits(
                channel_msb = 7,
                channel_lsb = 10,

                min         = 0.0,
                max         = 360.0,
                unit        = "°"
            )
        )
    ))
