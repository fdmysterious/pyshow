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

# ┌────────────────────────────────────────┐
# │ Base function class                    │
# └────────────────────────────────────────┘

class Function:
    def __init__(self, interface: BaseValue):
        self.interface = interface
        self.dirty     = asyncio.Event()

    async def update(self, timestamp: float):
        pass


# ┌────────────────────────────────────────┐
# │ Static function                        │
# └────────────────────────────────────────┘

class Function_Static(Function):
    def __init__(self, interface: BaseValue):
        super().__init__(interface)

    async def update(self, timestamp: float):
        if self.dirty.is_set():
            v = await self._compute_value(timestamp)
            self.interface.set(v)
            self.dirty.clear()

    async def _compute_value(self, timestamp: float):
        pass

# ┌────────────────────────────────────────┐
# │ Fade function                          │
# └────────────────────────────────────────┘

class Function_Fade(Function):
    def __init__(self, interface: RangeValue, fade_time_s: float):
        super().__init__(interface)
        if not isinstance(interface, RangeValue):
            raise TypeError(f"{self.__class__.name} only works for RangeValue based interfaces")

        self.fade_time_s   = fade_time_s # Fade time before target value

        self._target       = None        # Target value
        self._tstamp_last  = 0           # Last execution timestamp
        self._tstamp_end   = 0           # Timestamp when target value should be reached


    async def update(self, timestamp: float):
        if self.dirty.is_set():
            v = await self._compute_value(timestamp)
            self.interface.set(v)

            if timestamp > self._tstamp_end:
                self.dirty.clear() # Last value has been set!
    

    async def _compute_value(self, timestamp: float):
        v_cur = self.interface.get()     # Current value

        v_new = self._target             # By default, target value
        if timestamp > self._tstamp_end: # In middle of an update, compute value using linear interpolation
            v_new = (self._target - v_cur)/(self._tstamp_end-self._tstamp_last)
        self._tstamp_last = timestamp

        return v_new

    def target_set(self, target: float):
        self._tstamp_end = time.time() + self.fade_time_s

        self._target = target
        self.dirty.set()
            
        
# ┌────────────────────────────────────────┐
# │ Animation function                     │
# └────────────────────────────────────────┘

class Function_Animation(Function):
    def __init__(self, interface: BaseValue):
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
    def __init__(self, interface: BaseValue, period_s: float):
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
