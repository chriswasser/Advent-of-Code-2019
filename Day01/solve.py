#!/usr/bin/env python3

import fileinput
import functools


@functools.lru_cache(maxsize=None)
def fuel(mass):
    return mass // 3 - 2


total_fuel = sum((fuel(int(line)) for line in fileinput.input()))
print(f'answer to part 1: {total_fuel}')


@functools.lru_cache(maxsize=None)
def fuel_recursive(mass):
    if fuel(mass) <= 0:
        return 0
    return fuel(mass) + fuel_recursive(fuel(mass))


total_fuel = sum((fuel_recursive(int(line)) for line in fileinput.input()))
print(f'answer to part 2: {total_fuel}')
