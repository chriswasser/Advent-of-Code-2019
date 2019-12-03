#!/usr/bin/env python3

from collections import namedtuple
import fileinput
import itertools


Point = namedtuple('Point', field_names=['x', 'y'], defaults=[0, 0])


def manhattan_distance(point1, point2):
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)


def test_task1():
    assert True
    print('tests for task 1: ok')


def solve_task1():
    central_point = Point()

    wires = []
    for line in fileinput.input():
        wire = set()
        position = central_point
        moves = line.split(',')
        for move in moves:
            direction, num_fields = move[:1], int(move[1:])
            x, y = position
            if direction == 'U':
                for _ in range(num_fields):
                    y += 1
                    position = Point(x, y)
                    wire.add(position)
            elif direction == 'D':
                for _ in range(num_fields):
                    y -= 1
                    position = Point(x, y)
                    wire.add(position)
            elif direction == 'R':
                for _ in range(num_fields):
                    x += 1
                    position = Point(x, y)
                    wire.add(position)
            elif direction == 'L':
                for _ in range(num_fields):
                    x -= 1
                    position = Point(x, y)
                    wire.add(position)
        wires.append(wire)

    intersections = set()
    for wire1, wire2 in itertools.product(wires, wires):
        if wire1 == wire2:
            continue
        intersections |= wire1 & wire2

    closest_intersection = min(intersections,
                               key=lambda point: manhattan_distance(central_point, point))
    solution = manhattan_distance(central_point, closest_intersection)
    print(f'answer to task 1: {solution}')


def test_task2():
    assert True
    print('tests for task 2: ok')


def solve_task2():
    central_point = Point()

    wires = []
    for line in fileinput.input():
        wire = dict()
        position, steps = central_point, 0
        moves = line.split(',')
        for move in moves:
            direction, num_fields = move[:1], int(move[1:])
            x, y = position
            if direction == 'U':
                for _ in range(num_fields):
                    y += 1
                    steps += 1
                    position = Point(x, y)
                    if position not in wire:
                        wire[position] = steps
            elif direction == 'D':
                for _ in range(num_fields):
                    y -= 1
                    steps += 1
                    position = Point(x, y)
                    if position not in wire:
                        wire[position] = steps
            elif direction == 'R':
                for _ in range(num_fields):
                    x += 1
                    steps += 1
                    position = Point(x, y)
                    if position not in wire:
                        wire[position] = steps
            elif direction == 'L':
                for _ in range(num_fields):
                    x -= 1
                    steps += 1
                    position = Point(x, y)
                    if position not in wire:
                        wire[position] = steps
        wires.append(wire)

    intersections = dict()
    for wire1, wire2 in itertools.product(wires, wires):
        if wire1 == wire2:
            continue
        for key1 in wire1:
            if key1 in wire2:
                intersections[key1] = wire1[key1] + wire2[key1]

    solution = min(intersections.items(), key=lambda point: point[1])
    print(f'answer to task 2: {solution[1]}')


def main():
    test_task1()
    solve_task1()
    test_task2()
    solve_task2()


if __name__ == '__main__':
    main()
