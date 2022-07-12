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
from pyshow.core.interfaces import BaseValue

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
