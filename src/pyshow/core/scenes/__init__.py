"""
┌─────────────────────────┐
│ Base classes for Scenes │
└─────────────────────────┘

 Florian Dupeyron
 July 2022
"""

import asyncio
import time

from typing                import List, Dict, Tuple
from pyshow.core.functions import (Function)
from functools             import reduce, partial

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


    def randomize(self):
        for fkt in filter(lambda x: hasattr(x, "randomize")):
            fkt.randomize()


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
    

    # ┌────────────────────────────────────────┐
    # │ Randomize                              │
    # └────────────────────────────────────────┘

    def randomize(self):
        if self._scene_flash is not None:
            self._scene_flash.randomize()
            self._scene_flash.trigger()
        elif self._scene_current is not None:
            self._scene_current.randomize()
            self._scene_current.trigger()


# ┌────────────────────────────────────────┐
# │ Scene_Sequence class                   │
# └────────────────────────────────────────┘

class Scene_Sequence:
    """
    Defines a sequence, which is a suite of scenes, referred to as "steps".

    - auto mode: The next step is triggered automatically when the previous has
    finished. By default, the next step must be triggered manually using the "next"
    function.
    - loop mode: When all steps are finished, the next one is the first one.
    """

    def __init__(self, steps: List[Scene], auto: bool=True, loop: bool=True):
        self.steps = steps
        self.auto  = auto
        self.loop  = loop

        self._idx  = None

    # ──────────────── Update ──────────────── #
    async def update(self, tstamp: float):
        if not self.finished():
            cur_step = self.steps[self._idx]

            # Initial trigger check
            if cur_step.finished(): cur_step.trigger()

            # Update
            await cur_step.update(tstamp)

            # Next (if in auto mode) ?
            if cur_step.finished() and self.auto: self.next()

    # ────────────── Lifesceheme ───────────── #
    
    def finished(self):
        return self._idx is None

    # ─────────── Sequence control ─────────── #

    def trigger(self):
        self._idx = 0
    

    def next(self):
        if not self.finished():
            self._idx += 1

            # Loop control
            if self._idx >= len(self.steps):
                self._idx = 0 if self.loop else None
