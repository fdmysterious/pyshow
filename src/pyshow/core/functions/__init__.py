"""
┌──────────────────────────────────┐
│ Base classes to define Functions │
└──────────────────────────────────┘

 Florian Dupeyron
 July 2022
"""

import asyncio
import time

from abc                    import ABC, abstractmethod
from pyshow.core.interfaces import BaseValue, RangeValue

from dataclasses            import dataclass

from typing import List, Dict, Tuple

# ┌────────────────────────────────────────┐
# │ Base function class                    │
# └────────────────────────────────────────┘

class Function:
    def __init__(self, interface: BaseValue = None):
        self.interface = interface
        self.dirty     = asyncio.Event()

    async def update(self, timestamp: float):
        pass

    def trigger(self):
        self.dirty.set()

    def finished(self):
        return not self.dirty.is_set()

# ┌────────────────────────────────────────┐
# │ Special delay function                 │
# └────────────────────────────────────────┘

class Function_Delay(Function):
    def __init__(self, delay_s: float):
        super().__init__()

        self.delay_s = delay_s

        self.tend    = None

    async def update(self, tstamp: float):
        # Delay has just started
        if self.tend is None:
            self.tend = tstamp + self.delay_s

        # Delay is elapsed
        elif tstamp > self.tend:
            self.tend = None
            self.dirty.clear()


# ┌────────────────────────────────────────┐
# │ Static function                        │
# └────────────────────────────────────────┘

class Function_Static(Function):
    def __init__(self, interface: BaseValue = None, target: float = 0.0):
        super().__init__(interface)
        self._target = target

    async def update(self, timestamp: float):
        if self.dirty.is_set():
            v = await self._compute_value(timestamp)
            self.interface.set(v)
            self.dirty.clear()

    async def _compute_value(self, timestamp: float):
        return self._target

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, v: float):
        self._target = v
        self.dirty.set()


# ┌────────────────────────────────────────┐
# │ Fade function                          │
# └────────────────────────────────────────┘

class Function_Fade(Function):
    def __init__(self, target: float, fade_time_s: float, interface: RangeValue = None):
        super().__init__(interface)
        if not isinstance(interface, RangeValue):
            raise TypeError(f"{self.__class__.name} only works for RangeValue based interfaces")

        self.fade_time_s   = fade_time_s # Fade time before target value

        self.target        = target

        self._v_start      = 0           # Start value
        self._tstamp_start = 0           # Start timestamp

        self._tstamp_last  = 0           # Last execution timestamp
        self._tstamp_end   = 0           # Timestamp when target value should be reached

        #self._dy           = 0           # Difference on y when in update
        #self._dx           = 0           # Difference on x when in update
        self._delta        = 0            # Derivative of the curve



    async def update(self, timestamp: float):
        if self.dirty.is_set():
            v = await self._compute_value(timestamp)
            self.interface.set(v)

            if timestamp > self._tstamp_end:
                self.dirty.clear() # Last value has been set!
    

    async def _compute_value(self, timestamp: float):
        v_cur = self.interface.get()     # Current value
        v_new = self.target              # By default, target value

        if timestamp < self._tstamp_end: # In middle of an update, compute value using linear interpolation
            dt    = timestamp-self._tstamp_start
            v_new = self._delta*dt + self._v_start

        # Clip value
        v_new = self.interface.max if v_new > self.interface.max else v_new
        v_new = self.interface.min if v_new < self.interface.min else v_new

        self._tstamp_last = timestamp

        return v_new


    def trigger(self):
        self._v_start      = self.interface.get()
        self._tstamp_start = time.time()

        self._tstamp_end   = time.time() + self.fade_time_s

        dy           = self.target-self._v_start
        dx           = self._tstamp_end-self._tstamp_start
        self._delta  = dy/dx

        self.dirty.set()


# ┌────────────────────────────────────────┐
# │ Animation function                     │
# └────────────────────────────────────────┘

class Function_Animation(Function):
    def __init__(self, interface: BaseValue = None):
        super().__init__(interface)
        
    async def update(self, timestamp: float):
        v = await self._compute_value(timestamp)
        self.interface.set(v)
        self.dirty.set()

    async def _compute_value(self, timestamp: float):
        pass


# ┌────────────────────────────────────────┐
# │ Periodic function                      │
# └────────────────────────────────────────┘

class Function_Periodic(Function):
    def __init__(self, period_s: float, interface: BaseValue = None ):
        super().__init__(interface)

        self.period_s       = period_s
        self.last_execution = 0.0


    async def update(self, timestamp: float):
        if (timestamp - self.last_execution) >= self.period_s:
            self.dirty.set()

        if self.dirty.is_set():
            v = await self._compute_value(timestamp)
            self.interface.set(v)
            self.dirty.clear()
            self.last_execution = timestamp

