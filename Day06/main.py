#!/usr/bin/env python3

from collections import defaultdict
import fileinput

import numpy as np


def num_orbits(map_data):
    adjacency_list, planets = defaultdict(set), set()
    for line in map_data:
        orbitee, orbiter = line.split(')')
        adjacency_list[orbiter].add(orbitee)
        planets.add(orbitee)
        planets.add(orbiter)

    planets = dict(map(reversed, enumerate(planets)))
    adjaceny_matrix = np.zeros(shape=(len(planets), len(planets)))
    for orbiter in planets:
        for orbitee in adjacency_list[orbiter]:
            adjaceny_matrix[planets[orbiter], planets[orbitee]] = 1

    # Floyd–Warshall (https://en.wikipedia.org/wiki/Floyd–Warshall_algorithm)
    for k in range(len(planets)):
        for i in range(len(planets)):
            for j in range(len(planets)):
                if adjaceny_matrix[i, k] == 1 and adjaceny_matrix[k, j] == 1:
                    adjaceny_matrix[i, j] = 1
    checksum = np.sum(adjaceny_matrix)
    return checksum


def shortest_path(map_data):
    adjacency_list, planets = defaultdict(set), set()
    for line in map_data:
        orbitee, orbiter = line.split(')')
        adjacency_list[orbiter].add(orbitee)
        planets.add(orbitee)
        planets.add(orbiter)

    planets = dict(map(reversed, enumerate(planets)))
    adjaceny_matrix = np.zeros(shape=(len(planets), len(planets)))
    adjaceny_matrix.fill(np.inf)
    for orbiter in planets:
        for orbitee in adjacency_list[orbiter]:
            adjaceny_matrix[planets[orbiter], planets[orbitee]] = 1
            adjaceny_matrix[planets[orbitee], planets[orbiter]] = 1

    # Floyd–Warshall (https://en.wikipedia.org/wiki/Floyd–Warshall_algorithm)
    for k in range(len(planets)):
        for i in range(len(planets)):
            for j in range(len(planets)):
                adjaceny_matrix[i, j] = min(
                    adjaceny_matrix[i, j],
                    adjaceny_matrix[i, k] + adjaceny_matrix[k, j]
                )
    path = adjaceny_matrix[planets['YOU'], planets['SAN']] - 2
    return path


def test_task1():
    assert num_orbits(['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L']) == 42  # noqa: max_line_length
    print('tests for task 1: ok')


def solve_task1():
    map_data = [line.rstrip('\n') for line in fileinput.input()]
    orbits = num_orbits(map_data)
    print(f'answer to task 1: {orbits}')


def test_task2():
    assert shortest_path(['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L', 'K)YOU', 'I)SAN']) == 4  # noqa: max_line_length
    print('tests for task 2: ok')


def solve_task2():
    map_data = [line.rstrip('\n') for line in fileinput.input()]
    path = shortest_path(map_data)
    print(f'answer to task 2: {path}')


def main():
    test_task1()
    solve_task1()
    test_task2()
    solve_task2()


if __name__ == '__main__':
    main()
