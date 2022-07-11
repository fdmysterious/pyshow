"""
┌──────────────────────────┐
│ Steps for basic.features │
└──────────────────────────┘

 Florian Dupeyron
 July 2022
"""

from behave import *

use_match_parser("TODO")

from dataclasses import asdict

from pyshow.core.interfaces import (
    RangeValue,

    DiscreteValue_Choice,
    DiscreteValue
)

# ┌────────────────────────────────────────┐
# │ Generic steps                          │
# └────────────────────────────────────────┘

# ───────────── Instanciation ──────────── #

@given("a `RangeValue` instance with a min of {v_min:d}, a max of {v_max:d}, and a unit of \"{v_unit}\"")
def step(ctx, v_min, v_max, v_unit):
    ctx.instance = RangeValue(min=v_min, max=v_max, unit=v_unit)


@given("a dictonary containing \"{dict_repr}\"")
def step(ctx, dict_repr):
    dict_value = eval(dict_repr)
    ctx.dict_value = dict_value

# ────────── Instance's asserts ────────── #

@then("The instance's \"{field}\" is equal to the number {value}")
def step(ctx, field, value):
    value = float(value)
    assert hasattr(ctx.instance, field)
    assert getattr(ctx.instance, field) == value


@then("The instance's \"{field}\" is equal to the string \"{value}\"")
def step(ctx, field, value):
    assert hasattr(ctx.instance, field)
    assert getattr(ctx.instance, field) == value


# ┌────────────────────────────────────────┐
# │ Serialize/Deserialize                  │
# └────────────────────────────────────────┘

@when("I serialize the instance")
def step(ctx):
    ctx.instance_serialized = asdict(ctx.instance)


@then("The serialized value is \"{dict_repr}\"")
def step(ctx, dict_repr):
    dict_value = eval(dict_repr) # Convert from string to dict

    # TODO # Comparaison using dictdiffer

@when("I create an instance of `RangeValue` using the dictionnary")
def step(ctx):
    ctx.instance = RangeValue(**ctx.dict_value)
