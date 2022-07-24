"""
┌───────────────────────────────┐
│ Simple test using 60W fixture │
└───────────────────────────────┘

 Florian Dupeyron
 July 2022
"""

import time
import logging

from pyshow.fixtures.nobrand.moving_head_60w import NoBrand_60W_MovingHead_11Ch
from pyshow.dmx.stm32dmx import DMX_Controller_STM32

logging.basicConfig(level=logging.DEBUG)

transport = DMX_Controller_STM32("/dev/ttyACM0")
fixture   = NoBrand_60W_MovingHead_11Ch(transport=transport, channel_start=0)

transport.open()

fixture.interfaces["pos"].pan.set (180)
fixture.interfaces["pos"].tilt.set(180)
fixture.interfaces["dimmer"].set(50)
fixture.interfaces["color"].set("cyan_orange")

transport.flush()
