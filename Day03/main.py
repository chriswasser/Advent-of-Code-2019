#!/usr/bin/env python3

from collections import namedtuple
import fileinput


Point = namedtuple('Point', field_names=['x', 'y'], defaults=[0, 0])


def manhattan_distance(point1, point2):
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)


def move(point, direction):
    x, y = point
    if direction == 'U':
        y += 1
    elif direction == 'D':
        y -= 1
    elif direction == 'R':
        x += 1
    elif direction == 'L':
        x -= 1
    return Point(x, y)


def path(wire):
    path_, point, steps = dict(), Point(), 0
    for instruction in wire.split(','):
        direction, num_fields = instruction[:1], int(instruction[1:])
        for _ in range(num_fields):
            point, steps = move(point, direction), steps + 1
            if point not in path_:
                path_[point] = steps
    return path_


def intersections(wire1, wire2):
    path_wire1, path_wire2 = path(wire1), path(wire2)
    intersections_ = {
        point: path_wire1[point] + path_wire2[point]
        for point in path_wire1.keys() & path_wire2.keys()
    }
    return intersections_


def distance_closest_intersection(wire1, wire2):
    intersections_ = intersections(wire1, wire2)
    closest_point = min(intersections_.keys(), key=lambda point: manhattan_distance(Point(), point))
    distance = manhattan_distance(Point(), closest_point)
    return distance


def steps_cheapest_intersection(wire1, wire2):
    intersections_ = intersections(wire1, wire2)
    cheapest_intersection = min(intersections_.items(), key=lambda item: item[1])
    steps = cheapest_intersection[1]
    return steps


def test_task1():
    assert distance_closest_intersection('R8,U5,L5,D3', 'U7,R6,D4,L4') == 6
    assert distance_closest_intersection(
        'R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83'
    ) == 159
    assert distance_closest_intersection(
        'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'
    ) == 135
    print('tests for task 1: ok')


def solve_task1():
    wire1, wire2 = [line for line in fileinput.input()]
    distance = distance_closest_intersection(wire1, wire2)
    print(f'answer to task 1: {distance}')


def test_task2():
    assert steps_cheapest_intersection('R8,U5,L5,D3', 'U7,R6,D4,L4') == 30
    assert steps_cheapest_intersection(
        'R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83'
    ) == 610
    assert steps_cheapest_intersection(
        'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'
    ) == 410
    print('tests for task 2: ok')


def solve_task2():
    wire1, wire2 = [line for line in fileinput.input()]
    steps = steps_cheapest_intersection(wire1, wire2)
    print(f'answer to task 2: {steps}')


def main():
    test_task1()
    solve_task1()
    test_task2()
    solve_task2()


if __name__ == '__main__':
    main()
