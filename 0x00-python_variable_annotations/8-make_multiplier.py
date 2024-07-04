#!/usr/bin/env python3
"""Write a type-annotated function make_multiplier that takes
a float multiplier as argument and returns a function that
multiplies a float by multiplier.
"""

import typing


def make_multiplier(multiplier: float) -> typing.Callable[[float], float]:
    """returns a function that multiplies a float by multiplier"""
    def float_multiplier(x: float) -> float:
        return multiplier * x

    return float_multiplier
