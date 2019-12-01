#!/usr/bin/env python3

import fileinput
import functools


@functools.lru_cache(maxsize=None)
def fuel(mass):
    return mass // 3 - 2


@functools.lru_cache(maxsize=None)
def fuel_recursive(mass):
    if fuel(mass) <= 0:
        return 0
    return fuel(mass) + fuel_recursive(fuel(mass))


def test_task1():
    assert fuel(12) == 2
    assert fuel(14) == 2
    assert fuel(1969) == 654
    assert fuel(100756) == 33583
    print('tests for task 1: ok')


def solve_task1():
    total_fuel = sum(fuel(int(line)) for line in fileinput.input())
    print(f'answer to task 1: {total_fuel}')


def test_task2():
    assert fuel_recursive(14) == 2
    assert fuel_recursive(1969) == 966
    assert fuel_recursive(100756) == 50346
    print('tests for task 2: ok')


def solve_task2():
    total_fuel = sum(fuel_recursive(int(line)) for line in fileinput.input())
    print(f'answer to task 2: {total_fuel}')


def main():
    test_task1()
    solve_task1()
    test_task2()
    solve_task2()


if __name__ == '__main__':
    main()
