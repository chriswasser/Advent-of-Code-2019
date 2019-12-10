#!/usr/bin/env python3

import fileinput
from math import atan2, sqrt, pi
from collections import namedtuple, defaultdict


Point = namedtuple('Point', field_names=['x', 'y'])


def test_task1():
    assert True
    print('tests for task 1: ok')


def solve_task1():
    asteroids = []
    for y, line in enumerate(fileinput.input()):
        for x, char in enumerate(line.rstrip('\n')):
            if char == '#':
                asteroids.append(Point(x, y))

    max_visible = -1
    for station in asteroids:
        visible = {
            atan2(station.y - asteroid.y, station.x - asteroid.x)
            for asteroid in asteroids
            if asteroid != station
        }
        if len(visible) > max_visible:
            max_visible, max_station = len(visible), station
    print(f'answer to task 1: {max_visible} @ {max_station}')


def test_task2():
    assert True
    print('tests for task 2: ok')


def solve_task2():
    asteroids = []
    for y, line in enumerate(fileinput.input()):
        for x, char in enumerate(line):
            if char == '#':
                asteroids.append(Point(x, y))

    station = Point(x=22, y=28)

    angles = defaultdict(list)
    for asteroid in asteroids:
        if asteroid == station:
            continue
        angle = atan2(station.y - asteroid.y, station.x - asteroid.x)
        dist = sqrt((station.x - asteroid.x) ** 2 + (station.y - asteroid.y) ** 2)
        angles[angle].append((dist, asteroid))

    for key in angles.keys():
        angles[key] = sorted(angles[key], key=lambda x: x[0])

    vaporized = []
    while angles.keys():
        for key in sorted(angles.keys(), key=lambda x: (x * 180 / pi + 270) % 360):
            vaporized.append(angles[key][0])
            del angles[key][0]
            if not angles[key]:
                del angles[key]

    # 2404 too high
    print(vaporized[0])
    print(vaporized[1])
    print(vaporized[2])
    print(vaporized[9])
    print(vaporized[19])
    print(vaporized[49])
    print(vaporized[99])
    print(vaporized[198])
    print(vaporized[199])
    print(vaporized[200])
    print(vaporized[298])
    print(f'answer to task 2: {vaporized[199][1].x * 100 + vaporized[199][1].y}')


def main():
    test_task1()
    solve_task1()
    test_task2()
    solve_task2()


if __name__ == '__main__':
    main()
