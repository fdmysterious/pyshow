"""
┌──────────────────────────────────────┐
│ Simple OSC controller implementation │
└──────────────────────────────────────┘

 Florian Dupeyron
 July 2022
"""

import asyncio
import logging

from pythonosc           import dispatcher
from pythonosc           import osc_server

from pyshow.core.control import Control_Desk
from asyncio.exceptions  import CancelledError

# ┌────────────────────────────────────────┐
# │ Control_Desk_OSC class                 │
# └────────────────────────────────────────┘

class Control_Desk_OSC(Control_Desk):
    def __init__(self, host: str, port: int):
        super().__init__()

        self.host         = host
        self.port         = port

        self._filters     = dict()

        self.log          = logging.getLogger(f"OSC control on {self.host}:{self.port}")

        # # # # # #
        self.dispatcher   = dispatcher.Dispatcher()
        self.dispatcher.set_default_handler(self._osc_in_handler)

        self.server                   = None
        self.transport, self.protocol = None, None

    
    def event_register(self, path, cbk):
        self.log.debug(f"Register event for path {path}")
        if path in self._filters:
            raise ValueError(f"Path already registered: {path}")
        self._filters[path] = cbk


    # ───── Process OSC message callback ───── #

    def _osc_in_handler(self, path, *args):
        self.log.debug(f"Process in OSC: {path} with args {args}")
        self._push_event((path, args,))


    # ───────── Hooks implementation ───────── #
    
    async def _hook_open(self):
        self.log.info("Open OSC server")
        self.server = osc_server.AsyncIOOSCUDPServer(
            (self.host, self.port),
            self.dispatcher,
            self._loop
        )

        self.transport, self.protocol = await self.server.create_serve_endpoint()


    async def _hook_close(self):
        self.log.info("Close OSC server")
        self.transport.close()

        self.server    = None
        self.transport = None
        self.protocol  = None


    async def _hook_process(self, ev):
        path, args = ev
        self.log.debug(f"Process OSC event: {path} with args {args}")
    
        if path in self._filters:
            # Callback for event
            self._filters[path](*args)
