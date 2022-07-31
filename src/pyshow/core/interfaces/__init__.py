"""
┌─────────────────┐
│ Main interfaces │
└─────────────────┘

 Florian Dupeyron
 July 2022
"""

from dataclasses import dataclass, field
from typing      import Optional, Dict


# ┌────────────────────────────────────────┐
# │ BaseValue base class                   │
# └────────────────────────────────────────┘

@dataclass(kw_only=True)
class BaseValue:
    class_id: str = ""

    def __post_init__(self):
        pass

    # ─────────── Fixture property ─────────── #

    # This property can be reimplemented by subclasses
    # For specific behaviour, for example when a interface
    # Groups specific interfaces.

    @property
    def fixture(self):
        return None
    
    @fixture.setter
    def fixture(self, fixt):
        pass


# ┌────────────────────────────────────────┐
# │ AtomicValue interface class            │
# └────────────────────────────────────────┘

@dataclass(kw_only=True)
class AtomicValue(BaseValue):
    def __post_init__(self):
        super().__post_init__()
        self.__fixture = None


    @property
    def fixture(self):
        return self.__fixture
    

    @fixture.setter
    def fixture(self, fixt):
        self.__fixture = fixt


# ┌────────────────────────────────────────┐
# │ GroupValue interface class             │
# └────────────────────────────────────────┘

@dataclass(kw_only=True)
class GroupValue(BaseValue):
    def __post_init__(self):
        super().__post_init__()
        self.__fixture = None

    @property
    def fixture(self):
        return self.__fixture
        
    
    @fixture.setter
    def fixture(self, fixt):
        self.__fixture = fixt

        # Attach to children
        for ch_name, ch in self.__dict__.items():
            if isinstance(ch, BaseValue):
                ch.fixture = self.__fixture


# ┌────────────────────────────────────────┐
# │ RangeValue interface class             │
# └────────────────────────────────────────┘

@dataclass(kw_only=True)
class RangeValue(AtomicValue):
    min: float
    max: float
    
    unit: Optional[str] = ""
    invert: Optional[bool] = False
    class_id: str       = "RangeValue"

    # ─────────────── Post init ────────────── #
    
    def __post_init__(self):
        super().__post_init__()
        self._value = 0

    # ────────────── Set and get ───────────── #
    
    def set(self, v):
        if   v < self.min: raise ValueError(f"{v} < {self.min}")
        elif v > self.max: raise ValueError(f"{v} > {self.max}")
        else:
            self._value = v
            self._on_set(self.max-v if self.invert else v)

    def get(self):
        return self._value

    # ───────────────── Hooks ──────────────── #
    
    def _on_set(self, v):
        pass


# ┌────────────────────────────────────────┐
# │ DiscreteValue interface class          │
# └────────────────────────────────────────┘

@dataclass(kw_only=True)
class DiscreteValue_Choice:
    label: str
    value: any
    image: Optional[str] = ""


@dataclass(kw_only=True)
class DiscreteValue(AtomicValue):
    choices: Dict[str, DiscreteValue_Choice]

    class_id: str = "DiscreteValue"

    # ─────────────── Post init ────────────── #
    
    def __post_init__(self):
        super().__post_init__()
        self._value  = None


    # ─────────────── Set / Get ────────────── #
    
    def set(self, v):
        if not v in self.choices: raise ValueError(f"Invalid discrete value {v}")
        else:
            self._value = v
            self._on_set(v)

    def get(self):
        return self._value


    # ──────── Hooks to be implemented ─────── #
    def _on_set(self, v):
        pass


# ┌────────────────────────────────────────┐
# │ ColorValue interface                   │
# └────────────────────────────────────────┘

@dataclass(kw_only=True)
class ColorValue(GroupValue):
    r: RangeValue
    g: RangeValue
    b: RangeValue

    class_id: str = "ColorValue"


# ┌────────────────────────────────────────┐
# │ RotationValue interface                │
# └────────────────────────────────────────┘

@dataclass(kw_only=True)
class RotationValue(GroupValue):
    pan:  RangeValue
    tilt: RangeValue
    
    class_id: str = "RotationValue"

    def set(self, x: float, y: float):
        self.pan.set(x)
        self.tilt.set(y)
