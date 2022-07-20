"""
┌───────────────────────────┐
│ Control desk base classes │
└───────────────────────────┘

 Florian Dupeyron
 July 2022
"""

import asyncio
import threading

class Control_Desk:
    def __init__(self):
        self._queue = asyncio.Queue()
        self._task  = None
        self._loop  = None

    def start(self, loop):
        self._loop = loop
        self._task = loop.create_task(self._process())

    def stop(self, loop):
        self._task.cancel()
        self._task = None
        self._loop = None

    # ┌────────────────────────────────────────┐
    # │ User utilities                         │
    # └────────────────────────────────────────┘

    def _push_event(self, ev: any):
        async def _push_ev_task(self, ev: any):
            await self._queue.put(ev)

        future = asyncio.run_coroutine_threadsafe(_push_ev_task(self, ev), self._loop)
        result = future.result() # Await execution


    # ┌────────────────────────────────────────┐
    # │ Main process loop                      │
    # └────────────────────────────────────────┘
    
    async def _process(self):
        await self._hook_open()
        try:
            while True:
                ev = await self._queue.get()
                await self._hook_process(ev)

        except asyncio.CancelledError:
            pass
        finally:
            await self._hook_close()


    # ┌────────────────────────────────────────┐
    # │ User hooks                             │
    # └────────────────────────────────────────┘

    async def _hook_process(self, ev):
        pass
    
    async def _hook_open(self):
        pass

    async def _hook_close(self):
        pass


