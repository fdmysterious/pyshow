"""
┌───────────────────────────┐
│ DMX Controller base class │
└───────────────────────────┘

 Florian Dupeyron
 July 2022
"""

from abc import ABC, abstractmethod


# ┌────────────────────────────────────────┐
# │ DMX Controller base class              │
# └────────────────────────────────────────┘

class DMX_Controller:
    def __init__(self):
        pass

    def ch_set(self, ch: int, value: int):
        if (ch < 0) or (ch >= 512):
            raise ValueError(f"DMX Channel out of bounds: {ch}")
        if (value < 0) or (value > 255):
            raise ValueError(f"DMX Value out of bounds: {value}")

        self._on_ch_set(ch, value)

    @abstractmethod
    def _on_ch_set(self, ch: int, value: int):
        pass

