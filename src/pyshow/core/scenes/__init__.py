"""
┌─────────────────────────┐
│ Base classes for Scenes │
└─────────────────────────┘

 Florian Dupeyron
 July 2022
"""

import asyncio

from typing                import List, Dict
from pyshow.core.functions import (Function)
from functools             import reduce


# ┌────────────────────────────────────────┐
# │ Basic scene                            │
# └────────────────────────────────────────┘

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


# ┌────────────────────────────────────────┐
# │ Scene_Chooser class                    │
# └────────────────────────────────────────┘

class Scene_Chooser:
    def __init__(self, scenes: Dict[str, Scene] = None):
        self.scenes              = scenes or dict()

        self._scene_current      = None
        self._scene_flash        = None

        self._scene_current_name = None
        self._scene_flash_name   = None


    # ┌────────────────────────────────────────┐
    # │ Choose and get current scene           │
    # └────────────────────────────────────────┘
    
    def choose(self, name: str):
        try:
            self._scene_current_name = name
            self._scene_current      = self.scenes[name]
            self._scene_current.trigger()
        except KeyError as exc:
            raise KeyError(f"No such scene: {exc!s}")
    
    def current(self):
        return self._scene_current_name

    # ┌────────────────────────────────────────┐
    # │ Flash feature                          │
    # └────────────────────────────────────────┘

    def flash_start(self, name: str):
        try:
            self._scene_flash_name = name
            self._scene_flash      = self.scenes[name]
            self._scene_flash.trigger()
        except KeyError as exc:
            raise KeyError(f"No such scene: {exc!s}")


    def flash_end(self):
        self._scene_flash = None
        if self._scene_current is not None:
            self._scene_current.trigger()


    def flash_current(self):
        return self._scene_flash_name


    # ┌────────────────────────────────────────┐
    # │ Update                                 │
    # └────────────────────────────────────────┘

    async def update(self, tstamp: float):
        if self._scene_flash is not None:
            await self._scene_flash.update(tstamp)
        elif self._scene_current is not None:
            await self._scene_current.update(tstamp)


    def finished(self):
        if self._scene_flash is not None:
            return self._scene_flash.finished()
        elif self._scene_current is not None:
            return self._scene_current.finished()
        return True # By default, finished

    
