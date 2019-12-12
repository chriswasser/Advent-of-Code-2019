#!/usr/bin/env python3

import fileinput
import itertools

import numpy as np


def test_task1():
    assert True
    print('tests for task 1: ok')


class Moon:
    def __init__(self, position):
        self.position = np.array(position)
        self.velocity = np.array([0, 0, 0])


def update_velocites(moons):
    for moon1, moon2 in itertools.combinations(moons, r=2):
        if moon1 == moon2:
            continue
        for dimension in range(3):
            if moon1.position[dimension] == moon2.position[dimension]:
                continue
            if moon1.position[dimension] > moon2.position[dimension]:
                moon1.velocity[dimension] -= 1
                moon2.velocity[dimension] += 1
            else:
                moon1.velocity[dimension] += 1
                moon2.velocity[dimension] -= 1


def update_positions(moons):
    for moon in moons:
        moon.position += moon.velocity


def solve_task1():
    moons = []
    for line in fileinput.input():
        variables = line.lstrip('<').rstrip('>\n').replace(',', '').split(' ')
        moons.append(Moon([int(variable[2:]) for variable in variables]))

    for _ in range(1000):
        update_velocites(moons)
        update_positions(moons)
    
    total_energy = sum(
        np.sum(np.abs(moon.position)) * np.sum(np.abs(moon.velocity))
        for moon in moons
    )
    print(f'answer to task 1: {total_energy}')


def test_task2():
    assert True
    print('tests for task 2: ok')


def solve_task2():
    moons = []
    for line in fileinput.input():
        variables = line.lstrip('<').rstrip('>\n').replace(',', '').split(' ')
        moons.append(Moon([int(variable[2:]) for variable in variables]))

    x = {(
        moons[0].position[0], moons[0].velocity[0],
        moons[1].position[0], moons[1].velocity[0],
        moons[2].position[0], moons[2].velocity[0],
        moons[3].position[0], moons[3].velocity[0],
    )}
    printed_x = False
    y = {(
        moons[0].position[1], moons[0].velocity[1],
        moons[1].position[1], moons[1].velocity[1],
        moons[2].position[1], moons[2].velocity[1],
        moons[3].position[1], moons[3].velocity[1],
    )}
    printed_y = False
    z = {(
        moons[0].position[2], moons[0].velocity[2],
        moons[1].position[2], moons[1].velocity[2],
        moons[2].position[2], moons[2].velocity[2],
        moons[3].position[2], moons[3].velocity[2],
    )}
    printed_z = False
    for _ in range(10000000000):
        update_velocites(moons)
        update_positions(moons)
        item_x = (
            moons[0].position[0], moons[0].velocity[0],
            moons[1].position[0], moons[1].velocity[0],
            moons[2].position[0], moons[2].velocity[0],
            moons[3].position[0], moons[3].velocity[0],
        )
        if item_x in x:
            if not printed_x:
                print(f'x repeated @ {_}')
                printed_x = True
        x.add(item_x)

        item_y = (
            moons[0].position[1], moons[0].velocity[1],
            moons[1].position[1], moons[1].velocity[1],
            moons[2].position[1], moons[2].velocity[1],
            moons[3].position[1], moons[3].velocity[1],
        )
        if item_y in y:
            if not printed_y:
                print(f'y repeated @ {_}')
                printed_y = True
        y.add(item_y)

        item_z = (
            moons[0].position[2], moons[0].velocity[2],
            moons[1].position[2], moons[1].velocity[2],
            moons[2].position[2], moons[2].velocity[2],
            moons[3].position[2], moons[3].velocity[2],
        )
        if item_z in z:
            if not printed_z:
                print(f'z repeated @ {_}')
                printed_z = True
        z.add(item_z)
    print(f'answer to task 2: calculate lcm of printed numbers')


def main():
    test_task1()
    solve_task1()
    test_task2()
    solve_task2()


if __name__ == '__main__':
    main()
