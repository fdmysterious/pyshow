"""
┌─────────────────────────┐
│ Base classes for Scenes │
└─────────────────────────┘

 Florian Dupeyron
 July 2022
"""

import asyncio

from typing                import List
from pyshow.core.functions import (Function)
from functools             import reduce

class Scene:
    def __init__(self, functions: List[Function] = None):
        self.functions = functions or []

    def trigger(self):
        for f in self.functions: f.trigger()

    async def update(self, timestamp: float):
        await asyncio.gather(*[
            fkt.update(timestamp) for fkt in self.functions
        ])

    def finished(self):
        return reduce(
            lambda a,b: a and b,
            map(lambda x: x.finished(), self.functions),
            True
        )
