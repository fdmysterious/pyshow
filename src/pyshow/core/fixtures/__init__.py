"""
┌────────────────────┐
│ Fixture base class │
└────────────────────┘

 Florian Dupeyron
 July 2022
"""


from dataclasses import dataclass, field
from copy        import deepcopy

from typing      import Dict


# ┌────────────────────────────────────────┐
# │ Main fixture base class                │
# └────────────────────────────────────────┘

@dataclass
class Fixture:
    brand: str
    name: str

    interfaces: Dict[str,any]

    def __post_init__(self):
        # Associate fixture with interfaces
        for itf_name, itf in self.interfaces.items():
            itf.fixture = self
