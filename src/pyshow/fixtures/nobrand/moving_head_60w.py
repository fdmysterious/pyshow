"""
┌──────────────────────────────────────┐
│ 60W Moving Head chinese fixture def. │
└──────────────────────────────────────┘

 Florian Dupeyron
 July 2022
"""

from typing import Dict
from pyshow.core.interfaces import (
    DiscreteValue_Choice,
    RotationValue
)

from pyshow.dmx.fixtures   import Fixture_DMX
from pyshow.dmx.interfaces import (
    RangeValue_DMX_8Bits,
    RangeValue_DMX_16Bits,

    DiscreteValue_DMX_8Bits
)

from pyshow.dmx.controller import DMX_Controller

from dataclasses import dataclass, field, InitVar

@dataclass(kw_only=True)
class NoBrand_60W_MovingHead_11Ch(Fixture_DMX):
    transport: InitVar[DMX_Controller]
    channel_start: int

    brand: str = "No brand"
    name: str  = "60W Moving head"

    interfaces: Dict[str, any] = field(default_factory=lambda: dict(
        pos = RotationValue(
            pan = RangeValue_DMX_16Bits(
                channel_msb=0,
                channel_lsb=1,

                min        = 0.0,
                max        = 360.0,
                unit       = "°"
            ),

            tilt= RangeValue_DMX_16Bits(
                channel_msb=2,
                channel_lsb=3,

                min        = 0.0,
                max        = 360.0,
                unit       = "°"
            )
        ),

        # TODO #
        color = DiscreteValue_DMX_8Bits(
            channel = 4,
            choices = {
               "white"         : DiscreteValue_Choice(label="white"         , value=0  ),
               "magenta"       : DiscreteValue_Choice(label="Magenta"       , value=10 ),
               "green"         : DiscreteValue_Choice(label="Green"         , value=20 ),
               "blue"          : DiscreteValue_Choice(label="Blue"          , value=30 ),
               "yellow"        : DiscreteValue_Choice(label="Yellow"        , value=40 ),
               "orange"        : DiscreteValue_Choice(label="Orange"        , value=50 ),
               "cyan"          : DiscreteValue_Choice(label="Cyan"          , value=60 ),
               "purple"        : DiscreteValue_Choice(label="Purple"        , value=70 ),

               "purple_cyan"   : DiscreteValue_Choice(label="Purple/Cyan"   , value=80 ),
               "cyan_orange"   : DiscreteValue_Choice(label="Cyan/Orange"   , value=90 ),
               "orange_yellow" : DiscreteValue_Choice(label="Orange/Yellow" , value=100),
               "yellow_blue"   : DiscreteValue_Choice(label="Yellow/Blue"   , value=110),
               "blue_green"    : DiscreteValue_Choice(label="Blue/Green"    , value=120),
               "green_magenta" : DiscreteValue_Choice(label="Green/Magenta" , value=130)
            }
        ),

        # TODO #
        gobo = DiscreteValue_DMX_8Bits(
            channel = 5,
            choices = {
                "plain":     DiscreteValue_Choice(label="Plain",     value=0  ),
                "circles":   DiscreteValue_Choice(label="Circles",   value=8  ),
                "alien":     DiscreteValue_Choice(label="Alien",     value=16 ),
                "fireworks": DiscreteValue_Choice(label="Fireworks", value=24 ),
                "rocks":     DiscreteValue_Choice(label="Rocks",     value=32 ),
                "bubbles":   DiscreteValue_Choice(label="Bubbles",   value=40 ),
                "vortex":    DiscreteValue_Choice(label="Vortex",    value=48 ),
                "zebra":     DiscreteValue_Choice(label="Zebra",     value=56 )

                # TODO # Shake variants
            }
        ),

        strobe = RangeValue_DMX_8Bits(
            channel = 6,

            min     = 0,
            max     = 100,
            unit    = "%"
        ),

        dimmer = RangeValue_DMX_8Bits(
            channel = 7,

            min     = 0,
            max     = 100,
            unit    = "%"
        ),

        speed = RangeValue_DMX_8Bits(
            channel = 8,

            min     = 0,
            max     = 100,
            unit    = "%"
        )

        # Channels 10 and 11 are not implemented here
    ))
