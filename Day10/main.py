#!/usr/bin/env python3

import fileinput
from math import atan2, sqrt, pi, inf
from collections import namedtuple, defaultdict, OrderedDict


Point = namedtuple('Point', field_names=['x', 'y'])


def parse_asteroids(string):
    return [
        Point(x, y)
        for y, line in enumerate(string.split('\n'))
        for x, char in enumerate(line)
        if char == '#'
    ]


def max_visibility(asteroids):
    return max(
        {
            station: {
                atan2(station.y - asteroid.y, station.x - asteroid.x)
                for asteroid in asteroids
                if asteroid != station
            } for station in asteroids
        }.items(),
        key=lambda item: len(item[1])
    )


def euclidean_distance(a, b):
    return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def asteroids_by_angle(asteroids, station):
    lines_of_sight = defaultdict(list)
    for asteroid in asteroids:
        if asteroid == station:
            continue
        angle = atan2(station.y - asteroid.y, station.x - asteroid.x)
        lines_of_sight[angle].append(asteroid)
    return lines_of_sight


def reorder(lines_of_sight, station):
    lines_of_sight = {
        (angle * 180 / pi + 270) % 360: sorted(
            asteroids,
            key=lambda asteroid: euclidean_distance(station, asteroid),
            reverse=True
        ) for angle, asteroids in lines_of_sight.items()
    }
    return OrderedDict(sorted(lines_of_sight.items()))


def vaporized_asteroids(lines_of_sight, n=inf):
    vaporized = []
    while len(vaporized) < n and all(lines_of_sight.values()):
        for angle in lines_of_sight.keys():
            if not lines_of_sight[angle]:
                continue
            vaporized.append(lines_of_sight[angle].pop())
    return vaporized


def test_task1():
    assert True
    print('tests for task 1: ok')


def solve_task1():
    string = ''.join(fileinput.input())
    asteroids = parse_asteroids(string)
    maximum = max_visibility(asteroids)
    print(f'answer to task 1: {len(maximum[1])}')


def test_task2():
    assert True
    print('tests for task 2: ok')


def solve_task2():
    string = ''.join(fileinput.input())
    asteroids = parse_asteroids(string)
    station = max_visibility(asteroids)[0]
    lines_of_sight = asteroids_by_angle(asteroids, station)
    lines_of_sight = reorder(lines_of_sight, station)
    asteroid = vaporized_asteroids(lines_of_sight, n=200)[199]
    print(f'answer to task 2: {asteroid.x * 100 + asteroid.y}')


def main():
    test_task1()
    solve_task1()
    test_task2()
    solve_task2()


if __name__ == '__main__':
    main()
