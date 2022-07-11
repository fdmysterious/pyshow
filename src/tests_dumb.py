"""
┌─────────────────────────────────┐
│ Various dumb tests using pyshow │
└─────────────────────────────────┘

 Florian Dupeyron
 July 2022
"""

from pyshow.core.fixtures  import Fixture

from pyshow.dmx.fixtures   import Fixture_DMX
from pyshow.dmx.controller import DMX_Controller
from pyshow.dmx.interfaces import (
    RangeValue_DMX_8Bits,
    RangeValue_DMX_16Bits
)

from pyshow.core.interfaces import (
    ColorValue,
    RotationValue
)

from dataclasses import dataclass, field, asdict, InitVar
from pprint      import pprint

from typing      import Dict

# ┌────────────────────────────────────────┐
# │ Dumb DMX controller                    │
# └────────────────────────────────────────┘

class DumbController(DMX_Controller):
    def __init__(self):
        super().__init__()

    def _on_ch_set(self, ch: int, value: int):
        print(f"Set ch #{ch:3d}: {value}")


# ┌────────────────────────────────────────┐
# │ Dumb DMX Fixture                       │
# └────────────────────────────────────────┘

@dataclass(kw_only=True)
class MyFixture(Fixture_DMX):
    transport: InitVar[DMX_Controller]
    channel_start: int

    brand: str = "Generic"
    name: str  = "Generic RGB DMX fixture"

    interfaces: Dict[str, any] = field(default_factory=lambda: dict(
        dimmer = RangeValue_DMX_8Bits(
            channel = 0,
            min     = 0.0,
            max     = 100.0,
            unit    = "%"
        ),

        color = ColorValue(
            r = RangeValue_DMX_8Bits(
                channel = 1,
                min     = 0.0,
                max     = 1.0,
                unit    = ""
            ),

            g = RangeValue_DMX_8Bits(
                channel = 2,
                min     = 0.0,
                max     = 1.0,
                unit    = ""
            ),

            b = RangeValue_DMX_8Bits(
                channel = 3,
                min     = 0.0,
                max     = 1.0,
                unit    = ""
            )
        ),
    ))

@dataclass(kw_only=True)
class MyMovingHead(Fixture_DMX):
    transport: InitVar[DMX_Controller]
    channel_start: int

    brand: str = "Generic"
    name: str  = "Generic moving head"

    interfaces: Dict[str, any] = field(default_factory=lambda: dict(
        dimmer = RangeValue_DMX_8Bits(
            channel = 0,
            min     = 0.0,
            max     = 100.0,
            unit    = "%"
        ),

        color = ColorValue(
            r = RangeValue_DMX_8Bits(
                channel = 1,
                min     = 0.0,
                max     = 1.0,
                unit    = ""
            ),

            g = RangeValue_DMX_8Bits(
                channel = 2,
                min     = 0.0,
                max     = 1.0,
                unit    = ""
            ),

            b = RangeValue_DMX_8Bits(
                channel = 3,
                min     = 0.0,
                max     = 1.0,
                unit    = ""
            )
        ),

        pos = RotationValue(
            pan = RangeValue_DMX_16Bits(
                channel_msb=4,
                channel_lsb=5,

                min        = 0.0,
                max        = 360.0,
                unit       = "°"
            ),

            tilt = RangeValue_DMX_16Bits(
                channel_msb= 4,
                channel_lsb= 5,

                min        = 0.0,
                max        = 360.0,
                unit       = "°"
            )
        )

    ))

if __name__ == "__main__":
    # Init transport
    transport = DumbController()

    # Init fixture
    fixture = MyFixture(transport=transport, channel_start=1)

    # Set some values
    fixture.interfaces["dimmer"].set (100.0)
    fixture.interfaces["color"].r.set(0.5  )
    fixture.interfaces["color"].g.set(0.23 )
    fixture.interfaces["color"].b.set(0.8  )

    print("Serialize fixture: ")
    pprint(asdict(fixture))

    fixt2 = MyMovingHead(transport=transport, channel_start=4)
    pprint(asdict(fixt2))
